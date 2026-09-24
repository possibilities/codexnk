#!/usr/bin/env python3
"""Install one exact codexnk release without replacing vendor Codex."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import tarfile
import tempfile

REPOSITORY = "possibilities/codexnk-codex"
OWNER = "codexnk-release-v2"
LEGACY_OWNER = "codexnk-release-v1"


def package_files(target):
    files = ("bin/codex", "bin/codex-code-mode-host", "codex-package.json")
    if "linux" in target:
        files += ("codex-resources/bwrap",)
    return files


def package_metadata(target, tag):
    return {"layoutVersion": 1, "version": tag.removeprefix("codexnk-v"),
            "target": target, "variant": "codex", "entrypoint": "bin/codex",
            "resourcesDir": "codex-resources", "pathDir": "codex-path"}


def run(*args):
    return subprocess.check_output(args, text=True, timeout=600).strip()


def digest(path):
    with path.open("rb") as stream:
        checksum = hashlib.sha256()
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            checksum.update(chunk)
        return checksum.hexdigest()


def extract_package(archive, destination, target, tag):
    prefix = f"codex-{target}"
    files = package_files(target)
    expected = {f"{prefix}/{file}" for file in files}
    directories = {prefix, f"{prefix}/bin"}
    if "linux" in target:
        directories.add(f"{prefix}/codex-resources")
    with tarfile.open(archive, "r:gz") as bundle:
        members = bundle.getmembers()
        names = [entry.name for entry in members]
        if len(names) != len(set(names)) or not expected <= {entry.name for entry in members if entry.isfile()}:
            raise ValueError("release package has missing or duplicate required files")
        for entry in members:
            if entry.name in expected and entry.isfile():
                if not 0 < entry.size <= 2 * 1024**3:
                    raise ValueError(f"invalid package file size: {entry.name}")
                if entry.name != f"{prefix}/codex-package.json" and not entry.mode & 0o111:
                    raise ValueError(f"package file is not executable: {entry.name}")
                continue
            if entry.name.rstrip("/") in directories and entry.isdir():
                continue
            raise ValueError(f"unexpected archive member: {entry.name}")
        for file in files:
            member = bundle.getmember(f"{prefix}/{file}")
            path = destination / file
            path.parent.mkdir(parents=True, exist_ok=True)
            with bundle.extractfile(member) as source, path.open("xb") as output:
                shutil.copyfileobj(source, output)
            path.chmod(0o600 if file == "codex-package.json" else 0o755)
    if json.loads((destination / "codex-package.json").read_text()) != package_metadata(target, tag):
        raise ValueError("release package metadata does not match target and tag")


def verify_files(directory, target, files_sha256):
    if not isinstance(target, str) or not isinstance(files_sha256, dict) or set(files_sha256) != set(package_files(target)):
        raise ValueError("release receipt has incomplete package files")
    if any((directory / part).is_symlink() for part in ("bin", "codex-resources")):
        raise ValueError("release package has redirected directory")
    for file, checksum in files_sha256.items():
        path = directory / file
        if path.is_symlink() or not path.is_file() or not isinstance(checksum, str) or not re.fullmatch(r"[0-9a-f]{64}", checksum):
            raise ValueError(f"release package has missing or redirected file: {file}")
        if file != "codex-package.json" and not path.stat().st_mode & 0o111:
            raise ValueError(f"release package has non-executable file: {file}")
        if digest(path) != checksum:
            raise ValueError(f"release package file differs from ownership receipt: {file}")


def inspect_release(tag, sha):
    obj = json.loads(run("gh", "api", f"repos/{REPOSITORY}/git/ref/tags/{tag}"))["object"]
    if obj["type"] == "tag":
        obj = json.loads(run("gh", "api", f"repos/{REPOSITORY}/git/tags/{obj['sha']}"))["object"]
    if obj.get("type") != "commit" or obj.get("sha") != sha:
        raise ValueError("release tag does not match the pinned Integration commit")
    release = json.loads(run("gh", "release", "view", tag, "--repo", REPOSITORY,
                             "--json", "assets,isDraft,isPrerelease"))
    if release["isDraft"] or release["isPrerelease"]:
        raise ValueError("release is not a published stable release")
    return release


def install(root, tag, sha, target):
    release = inspect_release(tag, sha)
    name = f"codex-{target}.tar.gz"
    assets = [a for a in release["assets"] if a["name"] == name]
    if len(assets) != 1:
        raise ValueError(f"expected one published {name}")
    asset = assets[0]
    checksum = asset.get("digest", "")
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", checksum) or asset.get("state") != "uploaded":
        raise ValueError("release asset has no valid SHA-256 digest")
    if not isinstance(asset.get("size"), int) or not 0 < asset["size"] <= 1024**3:
        raise ValueError("invalid archive size")
    # This private directory is owned as a unit. Never adopt a foreign target.
    root.parent.mkdir(parents=True, exist_ok=True)
    if root.is_symlink():
        raise ValueError(f"refusing redirected install root: {root}")
    root.mkdir(mode=0o700, exist_ok=True)
    root = root.resolve()
    lock = root / ".install-lock"
    try:
        lock.mkdir(mode=0o700)
    except FileExistsError:
        raise ValueError(f"another installation owns {lock}; inspect before removing a stale lock")
    stage = None
    try:
        destination = root / f"{tag}-{sha}-{target}"
        link = root / "codex"
        if link.is_symlink():
            current = link.resolve()
            legacy = current.name == "codex" and current.parent.parent == root
            packaged = current.name == "codex" and current.parent.name == "bin" and current.parent.parent.parent == root
            release_dir = current.parent if legacy else current.parent.parent
            receipt_path = release_dir / "receipt.json"
            if not (legacy or packaged) or not receipt_path.is_file() or receipt_path.is_symlink():
                raise ValueError("refusing foreign codex link")
            receipt = json.loads(receipt_path.read_text())
            if legacy and receipt.get("owner") == LEGACY_OWNER and digest(current) == receipt.get("binary_sha256"):
                # The previous binary-only release is accepted solely as an upgrade source.
                pass
            elif packaged and receipt.get("owner") == OWNER and receipt.get("repository") == REPOSITORY:
                verify_files(release_dir, receipt.get("target"), receipt.get("files_sha256"))
                if json.loads((release_dir / "codex-package.json").read_text()) != package_metadata(receipt["target"], receipt["tag"]):
                    raise ValueError("installed package metadata differs from ownership receipt")
            else:
                raise ValueError("installed binary differs from its ownership receipt")
        elif link.exists():
            raise ValueError("refusing independent codex executable")
        expected = {"owner": OWNER, "repository": REPOSITORY, "tag": tag,
                    "commit": sha, "target": target, "archive_sha256": checksum[7:]}
        if destination.exists() or destination.is_symlink():
            if destination.is_symlink():
                raise ValueError("refusing redirected release directory")
            if (destination / "receipt.json").is_symlink():
                raise ValueError("refusing redirected release files")
            receipt = json.loads((destination / "receipt.json").read_text())
            if any(receipt.get(k) != v for k, v in expected.items()):
                raise ValueError("existing release differs from its receipt")
            verify_files(destination, target, receipt.get("files_sha256"))
            if json.loads((destination / "codex-package.json").read_text()) != package_metadata(target, tag):
                raise ValueError("existing release metadata differs from its receipt")
        else:
            stage = Path(tempfile.mkdtemp(prefix=".release-", dir=root))
            run("gh", "release", "download", tag, "--repo", REPOSITORY,
                "--pattern", name, "--dir", str(stage))
            archive = stage / name
            if archive.stat().st_size != asset["size"] or digest(archive) != checksum[7:]:
                raise ValueError("downloaded archive digest or size mismatch")
            extract_package(archive, stage, target, tag)
            binary = stage / "bin/codex"
            version = run(str(binary), "--version")
            help_text = run(str(binary), "app-server", "--help")
            if not version.startswith("codex-cli ") or not all(flag in help_text for flag in ("--identity", "--capabilities", "--history-dir")):
                raise ValueError("downloaded binary lacks the codexnk invocation contract")
            if "--listen" not in run(str(stage / "bin/codex-code-mode-host"), "--help"):
                raise ValueError("downloaded code-mode host lacks its runtime contract")
            archive.unlink()
            receipt_path = stage / "receipt.json"
            files_sha256 = {file: digest(stage / file) for file in package_files(target)}
            receipt_path.write_text(json.dumps({**expected, "files_sha256": files_sha256, "version": version}, indent=2) + "\n")
            receipt_path.chmod(0o600)
            stage.rename(destination)
            stage = None
        # A new link in the owned lock directory makes publication atomic.
        pending = lock / "codex"
        pending.symlink_to(destination / "bin/codex")
        pending.replace(link)
        print(f"Installed {tag} ({sha}) at {link}")
    finally:
        if stage is not None:
            shutil.rmtree(stage)
        shutil.rmtree(lock)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--install", action="store_true")
    modes.add_argument("--check", action="store_true")
    modes.add_argument("--print-bin", action="store_true")
    parser.add_argument("--tag")
    parser.add_argument("--sha")
    args = parser.parse_args()
    root = Path(os.environ.get("CODEXNK_INSTALL_ROOT", str(Path.home() / ".local/libexec/codexnk")))
    if not root.is_absolute():
        parser.error("CODEXNK_INSTALL_ROOT must be absolute")
    if args.install:
        if not re.fullmatch(r"codexnk-v\d+\.\d+\.\d+", args.tag or "") or not re.fullmatch(r"[0-9a-f]{40}", args.sha or ""):
            parser.error("--install requires --tag codexnk-vVERSION and --sha FULL_COMMIT")
        target = {("Darwin", "arm64"): "aarch64-apple-darwin",
                  ("Linux", "x86_64"): "x86_64-unknown-linux-gnu"}.get((platform.system(), platform.machine()))
        if not target:
            parser.error("no codexnk release target for this platform")
        install(root, args.tag, args.sha, target)
    elif args.tag or args.sha:
        parser.error("--tag and --sha apply only to --install")
    elif args.print_bin:
        print(root / "codex")
    else:
        print(f"Install a pinned codexnk GitHub Release into {root}; verify tag, archive digest, runtime package and receipt; atomically publish {root / 'codex'}. Vendor Codex remains installed separately.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, subprocess.SubprocessError, tarfile.TarError) as error:
        raise SystemExit(f"codexnk installer: {error}")
