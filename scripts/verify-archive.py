#!/usr/bin/env python3
"""Verify one published codexnk runtime archive without executing its target binaries."""
import sys
import tempfile
from pathlib import Path

from install import digest, extract_package, package_files


def main():
    archive, target, tag = sys.argv[1:]
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        extract_package(Path(archive), root, target, tag)
        for file in package_files(target):
            print(f"{file} sha256:{digest(root / file)}")


if __name__ == "__main__":
    main()
