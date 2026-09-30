#!/usr/bin/env python3
"""macOS-only, explicitly owned Scratch build lifecycle; see MAINTAIN.md."""
import argparse
from contextlib import contextmanager
import fcntl
import json
import os
from pathlib import Path
import re
import shutil
import signal
import stat
import subprocess
import sys
import time
import uuid

SCRATCH = Path("/Volumes/Scratch")
OWNER = "codexnk-cycle-v1"


def fail(message):
    raise ValueError(message)


def plain(path):
    if path.is_symlink() or path.resolve() != path:
        fail(f"redirected path refused: {path}")


def scratch_ready():
    if sys.platform != "darwin":
        fail("cycle helper requires macOS")
    plain(SCRATCH)
    if not SCRATCH.is_mount():
        fail("/Volumes/Scratch must be mounted; no internal-disk fallback")


def identity(path):
    plain(path)
    info = path.stat()
    if info.st_uid != os.getuid():
        fail(f"foreign owner: {path}")
    return [info.st_dev, info.st_ino]


def write_json(path, value):
    # Exclusive receipts: neither overwrite evidence nor follow an existing link.
    with path.open("x") as output:
        json.dump(value, output, indent=2)
        output.write("\n")


class Cycle:
    def __init__(self, name):
        if not re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,79}", name):
            fail("cycle must be 1..80 letters, digits, underscores or hyphens")
        scratch_ready()
        self.root = SCRATCH / "codexnk-cycles" / name
        self.archive = SCRATCH / "archive" / "codexnk-cycles" / name
        self.target = self.root / "target"
        self.tmp = self.root / "tmp"
        self.lock = self.root / "lock"

    def start(self):
        for path in (self.root, self.archive):
            plain(path)
            if path.exists():
                fail(f"cycle already exists; resume it or choose a new name: {path}")
        # Partial creation is intentionally preserved for inspection on failure.
        self.root.mkdir(parents=True, mode=0o700)
        self.archive.mkdir(parents=True, mode=0o700)
        self.target.mkdir(mode=0o700)
        self.tmp.mkdir(mode=0o700)
        self.lock.touch(mode=0o600, exist_ok=False)
        receipt = {"owner": OWNER, "uid": os.getuid(), "nonce": uuid.uuid4().hex,
                   "paths": {str(p): identity(p) for p in
                             (self.root, self.archive, self.target, self.tmp, self.lock)}}
        write_json(self.archive / "owner.json", receipt)
        write_json(self.root / "owner.json", receipt)
        self.record("start")
        self.show()

    def validate(self):
        scratch_ready()
        for path in (self.root, self.archive, self.target, self.tmp, self.lock,
                     self.root / "owner.json", self.archive / "owner.json"):
            plain(path)
        receipt = json.loads((self.root / "owner.json").read_text())
        archived = json.loads((self.archive / "owner.json").read_text())
        expected = {str(p): identity(p) for p in
                    (self.root, self.archive, self.target, self.tmp, self.lock)}
        if (receipt != archived or receipt.get("owner") != OWNER or
                receipt.get("uid") != os.getuid() or receipt.get("paths") != expected):
            fail("ownership receipt does not match exact cycle paths/inodes")
        for path in (self.root, self.archive, self.target, self.tmp):
            if not path.is_dir():
                fail(f"cycle directory replaced: {path}")
        info = self.lock.stat()
        if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
            fail("cycle lock is not a private regular file")

    @contextmanager
    def locked(self):
        self.validate()
        fd = os.open(self.lock, os.O_RDWR | os.O_NOFOLLOW)
        with os.fdopen(fd, "r+") as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                fail("cycle is active (another helper/command holds its lock)")
            self.validate()
            if [os.fstat(fd).st_dev, os.fstat(fd).st_ino] != identity(self.lock):
                fail("cycle lock changed during acquisition")
            yield fd

    def record(self, action, **details):
        write_json(self.archive / f"{time.time_ns()}-{action}.json",
                   {"action": action, "time": time.time(), **details})

    def show(self):
        print(json.dumps({"target": str(self.target), "tmp": str(self.tmp),
                          "evidence": str(self.archive)}))

    def idle(self):
        # One complete listing is cheaper than recursive lsof +D on a Cargo tree.
        # A failed/partial listing is never interpreted as "nothing is open".
        result = subprocess.run(["/usr/sbin/lsof", "-nP", "-F0pn"],
                                capture_output=True, timeout=60)
        if result.returncode != 0 or result.stderr or not result.stdout.startswith(b"p"):
            fail("activity inspection unavailable/incomplete; preserving output")
        pid = b"?"
        for field in result.stdout.split(b"\0"):
            field = field.lstrip(b"\n")
            if field.startswith(b"p"):
                pid = field[1:]
            elif field.startswith(b"n"):
                if field[1:] == os.fsencode(self.lock) and pid != str(os.getpid()).encode():
                    fail(f"live cycle command retains lock (pid {os.fsdecode(pid)})")
                for path in (self.target, self.tmp):
                    prefix = os.fsencode(path)
                    if field[1:] == prefix or field[1:].startswith(prefix + b"/"):
                        fail(f"live/open build output (pid {os.fsdecode(pid)}): {os.fsdecode(field[1:])}")

    def inventory(self, directory):
        # Reject *all* symlinks and nested mounts, including benign-looking ones.
        # This is not a general cleaner and never adopts a legacy target.
        size = 0
        device = directory.stat().st_dev
        pending = [directory]
        while pending:
            parent = pending.pop()
            with os.scandir(parent) as entries:
                for entry in entries:
                    info = entry.stat(follow_symlinks=False)
                    if (entry.is_symlink() or info.st_dev != device or
                            info.st_uid != os.getuid() or os.path.ismount(entry.path)):
                        fail(f"redirected/foreign output refused: {entry.path}")
                    if entry.is_dir(follow_symlinks=False):
                        pending.append(entry.path)
                    else:
                        size += info.st_size
        return size

    def cleanup(self, build=False):
        self.validate()
        paths = (self.target, self.tmp) if build else (self.tmp,)
        sizes = {str(path): self.inventory(path) for path in paths}
        self.idle()
        # Keep the exact owned directories/inodes, deleting only their contents.
        for path in paths:
            for item in path.iterdir():
                if item.is_symlink():
                    fail(f"output changed during cleanup: {item}")
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
        return sizes

    def run(self, command, lock_fd):
        if (self.archive / "final.json").exists():
            fail("cycle is final; start a new cycle")
        # Recover only an idle prior command's temporary output.
        self.cleanup()
        env = dict(os.environ, CARGO_TARGET_DIR=str(self.target),
                   CARGO_INCREMENTAL=os.environ.get("CARGO_INCREMENTAL", "0"),
                   TMPDIR=str(self.tmp), TMP=str(self.tmp), TEMP=str(self.tmp),
                   CODEXNK_EVIDENCE_DIR=str(self.archive))
        process = None
        code = None
        cleanup_error = None
        try:
            # The direct child retains the lock if the wrapper is interrupted.
            process = subprocess.Popen(command, env=env, pass_fds=(lock_fd,))
            code = process.wait()
        finally:
            try:
                if process is not None and process.poll() is None:
                    fail("command still running; preserve output and resume at checkpoint when idle")
                self.cleanup()
            except (OSError, ValueError, subprocess.SubprocessError) as error:
                cleanup_error = str(error)
            self.record("run", command=command, cwd=os.getcwd(), exit_code=code,
                        incremental=env["CARGO_INCREMENTAL"], cleanup_error=cleanup_error)
            if cleanup_error:
                fail(cleanup_error)
        return code if code >= 0 else 128 - code


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    for action in ("start", "run", "checkpoint", "final"):
        command = sub.add_parser(action)
        command.add_argument("cycle")
        if action == "run":
            command.add_argument("command", nargs=argparse.REMAINDER)
        if action == "checkpoint":
            command.add_argument("--clean", action="store_true",
                                 help="discard target cache at a phase boundary after saving evidence")
        if action == "final":
            command.add_argument("--evidence-saved", action="store_true", required=True,
                                 help="confirm useful evidence is already outside target/tmp")
    args = parser.parse_args(argv)
    cycle = Cycle(args.cycle)
    if args.action == "start":
        cycle.start()
        return 0
    with cycle.locked() as lock_fd:
        if args.action == "run":
            command = args.command
            if command[:1] == ["--"]:
                command = command[1:]
            if not command:
                fail("run requires -- COMMAND [ARG ...]")
            return cycle.run(command, lock_fd)
        clean = args.action == "final" or args.clean
        sizes = cycle.cleanup(build=clean)
        cycle.record(args.action, cleaned_bytes=sizes,
                     target_bytes=cycle.inventory(cycle.target))
        if args.action == "final" and not (cycle.archive / "final.json").exists():
            write_json(cycle.archive / "final.json", {"time": time.time(), "owner": OWNER})
        cycle.show()
    return 0


def interrupted(signum, frame):
    raise InterruptedError(f"interrupted by signal {signum}; check cycle activity before resuming")


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, interrupted)
    try:
        sys.exit(main())
    except (OSError, ValueError, subprocess.SubprocessError, KeyboardInterrupt) as error:
        print(f"cycle: {error or 'interrupted; resume at checkpoint when idle'}", file=sys.stderr)
        sys.exit(1)
