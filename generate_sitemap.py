#!/usr/bin/env python3
"""Generate sitemap.xml for the public Tuesday Ukes site."""

from __future__ import annotations

import argparse
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote


BASE_URL = "https://tuesdayukes.org"
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_OUTPUT = SCRIPT_DIR / "sitemap.xml"

# Exclude obvious non-canonical, test, or generated-internal HTML surfaces.
EXCLUDED_RELATIVE_PATHS = {
    Path("yt.php.html"),
    Path("music/scripts/testVideoIndex.html"),
    Path("music/scripts/ukulele-song-archive.html"),
}

EXCLUDED_PATH_PARTS = {
    ".git",
    ".github",
    ".venv",
    "__pycache__",
    "docs",
    "music/ChordPro",
}


def is_excluded(path: Path) -> bool:
    relative_path = path.relative_to(SCRIPT_DIR)
    relative_str = relative_path.as_posix()

    if relative_path in EXCLUDED_RELATIVE_PATHS:
        return True

    if relative_path.name.endswith(".backup"):
        return True

    return any(part in relative_str for part in EXCLUDED_PATH_PARTS)


def iter_public_html_files() -> list[Path]:
    html_files = []

    for path in SCRIPT_DIR.rglob("*.html"):
        if not path.is_file() or is_excluded(path):
            continue
        html_files.append(path)

    return sorted(html_files, key=lambda item: item.relative_to(SCRIPT_DIR).as_posix().lower())


def build_url(path: Path) -> str:
    relative_path = path.relative_to(SCRIPT_DIR).as_posix()

    if relative_path == "index.html":
        return f"{BASE_URL}/"

    if path.name == "index.html":
        parent = path.parent.relative_to(SCRIPT_DIR).as_posix()
        return f"{BASE_URL}/{quote(parent)}/"

    return f"{BASE_URL}/{quote(relative_path, safe='/')}"


def last_modified_date(path: Path) -> str:
    relative_path = path.relative_to(SCRIPT_DIR).as_posix()

    try:
        result = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", relative_path],
            cwd=SCRIPT_DIR,
            capture_output=True,
            text=True,
            check=True,
        )
        git_timestamp = result.stdout.strip()
        if git_timestamp:
            return datetime.fromisoformat(git_timestamp.replace("Z", "+00:00")).date().isoformat()
    except (OSError, subprocess.CalledProcessError, ValueError):
        pass

    timestamp = path.stat().st_mtime
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).date().isoformat()


def build_sitemap_content() -> tuple[str, list[str]]:
    urls = []
    entries = []

    for path in iter_public_html_files():
        url = build_url(path)
        urls.append(url)
        entries.append(
            "  <url>\n"
            f"    <loc>{url}</loc>\n"
            f"    <lastmod>{last_modified_date(path)}</lastmod>\n"
            "  </url>"
        )

    content = "\n".join([
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        *entries,
        '</urlset>',
        '',
    ])

    return content, urls


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate sitemap.xml for public site pages")
    parser.add_argument(
        "--output",
        "-o",
        default=str(DEFAULT_OUTPUT),
        help="Output sitemap path (default: sitemap.xml in repo root)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the discovered URLs without writing the sitemap file",
    )
    args = parser.parse_args()

    content, urls = build_sitemap_content()

    for url in urls:
        print(url)

    print(f"\nTotal URLs: {len(urls)}")

    if args.dry_run:
        return 0

    output_path = Path(args.output)
    output_path.write_text(content, encoding="utf-8")
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
