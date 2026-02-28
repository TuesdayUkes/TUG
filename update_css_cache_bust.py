#!/usr/bin/env python3
"""
Update cache-busting v= params for main.css links in HTML/PHP files.
"""

import argparse
import re
import subprocess
from datetime import datetime
from pathlib import Path

IGNORE_DIRS = {".git", ".venv", "__pycache__"}
DEFAULT_EXTENSIONS = {".html", ".php"}


def generate_timestamp():
    return datetime.now().strftime("%Y.%m.%d.%H.%M.%S")


def is_ignored_by_git(path, repo_root):
    try:
        result = subprocess.run(
            ["git", "check-ignore", "-q", path.as_posix()],
            cwd=repo_root,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except OSError:
        return False

    return result.returncode == 0


def iter_target_files(root, extensions):
    for path in root.rglob("*"):
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in extensions:
            if is_ignored_by_git(path.relative_to(root), root):
                continue
            yield path


def update_content(content, new_version):
    pattern = re.compile(
        r"(href=)([\"'])([^\"']*?main\.css\?v=)([^\"']*)(\2)",
        re.IGNORECASE,
    )

    def replace(match):
        return f"{match.group(1)}{match.group(2)}{match.group(3)}{new_version}{match.group(2)}"

    return pattern.subn(replace, content)


def update_file(path, new_version, dry_run):
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        content = path.read_text(encoding="iso-8859-1")

    updated_content, count = update_content(content, new_version)
    if count == 0:
        return 0

    if not dry_run:
        path.write_text(updated_content, encoding="utf-8")

    return count


def main():
    parser = argparse.ArgumentParser(
        description="Update cache-busting v= params for main.css links"
    )
    parser.add_argument(
        "--root",
        default=Path(__file__).resolve().parent,
        type=Path,
        help="Repository root to scan",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would change without writing files",
    )
    parser.add_argument(
        "--print-changed",
        action="store_true",
        help="Print changed file paths only",
    )

    args = parser.parse_args()
    root = args.root.resolve()
    new_version = generate_timestamp()

    changed_files = []
    total_updates = 0

    for path in iter_target_files(root, DEFAULT_EXTENSIONS):
        count = update_file(path, new_version, args.dry_run)
        if count:
            total_updates += count
            changed_files.append(path.relative_to(root).as_posix())

    if args.print_changed:
        for changed in changed_files:
            print(changed)
        return 0

    if total_updates == 0:
        print("No main.css cache-busting params found to update.")
        return 0

    print(f"Updated main.css cache-busting params to {new_version}.")
    for changed in changed_files:
        print(f"  {changed}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
