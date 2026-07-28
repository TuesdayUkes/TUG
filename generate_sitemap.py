#!/usr/bin/env python3
"""Generate sitemap.xml for the public Tuesday Ukes site."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from html.parser import HTMLParser
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit


BASE_URL = "https://tuesdayukes.org"
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_OUTPUT = SCRIPT_DIR / "sitemap.xml"
SITEMAP_TYPE_ORDER = ("html", "pdf", "chopro")
RESOURCE_TYPES = {
    ".pdf": "pdf",
    ".chopro": "chopro",
}

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
    "_site",
    "__pycache__",
    "docs",
    "music/ChordPro",
}


class LinkExtractor(HTMLParser):
    """Collect href attribute values from anchor tags."""

    def __init__(self) -> None:
        super().__init__()
        self.links: list[HtmlLink] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag != "a":
            return

        href = None
        css_classes: set[str] = set()

        for attr_name, attr_value in attrs:
            if attr_name == "href" and attr_value:
                href = attr_value
            elif attr_name == "class" and attr_value:
                css_classes = set(attr_value.split())

        if href:
            self.links.append(HtmlLink(href=href, css_classes=css_classes))


@dataclass(frozen=True)
class HtmlLink:
    href: str
    css_classes: set[str]


@dataclass(frozen=True)
class SitemapEntry:
    url: str
    lastmod: str
    resource_type: str


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


def resolve_internal_link(html_path: Path, href: str) -> Path | None:
    parsed = urlsplit(href)

    if parsed.scheme or parsed.netloc:
        return None

    decoded_path = Path(unquote(parsed.path.lstrip("/")))
    if parsed.path.startswith("/"):
        candidate = (SCRIPT_DIR / decoded_path).resolve()
    else:
        candidate = (html_path.parent / decoded_path).resolve()

    try:
        candidate.relative_to(SCRIPT_DIR)
    except ValueError:
        return None

    if not candidate.is_file():
        return None

    return candidate


def resource_group_key(path: Path, resource_type: str) -> str:
    if resource_type == "pdf":
        return path.stem.casefold()

    return path.relative_to(SCRIPT_DIR).as_posix().lower()


def resource_preference(path: Path, resource_type: str) -> tuple[int, str]:
    relative_path = path.relative_to(SCRIPT_DIR).as_posix().lower()

    if resource_type == "pdf":
        if relative_path.startswith("music/chordpro/"):
            return (0, relative_path)
        if relative_path.startswith("music/pdfs/"):
            return (1, relative_path)

    return (2, relative_path)


def iter_internal_resource_files() -> dict[str, list[Path]]:
    resource_files: dict[str, dict[str, Path]] = {
        resource_type: {} for resource_type in RESOURCE_TYPES.values()
    }

    for html_path in iter_public_html_files():
        extractor = LinkExtractor()
        extractor.feed(html_path.read_text(encoding="utf-8"))

        for link in extractor.links:
            candidate = resolve_internal_link(html_path, link.href)
            if candidate is None:
                continue

            extension = candidate.suffix.lower()
            resource_type = RESOURCE_TYPES.get(extension)
            if resource_type is None:
                continue

            if resource_type == "pdf" and "additional-version" in link.css_classes:
                continue

            group_key = resource_group_key(candidate, resource_type)
            existing = resource_files[resource_type].get(group_key)

            if existing is None:
                resource_files[resource_type][group_key] = candidate
                continue

            if resource_preference(candidate, resource_type) < resource_preference(existing, resource_type):
                resource_files[resource_type][group_key] = candidate

    return {
        resource_type: sorted(
            files.values(),
            key=lambda path: path.relative_to(SCRIPT_DIR).as_posix().lower(),
        )
        for resource_type, files in resource_files.items()
    }


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


def collect_sitemap_entries() -> list[SitemapEntry]:
    entries: list[SitemapEntry] = []

    for path in iter_public_html_files():
        entries.append(
            SitemapEntry(
                url=build_url(path),
                lastmod=last_modified_date(path),
                resource_type="html",
            )
        )

    resource_files = iter_internal_resource_files()
    for resource_type in ("pdf", "chopro"):
        for path in resource_files[resource_type]:
            entries.append(
                SitemapEntry(
                    url=build_url(path),
                    lastmod=last_modified_date(path),
                    resource_type=resource_type,
                )
            )

    return entries


def split_entries_by_type(entries: list[SitemapEntry]) -> dict[str, list[SitemapEntry]]:
    grouped_entries = {resource_type: [] for resource_type in SITEMAP_TYPE_ORDER}

    for entry in entries:
        grouped_entries[entry.resource_type].append(entry)

    return grouped_entries


def build_urlset_content(entries: list[SitemapEntry]) -> str:
    url_entries = []

    for entry in entries:
        url_entries.append(
            "  <url>\n"
            f"    <loc>{entry.url}</loc>\n"
            f"    <lastmod>{entry.lastmod}</lastmod>\n"
            "  </url>"
        )

    return "\n".join([
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        *url_entries,
        '</urlset>',
        '',
    ])


def child_sitemap_name(index_output_path: Path, resource_type: str) -> str:
    return f"{index_output_path.stem}-{resource_type}.xml"


def child_sitemap_url(index_output_path: Path, resource_type: str) -> str:
    return f"{BASE_URL}/{quote(child_sitemap_name(index_output_path, resource_type))}"


def build_sitemap_index_content(grouped_entries: dict[str, list[SitemapEntry]], index_output_path: Path) -> str:
    sitemap_entries = []

    for resource_type in SITEMAP_TYPE_ORDER:
        entries = grouped_entries[resource_type]
        if not entries:
            continue

        sitemap_entries.append(
            "  <sitemap>\n"
            f"    <loc>{child_sitemap_url(index_output_path, resource_type)}</loc>\n"
            f"    <lastmod>{max(entry.lastmod for entry in entries)}</lastmod>\n"
            "  </sitemap>"
        )

    return "\n".join([
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        *sitemap_entries,
        '</sitemapindex>',
        '',
    ])


def build_sitemap_files(index_output_path: Path) -> tuple[dict[Path, str], list[SitemapEntry]]:
    sitemap_entries = collect_sitemap_entries()
    grouped_entries = split_entries_by_type(sitemap_entries)
    sitemap_files: dict[Path, str] = {}

    for resource_type in SITEMAP_TYPE_ORDER:
        entries = grouped_entries[resource_type]
        if not entries:
            continue

        sitemap_files[index_output_path.parent / child_sitemap_name(index_output_path, resource_type)] = build_urlset_content(entries)

    sitemap_files[index_output_path] = build_sitemap_index_content(grouped_entries, index_output_path)

    return sitemap_files, sitemap_entries


def build_summary(entries: list[SitemapEntry]) -> dict[str, int]:
    summary = {
        "html": 0,
        "pdf": 0,
        "chopro": 0,
        "total": len(entries),
    }

    for entry in entries:
        summary[entry.resource_type] += 1

    return summary


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
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Print only HTML/PDF/ChordPro counts instead of every URL",
    )
    args = parser.parse_args()

    output_path = Path(args.output)
    sitemap_files, sitemap_entries = build_sitemap_files(output_path)
    summary = build_summary(sitemap_entries)

    if args.summary:
        print(f"HTML COUNT {summary['html']}")
        print(f"PDF COUNT {summary['pdf']}")
        print(f"CHOPRO COUNT {summary['chopro']}")
        print(f"SITEMAP FILE COUNT {len(sitemap_files)}")
    else:
        for entry in sitemap_entries:
            print(entry.url)

    print(f"TOTAL URLS {summary['total']}")

    if args.dry_run:
        return 0

    for file_path, content in sitemap_files.items():
        file_path.write_text(content, encoding="utf-8")
        print(f"Wrote {file_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
