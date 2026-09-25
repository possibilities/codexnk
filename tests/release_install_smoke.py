#!/usr/bin/env python3
"""Install one published release privately and exercise code-mode in a Bot cwd."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tag", required=True)
    parser.add_argument("--sha", required=True)
    parser.add_argument("--cwd", type=Path, required=True)
    args = parser.parse_args()
    workshop = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix="codexnk-release-smoke-") as temporary:
        root = Path(temporary) / "installed"
        env = {**os.environ, "CODEXNK_INSTALL_ROOT": str(root),
               "PYTHONDONTWRITEBYTECODE": "1"}
        subprocess.run([sys.executable, str(workshop / "scripts/install.py"),
                        "--install", "--tag", args.tag, "--sha", args.sha],
                       env=env, check=True, timeout=600)
        binary = (root / "codex").resolve(strict=True)
        receipt = json.loads((binary.parent.parent / "receipt.json").read_text())
        if receipt["tag"] != args.tag or receipt["commit"] != args.sha:
            raise RuntimeError("isolated install receipt does not match requested pin")
        subprocess.run([sys.executable, str(workshop / "tests/code_mode_smoke.py"),
                        "--bin", str(root / "codex"), "--cwd", str(args.cwd)],
                       env=env, check=True, timeout=180)
        print(f"Isolated release receipt owns {len(receipt['files_sha256'])} files at {binary.parent.parent}")


if __name__ == "__main__":
    main()
