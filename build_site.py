#!/usr/bin/env python3
"""Build local site artifacts using the same generation path as CI."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent


def run_command(command: list[str], description: str) -> None:
    print(f"\n==> {description}")
    print(" ".join(command))
    subprocess.run(command, cwd=SCRIPT_DIR, check=True)


def copy_site_tree() -> None:
    site_dir = SCRIPT_DIR / "_site"
    if site_dir.exists():
        shutil.rmtree(site_dir)
    site_dir.mkdir()

    for entry in SCRIPT_DIR.iterdir():
        if entry.name in {".git", ".github", "_site", ".venv", "__pycache__"}:
            continue

        destination = site_dir / entry.name
        if entry.is_dir():
            shutil.copytree(entry, destination)
        else:
            shutil.copy2(entry, destination)

    print(f"\n==> Prepared site output in {site_dir}")


def main() -> int:
    run_command(
        [
            "genlist",
            "music",
            "ukulele-song-archive.html",
            "--intro",
            "--no-genPDF",
            "--no-html",
        ],
        "Generate ukulele-song-archive.html",
    )

    run_command(
        [
            "genlist",
            "music/XmasSongbook",
            "xmas-songbook.html",
            "--intro",
            "--no-genPDF",
            "--no-html",
        ],
        "Generate xmas-songbook.html",
    )

    run_command(
        ["python", "create_urltxt_files.py"],
        "Generate or update .urltxt files",
    )

    run_command(
        ["python", "generate_sitemap.py"],
        "Generate sitemap.xml",
    )

    copy_site_tree()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
