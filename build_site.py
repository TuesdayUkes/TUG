#!/usr/bin/env python3
"""Build local site artifacts using the same generation path as CI."""

from __future__ import annotations

import os
import stat
import shutil
import subprocess
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent

# Directories that contain content intended for deployment.
PUBLISHABLE_ROOT_DIRS = {
    "amy",
    "assets",
    "includes",
    "music",
    "styles",
}

# File suffixes that are safe to publish from the repo root and subdirectories.
PUBLISHABLE_EXTENSIONS = {
    ".html",
    ".htm",
    ".css",
    ".js",
    ".json",
    ".xml",
    ".txt",
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".ico",
    ".webp",
    ".chopro",
    ".cho",
    ".chordpro",
    ".mscz",
    ".mp3",
    ".pptx",
    ".url",
    ".config",
}

SKIP_DIR_NAMES = {
    ".git",
    ".github",
    "_site",
    ".venv",
    "__pycache__",
    ".vscode",
    ".githooks",
    "docs",
    "tst",
}


def is_publishable_file(path: Path) -> bool:
    return path.suffix.lower() in PUBLISHABLE_EXTENSIONS


def ignore_unpublishable(_directory: str, names: list[str]) -> set[str]:
    ignored: set[str] = set()
    directory = Path(_directory)

    for name in names:
        candidate = directory / name
        if candidate.is_dir():
            if name in SKIP_DIR_NAMES or name.startswith("."):
                ignored.add(name)
            continue

        if not is_publishable_file(candidate):
            ignored.add(name)

    return ignored


def _remove_readonly(func, path, _excinfo) -> None:
    os.chmod(path, stat.S_IWRITE)
    func(path)


def run_command(command: list[str], description: str) -> None:
    print(f"\n==> {description}")
    print(" ".join(command))
    subprocess.run(command, cwd=SCRIPT_DIR, check=True)


def copy_site_tree() -> None:
    site_dir = SCRIPT_DIR / "_site"
    if site_dir.exists():
        shutil.rmtree(site_dir, onexc=_remove_readonly)
    site_dir.mkdir()

    for entry in SCRIPT_DIR.iterdir():
        if entry.name in SKIP_DIR_NAMES:
            continue

        if entry.is_dir() and entry.name not in PUBLISHABLE_ROOT_DIRS:
            continue

        if entry.is_file() and not is_publishable_file(entry):
            continue

        destination = site_dir / entry.name
        if entry.is_dir():
            shutil.copytree(entry, destination, ignore=ignore_unpublishable)
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
