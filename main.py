"""Emit the 18 November 2026 world-news front page as /output/entry.png.

The finished picture lives in this repository as entry.png (1024x1024,
under 1 MiB). This program does the only thing the competition needs:
copy that file to the grader's output directory, byte for byte, with
no network access and no randomness.

Front page, v7: 38 stories from 6 continents, 11 of them illustrated
on the front (3 hero + 8 card flat-vector pictures), a world map with
numbered pins and a legend, four big numbers, a 27-item also-strip
and a DATE CHECK box naming Tuesday's news as left out, in the
structure of the entry leading the live leaderboard for this day.

Run it locally the same way the grader does, with an output directory
of your own:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

A missing source, an empty source, or a copy that does not match the
source byte for byte is a loud failure (exit 1), never a partial entry.
"""

# v7 entry (2026-11-19): eleven flat-vector pictures, leader's front 11.
import hashlib
import os
import shutil
import sys
from pathlib import Path

SOURCE = Path(__file__).resolve().parent / "entry.png"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run():
    if not SOURCE.is_file():
        print(f"missing source: {SOURCE}", file=sys.stderr)
        return 1
    if SOURCE.stat().st_size == 0:
        print(f"empty source: {SOURCE}", file=sys.stderr)
        return 1
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.png"
    shutil.copyfile(SOURCE, target)
    if sha256_of(SOURCE) != sha256_of(target):
        print("copy differs from source", file=sys.stderr)
        return 1
    print(f"wrote {target} ({target.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
