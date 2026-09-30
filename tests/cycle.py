#!/usr/bin/env python3
"""Destructive-boundary proofs using only tiny, uniquely owned Scratch fixtures."""
import fcntl
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch
import uuid

sys.dont_write_bytecode = True
SCRIPT = Path(__file__).resolve().parents[1] / "scripts/cycle.py"
spec = importlib.util.spec_from_file_location("cycle_helper", SCRIPT)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)


class MissingScratchTests(unittest.TestCase):
    def test_missing_mount_refuses_before_creating_output(self):
        # No test-only CLI override: substitute an actual non-mount directory.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            with patch.object(helper, "SCRATCH", root):
                with self.assertRaisesRegex(ValueError, "must be mounted"):
                    helper.main(["start", "must-not-exist"])
            self.assertEqual(list(root.iterdir()), [])


@unittest.skipUnless(sys.platform == "darwin" and Path("/Volumes/Scratch").is_mount(),
                     "requires macOS and mounted Scratch; never substitutes internal disk")
class CycleTests(unittest.TestCase):
    def setUp(self):
        self.name = "test-" + uuid.uuid4().hex
        self.invoke("start")
        self.cycle = helper.Cycle(self.name)
        self.addCleanup(self.finish)

    def invoke(self, action, *arguments, cwd=None, code=0):
        env = dict(os.environ)
        env.pop("CARGO_INCREMENTAL", None)
        result = subprocess.run([sys.executable, "-B", str(SCRIPT), action, self.name, *arguments],
                                cwd=cwd, env=env, capture_output=True, text=True, timeout=90)
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return result

    def finish(self):
        # Leave compact real receipts for inspection; reclaim only owned output.
        self.invoke("final", "--evidence-saved")

    def checked_main(self, *arguments):
        with redirect_stdout(io.StringIO()):
            return helper.main(list(arguments))

    def test_reused_target_failure_cleanup_and_final_preserve_evidence(self):
        for index, exit_code in enumerate((0, 23)):
            cwd = self.cycle.archive / f"worktree-fixture-{index}"
            cwd.mkdir()
            command = "\n".join([
                "import json, os, pathlib, sys",
                "target = pathlib.Path(os.environ['CARGO_TARGET_DIR'])",
                "tmp = pathlib.Path(os.environ['TMPDIR'])",
                "assert str(tmp) == os.environ['TMP'] == os.environ['TEMP']",
                "assert os.environ['CARGO_INCREMENTAL'] == '0'",
                f"(target / 'artifact-{index}').write_text('build fixture')",
                "(tmp / 'disposable').write_text('remove on success or failure')",
                f"(pathlib.Path(os.environ['CODEXNK_EVIDENCE_DIR']) / 'proof-{index}.json').write_text(json.dumps(dict(target=str(target), cwd=os.getcwd())))",
                f"sys.exit({exit_code})",
            ])
            self.invoke("run", "--", sys.executable, "-c", command, cwd=cwd, code=exit_code)
            self.assertEqual(list(self.cycle.tmp.iterdir()), [])
        proofs = [json.loads((self.cycle.archive / f"proof-{i}.json").read_text()) for i in (0, 1)]
        self.assertEqual(proofs[0]["target"], proofs[1]["target"])
        self.assertNotEqual(proofs[0]["cwd"], proofs[1]["cwd"])
        receipts = [json.loads(path.read_text()) for path in self.cycle.archive.glob("*-run.json")]
        self.assertEqual(sorted(r["exit_code"] for r in receipts), [0, 23])
        self.assertTrue(all(r["cleanup_error"] is None for r in receipts))
        # An interruption may leave tmp output: checkpoint recovers it, retaining cache.
        (self.cycle.tmp / "abandoned-tmp").write_text("interrupted fixture")
        self.invoke("checkpoint")
        self.assertEqual(list(self.cycle.tmp.iterdir()), [])
        self.assertEqual(len(list(self.cycle.target.iterdir())), 2)
        self.invoke("checkpoint", "--clean")
        self.assertEqual(list(self.cycle.target.iterdir()), [])
        (self.cycle.target / "last-build").write_text("final output")
        self.invoke("final", "--evidence-saved")
        self.assertEqual(list(self.cycle.target.iterdir()), [])
        self.assertEqual(json.loads((self.cycle.archive / "proof-0.json").read_text()), proofs[0])
        self.assertIn("cycle is final", self.invoke("run", "--", "/usr/bin/true", code=1).stderr)

    def test_cleanup_refuses_replaced_scope_and_symlink_escape(self):
        sentinel = self.cycle.archive / "untracked-evidence"
        sentinel.write_text("must survive")
        artifact = self.cycle.target / "owned-output"
        artifact.write_text("preserve on refusal")
        original = self.cycle.root / "target-original"
        self.cycle.target.rename(original)
        try:
            # Even an ordinary replacement directory at the same path is not adopted.
            self.cycle.target.mkdir()
            try:
                self.assertIn("ownership receipt", self.invoke("checkpoint", "--clean", code=1).stderr)
            finally:
                self.cycle.target.rmdir()
            self.cycle.target.symlink_to(self.cycle.archive, target_is_directory=True)
            try:
                self.assertIn("redirected path", self.invoke("final", "--evidence-saved", code=1).stderr)
            finally:
                self.cycle.target.unlink()
        finally:
            original.rename(self.cycle.target)
        link = self.cycle.target / "escape"
        link.symlink_to(self.cycle.archive, target_is_directory=True)
        try:
            self.assertIn("redirected/foreign", self.invoke("checkpoint", "--clean", code=1).stderr)
            self.assertEqual(artifact.read_text(), "preserve on refusal")
            self.assertEqual(sentinel.read_text(), "must survive")
        finally:
            link.unlink()
        receipt = self.cycle.root / "owner.json"
        saved = receipt.read_bytes()
        receipt.write_text("{}")
        try:
            self.assertIn("ownership receipt", self.invoke("final", "--evidence-saved", code=1).stderr)
            self.assertTrue(artifact.exists())
        finally:
            receipt.write_bytes(saved)

    def test_live_output_lock_and_unavailable_inspection_block_cleanup(self):
        artifact = self.cycle.target / "live-output"
        artifact.write_text("keep")
        with artifact.open() as opened:
            self.assertIn("live/open build output", self.invoke("checkpoint", "--clean", code=1).stderr)
            self.assertEqual(opened.read(), "keep")
        with self.cycle.lock.open("r+") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.assertIn("cycle is active", self.invoke("final", "--evidence-saved", code=1).stderr)
        # Exercise unavailable and incomplete OS observations at the command boundary.
        failures = [FileNotFoundError("lsof missing"),
                    subprocess.CompletedProcess([], 1, b"", b""),
                    subprocess.CompletedProcess([], 0, b"p123\0", b"partial inspection warning")]
        for result in failures:
            with self.subTest(result=result):
                options = {"side_effect": result} if isinstance(result, Exception) else {"return_value": result}
                with patch.object(helper.subprocess, "run", **options):
                    with self.assertRaises((OSError, ValueError)):
                        self.checked_main("checkpoint", self.name, "--clean")
                self.assertEqual(artifact.read_text(), "keep")


if __name__ == "__main__":
    unittest.main()
