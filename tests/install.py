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
TAG = "codexnk-v0.1.4"
SHA = "a" * 40
TARGET = "aarch64-apple-darwin"


class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.root = self.base / "installed"
        self.archive = self.base / f"codex-{TARGET}.tar.gz"
        self.bundle(self.package_entries())
        self.downloads = 0

    def package_entries(self, target=TARGET):
        return [(f"codex-{target}/bin/codex", b"fake executable"),
                (f"codex-{target}/bin/codex-code-mode-host", b"fake host"),
                (f"codex-{target}/codex-package.json",
                 (json.dumps(installer.package_metadata(target, TAG)) + "\n").encode())]

    def bundle(self, entries):
        with tarfile.open(self.archive, "w:gz") as bundle:
            for name, content in entries:
                entry = tarfile.TarInfo(name)
                entry.size = len(content)
                entry.mode = 0o644 if name.endswith(".json") else 0o755
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
        if args[1:] == ("--help",) and args[0].endswith("codex-code-mode-host"):
            return "--listen"
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
        receipt = json.loads((original.parent.parent / "receipt.json").read_text())
        self.assertEqual(receipt["commit"], SHA)
        self.assertEqual(set(receipt["files_sha256"]), set(installer.package_files(TARGET)))
        self.assertFalse((self.root / ".install-lock").exists())

    def test_tampered_binary_is_preserved(self):
        self.install()
        (self.root / "codex").write_text("independent edit")
        with self.assertRaisesRegex(ValueError, "ownership receipt"):
            self.install()
        self.assertEqual((self.root / "codex").read_text(), "independent edit")

    def test_missing_host_is_rejected(self):
        self.bundle([entry for entry in self.package_entries() if not entry[0].endswith("codex-code-mode-host")])
        with self.assertRaisesRegex(ValueError, "missing or duplicate required files"):
            self.install()
        self.assertEqual(list(self.root.iterdir()), [])

    def test_nonexecutable_host_is_rejected(self):
        entries = self.package_entries()
        with tarfile.open(self.archive, "w:gz") as bundle:
            for name, content in entries:
                entry = tarfile.TarInfo(name)
                entry.size = len(content)
                entry.mode = 0o644 if name.endswith("codex-code-mode-host") else 0o755
                bundle.addfile(entry, io.BytesIO(content))
        with self.assertRaisesRegex(ValueError, "not executable"):
            self.install()

    def test_host_runtime_contract_is_required(self):
        original = self.fake_run
        def stock(*args):
            return "other helper" if args[0].endswith("codex-code-mode-host") else original(*args)
        with patch.object(installer, "run", stock), self.assertRaisesRegex(ValueError, "runtime contract"):
            installer.install(self.root, TAG, SHA, TARGET)
        self.assertEqual(list(self.root.iterdir()), [])

    def test_tampered_or_missing_installed_host_is_rejected(self):
        self.install()
        host = (self.root / "codex").resolve().with_name("codex-code-mode-host")
        host.write_bytes(b"tampered")
        with self.assertRaisesRegex(ValueError, "ownership receipt"):
            self.install()
        host.unlink()
        with self.assertRaisesRegex(ValueError, "missing or redirected"):
            self.install()

    def test_package_metadata_must_match_tag(self):
        entries = self.package_entries()
        entries[-1] = (entries[-1][0], b'{}')
        self.bundle(entries)
        with self.assertRaisesRegex(ValueError, "metadata"):
            self.install()
        self.assertEqual(list(self.root.iterdir()), [])

    def test_linux_package_requires_bwrap(self):
        target = "x86_64-unknown-linux-gnu"
        self.archive = self.base / f"codex-{target}.tar.gz"
        self.bundle(self.package_entries(target))
        with patch.object(installer, "run", self.fake_run), self.assertRaisesRegex(ValueError, "missing or duplicate required files"):
            installer.install(self.root, TAG, SHA, target)
        self.assertEqual(list(self.root.iterdir()), [])

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
        self.bundle(self.package_entries() + [("../escape", b"bad")])
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
            installer.install(self.root, "codexnk-v0.1.5", SHA, TARGET)
        self.assertEqual((self.root / "codex").resolve(), previous)
        self.assertEqual(previous.read_bytes(), b"fake executable")
        self.assertFalse((self.root / ".install-lock").exists())

    def test_legacy_release_can_be_upgraded_but_not_reused(self):
        self.root.mkdir()
        previous = self.root / f"codexnk-v0.1.3-{'b' * 40}-{TARGET}"
        previous.mkdir()
        binary = previous / "codex"
        binary.write_bytes(b"old binary")
        (previous / "receipt.json").write_text(json.dumps({
            "owner": installer.LEGACY_OWNER, "binary_sha256": installer.digest(binary)}))
        (self.root / "codex").symlink_to(binary)
        self.install()
        self.assertEqual(binary.read_bytes(), b"old binary")
        self.assertEqual((self.root / "codex").resolve().parent.parent.name,
                         f"{TAG}-{SHA}-{TARGET}")

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
