#!/usr/bin/env python3
import importlib.util
import io
import json
from pathlib import Path
import shutil
import tarfile
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("installer", Path(__file__).resolve().parents[1] / "scripts/install.py")
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)
TAG = "codexnk-v0.1.1"
SHA = "a" * 40
TARGET = "aarch64-apple-darwin"


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / "installed"
        self.archive = self.base / f"codex-{TARGET}.tar.gz"
        self.bundle([(f"codex-{TARGET}/codex", b"fake executable")])
        self.downloads = 0

    def bundle(self, entries):
        with tarfile.open(self.archive, "w:gz") as bundle:
            for name, content in entries:
                entry = tarfile.TarInfo(name)
                entry.size = len(content)
                bundle.addfile(entry, io.BytesIO(content))

    def fake_run(self, *args):
        if args[:2] == ("gh", "api"):
            return json.dumps({"object": {"type": "commit", "sha": SHA}})
        if args[:3] == ("gh", "release", "view"):
            return json.dumps({"isDraft": False, "isPrerelease": False, "assets": [{
                "name": self.archive.name, "state": "uploaded", "size": self.archive.stat().st_size,
                "digest": "sha256:" + installer.digest(self.archive)}]})
        if args[:3] == ("gh", "release", "download"):
            self.downloads += 1
            shutil.copyfile(self.archive, Path(args[-1]) / self.archive.name)
            return ""
        if args[1:] == ("--version",):
            return "codex-cli 0.test"
        if args[1:] == ("app-server", "--help"):
            return "--identity --capabilities --history-dir"
        raise AssertionError(args)

    def install(self):
        with patch.object(installer, "run", self.fake_run):
            installer.install(self.root, TAG, SHA, TARGET)

    def test_install_idempotence_and_receipt(self):
        self.install()
        original = (self.root / "codex").resolve()
        self.install()
        self.assertEqual(self.downloads, 1)
        self.assertEqual((self.root / "codex").resolve(), original)
        self.assertEqual(json.loads((original.parent / "receipt.json").read_text())["commit"], SHA)
        self.assertFalse((self.root / ".install-lock").exists())

    def test_tampered_binary_is_preserved(self):
        self.install()
        (self.root / "codex").write_text("independent edit")
        with self.assertRaisesRegex(ValueError, "ownership receipt"):
            self.install()
        self.assertEqual((self.root / "codex").read_text(), "independent edit")

    def test_foreign_link_and_file_are_preserved(self):
        self.root.mkdir()
        foreign = self.base / "foreign"
        foreign.write_text("keep")
        (self.root / "codex").symlink_to(foreign)
        with self.assertRaisesRegex(ValueError, "foreign"):
            self.install()
        self.assertEqual(foreign.read_text(), "keep")
        (self.root / "codex").unlink()
        (self.root / "codex").write_text("keep")
        with self.assertRaisesRegex(ValueError, "independent"):
            self.install()

    def test_wrong_tag_is_rejected_without_creating_root(self):
        with patch.object(installer, "run", self.fake_run), self.assertRaisesRegex(ValueError, "pinned"):
            installer.install(self.root, TAG, "b" * 40, TARGET)
        self.assertFalse(self.root.exists())

    def test_digest_mismatch_does_not_publish(self):
        original = self.fake_run
        def corrupted(*args):
            result = original(*args)
            if args[:3] == ("gh", "release", "download"):
                (Path(args[-1]) / self.archive.name).write_bytes(b"corrupt")
            return result
        with patch.object(installer, "run", corrupted), self.assertRaisesRegex(ValueError, "mismatch"):
            installer.install(self.root, TAG, SHA, TARGET)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_archive_escape_is_rejected(self):
        self.bundle([(f"codex-{TARGET}/codex", b"fake"), ("../escape", b"bad")])
        with self.assertRaisesRegex(ValueError, "unexpected archive"):
            self.install()
        self.assertFalse((self.base / "escape").exists())
        self.assertEqual(list(self.root.iterdir()), [])

    def test_missing_fork_contract_is_rejected(self):
        original = self.fake_run
        def stock(*args):
            return "stock help" if args[1:] == ("app-server", "--help") else original(*args)
        with patch.object(installer, "run", stock), self.assertRaisesRegex(ValueError, "invocation contract"):
            installer.install(self.root, TAG, SHA, TARGET)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_failed_upgrade_preserves_current_release(self):
        self.install()
        previous = (self.root / "codex").resolve()
        original = self.fake_run
        def corrupted(*args):
            result = original(*args)
            if args[:3] == ("gh", "release", "download"):
                (Path(args[-1]) / self.archive.name).write_bytes(b"corrupt")
            return result
        with patch.object(installer, "run", corrupted), self.assertRaisesRegex(ValueError, "mismatch"):
            installer.install(self.root, "codexnk-v0.1.2", SHA, TARGET)
        self.assertEqual((self.root / "codex").resolve(), previous)
        self.assertEqual(previous.read_bytes(), b"fake executable")
        self.assertFalse((self.root / ".install-lock").exists())

    def test_foreign_lock_is_not_removed(self):
        lock = self.root / ".install-lock"
        lock.mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, "another installation"):
            self.install()
        self.assertTrue(lock.is_dir())

    def test_redirected_install_root_is_not_adopted(self):
        foreign = self.base / "foreign"
        foreign.mkdir()
        self.root.symlink_to(foreign)
        with self.assertRaisesRegex(ValueError, "redirected install root"):
            self.install()
        self.assertEqual(list(foreign.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
