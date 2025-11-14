#!/usr/bin/env python3
"""
Script to create .urltxt files for all songs that have recordings in VideoIndex History.html
"""

import re
from pathlib import Path
from bs4 import BeautifulSoup
import datetime
from urllib.parse import unquote

def get_all_songs():
    """Find all ChordPro files in the music directory"""
    chopro_dir = Path("music/ChordPro")
    
    if not chopro_dir.exists():
        print(f"ChordPro directory not found: {chopro_dir}")
        return []
    
    # Find all .chopro files
    chopro_files = list(chopro_dir.rglob("*.chopro"))
    print(f"Found {len(chopro_files)} ChordPro files")
    
    return chopro_files

def parse_video_index():
    """Parse VideoIndex History.html and extract song recordings with dates.

    IMPORTANT: Keys are the exact PDF/ChordPro filename stems (lowercased),
    derived from the href of the song link in the history HTML. This enables
    strict, case-insensitive filename matching and avoids fuzzy matches.
    """
    video_index_path = Path("music/scripts/VideoIndex History.html")
    
    if not video_index_path.exists():
        print(f"VideoIndex History.html not found: {video_index_path}")
        return {}
    
    try:
        with open(video_index_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading VideoIndex History.html: {e}")
        return {}
    
    soup = BeautifulSoup(content, 'html.parser')
    
    # Dictionary to store song recordings keyed by filename stem (lowercased):
    # {filename_stem_lower: [(date_obj, original_date_str, youtube_url), ...]}
    recordings = {}
    current_date = None
    
    # Parse through the HTML structure
    for element in soup.find_all(['h2', 'tr']):
        if element.name == 'h2':
            # This is a date header
            current_date = element.get_text().strip()
            # Parse date to ensure we can sort chronologically
            try:
                # Convert "November 4, 2025" to datetime object for sorting
                date_obj = datetime.datetime.strptime(current_date, "%B %d, %Y")
            except:
                date_obj = datetime.datetime.min  # fallback for unparseable dates
                
        elif element.name == 'tr' and current_date:
            # This is a table row with song data
            cells = element.find_all('td')
            if len(cells) >= 3:
                # Extract timestamp link
                timestamp_link = None
                timestamp_cell = cells[0]
                link = timestamp_cell.find('a')
                if link and link.get('href'):
                    timestamp_link = link.get('href')
                
                # Extract song link and derive exact filename stem (lowercased)
                song_cell = cells[2]
                song_link = song_cell.find('a')
                filename_key = None
                if song_link:
                    href = song_link.get('href', '').strip()
                    if href:
                        # 1) strip query/fragment
                        href_clean = re.sub(r'[?#].*$', '', href)
                        # 2) get last path component
                        href_base = href_clean.split('/')[-1]
                        # 3) URL-decode and drop extension
                        href_base = unquote(href_base)
                        href_base = re.sub(r'\.(pdf|chopro|cho)$', '', href_base, flags=re.IGNORECASE)
                        # 4) Use exact base (except case) as key
                        filename_key = href_base.strip().lower()

                # Only record entries that have a resolvable filename key and timestamp
                if timestamp_link and filename_key:
                    if filename_key not in recordings:
                        recordings[filename_key] = []
                    recordings[filename_key].append((date_obj, current_date, timestamp_link))
    
    # Sort recordings by date (most recent first) for each song
    for key in recordings:
        recordings[key].sort(key=lambda x: x[0], reverse=True)
    
    return recordings

def clean_song_title(title):
    """Clean up song title for better matching"""
    # Remove common variations and normalize
    title = title.strip()
    
    # Remove file extensions if present
    title = re.sub(r'\.(pdf|chopro|cho)$', '', title, flags=re.IGNORECASE)
    
    # Remove version indicators (keep artist/qualifiers that help disambiguate)
    # Remove trailing parenthetical qualifiers like (Live) but keep meaningful words when inside the name
    title = re.sub(r'\s*\((live|version|easy|easier|scroll|inline|with.*|in [A-G][b#]?|key .*?)\)\s*$', '', title, flags=re.IGNORECASE)
    # Do NOT strip trailing "- Artist" style qualifiers; they disambiguate similar song names
    
    # Normalize whitespace
    title = re.sub(r'\s+', ' ', title).strip()
    
    # Convert to lowercase for comparison
    return title.lower()

def extract_title_from_chopro(chopro_file):
    """Extract song title from ChordPro file"""
    try:
        with open(chopro_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        return None
    
    # Look for {title:} or {t:} directive
    title_match = re.search(r'\{(?:title|t):\s*([^}]+)\}', content, re.IGNORECASE)
    if title_match:
        title = title_match.group(1).strip()
        return clean_song_title(title)
    
    # Fallback to filename
    return clean_song_title(chopro_file.stem)

def find_best_match(song_title, recordings, hint_title=None):
    """Find a matching recording strictly by filename stem (case-insensitive).

    We match ONLY when the filename stem from the ChordPro/PDF exactly equals
    the filename stem derived from the history HTML href (ignoring case).
    """
    # Prefer hint_title as the filename stem; fall back to song_title
    key = (hint_title or song_title or '').strip().lower()
    if not key:
        return None
    if key in recordings:
        return recordings[key][0]  # Most recent recording for this filename key
    return None

def create_urltxt_file(chopro_file, youtube_url, date_str):
    """Create a .urltxt file for the given ChordPro file"""
    urltxt_file = chopro_file.with_suffix('.urltxt')
    
    try:
        with open(urltxt_file, 'w', encoding='utf-8') as f:
            f.write(f"# Most recent recording: {date_str}\n")
            f.write(f"{youtube_url}\n")
        return True
    except Exception as e:
        print(f"Error creating {urltxt_file}: {e}")
        return False

def get_season_priority(folder_path):
    """Return priority for keeping files (lower = higher priority)"""
    folder_name = str(folder_path)
    # Prioritize 2025 first, then most recent years
    if '2025' in folder_name:
        return 0
    elif 'Fall 2024' in folder_name or 'Summer 2024' in folder_name:
        return 1
    elif '2024' in folder_name:
        return 2
    elif '2023' in folder_name:
        return 3
    elif '2022' in folder_name:
        return 4
    elif '2021' in folder_name:
        return 5
    elif '2020' in folder_name:
        return 6
    elif "Kevin's Memorial" in folder_name:
        return 7  # Keep memorial files
    elif 'TUG Archive' in folder_name:
        return 10  # Lower priority for archive
    else:
        return 8

def main():
    print("Finding all ChordPro songs...")
    all_songs = get_all_songs()
    print(f"Found {len(all_songs)} ChordPro files")

    if not all_songs:
        print("No ChordPro files found.")
        return

    print("Parsing VideoIndex History.html...")
    recordings = parse_video_index()
    print(f"Found recordings for {len(recordings)} different songs")

    if not recordings:
        print("No recordings found in VideoIndex History.html")
        return

    # Counters
    created_count = 0
    updated_count = 0
    not_found_count = 0
    removed_wrong_count = 0  # stale (no recording) script-managed removed
    already_exists_count = 0
    removed_title_duplicates = 0  # duplicates removed to enforce one per title

    print("Collecting candidate recordings per canonical title (enforcing ONE 'Most recent recording' per title)...")

    # Gather candidates keyed by canonical song title (case-insensitive)
    # title_key -> list of dicts {chopro_file, date_obj, date_str, youtube_url}
    title_candidates = {}

    for chopro_file in all_songs:
        song_title = extract_title_from_chopro(chopro_file)
        if not song_title:
            not_found_count += 1
            continue
        title_key = song_title.lower().strip()

        filename_hint = chopro_file.stem.lower()
        match = find_best_match(song_title, recordings, hint_title=filename_hint)
        if not match:
            # Handle stale script-managed file (no longer matches exactly)
            urltxt_file = chopro_file.with_suffix('.urltxt')
            if urltxt_file.exists():
                try:
                    with open(urltxt_file, 'r', encoding='utf-8') as f:
                        first_line = f.readline().strip()
                    if first_line.startswith('# Most recent recording:'):
                        try:
                            urltxt_file.unlink()
                            removed_wrong_count += 1
                            relative_path = chopro_file.relative_to(Path("music/ChordPro"))
                            print(f"REMOVED (stale): {relative_path} (no exact filename match in history)")
                        except Exception as de:
                            print(f"WARNING: Failed to remove {urltxt_file}: {de}")
                except Exception:
                    pass
            not_found_count += 1
            if not_found_count <= 20:
                relative_path = chopro_file.relative_to(Path("music/ChordPro"))
                print(f"NOT FOUND: No recording for: {relative_path} (title: '{song_title}')")
            elif not_found_count == 21:
                print("... (showing only first 20 'not found' messages)")
            continue

        date_obj, date_str, youtube_url = match
        title_candidates.setdefault(title_key, []).append({
            'chopro_file': chopro_file,
            'date_obj': date_obj,
            'date_str': date_str,
            'youtube_url': youtube_url
        })

    # Decide best candidate per title
    def candidate_sort_key(c):
        # Higher date first (descending), then season priority (lower better)
        date_obj = c['date_obj']
        # Use ordinal (robust); push pre-1970 fallback dates to bottom
        safe_ord = date_obj.toordinal() if date_obj.year >= 1970 else 0
        return (-safe_ord, get_season_priority(c['chopro_file'].parent))

    for title_key, candidates in title_candidates.items():
        # Sort candidates by (date desc, season priority asc)
        candidates.sort(key=candidate_sort_key)
        chosen = candidates[0]
        chosen_file = chosen['chopro_file']
        chosen_urltxt = chosen_file.with_suffix('.urltxt')
        file_exists = chosen_urltxt.exists()
        date_str = chosen['date_str']
        youtube_url = chosen['youtube_url']
        should_update = True

        if file_exists:
            try:
                with open(chosen_urltxt, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                if first_line.startswith('# Most recent recording:'):
                    if first_line == f"# Most recent recording: {date_str}":
                        should_update = False
                        already_exists_count += 1
                else:
                    # Manual file - preserve, do not overwrite
                    should_update = False
                    already_exists_count += 1
            except Exception:
                should_update = False
                already_exists_count += 1

        if should_update:
            if create_urltxt_file(chosen_file, youtube_url, date_str):
                relative_path = chosen_file.relative_to(Path("music/ChordPro"))
                if file_exists:
                    updated_count += 1
                    print(f"UPDATED (title winner): {relative_path} -> {date_str}")
                else:
                    created_count += 1
                    print(f"CREATED (title winner): {relative_path} -> {date_str}")
            else:
                not_found_count += 1

        # Remove other script-managed duplicates for this title
        for duplicate in candidates[1:]:
            dup_file = duplicate['chopro_file']
            dup_urltxt = dup_file.with_suffix('.urltxt')
            if dup_urltxt.exists():
                try:
                    with open(dup_urltxt, 'r', encoding='utf-8') as f:
                        first_line = f.readline().strip()
                    if first_line.startswith('# Most recent recording:'):
                        try:
                            dup_urltxt.unlink()
                            removed_title_duplicates += 1
                            relative_path = dup_file.relative_to(Path("music/ChordPro"))
                            print(f"REMOVED (duplicate title): {relative_path}")
                        except Exception as de:
                            print(f"WARNING: Failed to remove duplicate {dup_urltxt}: {de}")
                except Exception:
                    pass

    # Summary report
    print("\nSUMMARY:")
    print(f"ChordPro files processed: {len(all_songs)}")
    print(f"New .urltxt files created: {created_count}")
    print(f"Existing .urltxt files updated: {updated_count}")
    print(f"Already up-to-date .urltxt files: {already_exists_count}")
    print(f"Songs without recordings: {not_found_count}")
    if removed_wrong_count:
        print(f"Wrong .urltxt removed (no exact match): {removed_wrong_count}")
    if removed_title_duplicates:
        print(f"Title-level duplicate .urltxt removed: {removed_title_duplicates}")

    # Post-pass: ensure no lingering script-managed duplicates with identical header content
    post_pass_removed = 0
    header_pattern = re.compile(r'^# Most recent recording: (.+)$')
    urltxt_files = list(Path('music/ChordPro').rglob('*.urltxt'))
    duplicate_groups = {}
    for uf in urltxt_files:
        try:
            with open(uf, 'r', encoding='utf-8') as f:
                first_line = f.readline().strip()
            m = header_pattern.match(first_line)
            if not m:
                continue  # manual file; skip
            date_str = m.group(1).strip()
            # Title key inferred from sibling ChordPro filename if exists, else stem
            title_key = uf.stem.lower().strip()
            duplicate_groups.setdefault(title_key, []).append((uf, date_str))
        except Exception:
            continue

    for title_key, entries in duplicate_groups.items():
        if len(entries) <= 1:
            continue
        # Determine keeper: prefer one whose matching ChordPro file is in most recent season priority
        def entry_sort(e):
            urltxt_path, date_str = e
            chopro_path = urltxt_path.with_suffix('.chopro')
            priority = get_season_priority(chopro_path.parent)
            # Parse date for ordering (fallback minimal)
            try:
                date_obj = datetime.datetime.strptime(date_str, '%B %d, %Y')
            except Exception:
                date_obj = datetime.datetime(1970,1,1)
            return (-date_obj.toordinal(), priority)
        entries.sort(key=entry_sort)
        keeper = entries[0][0]
        for (dup_path, _) in entries[1:]:
            if dup_path == keeper:
                continue
            try:
                dup_path.unlink()
                post_pass_removed += 1
                rel = dup_path.relative_to(Path('music/ChordPro'))
                print(f"POST-PASS REMOVED duplicate: {rel}")
            except Exception as e:
                print(f"WARNING: Post-pass failed to remove {dup_path}: {e}")

    if post_pass_removed:
        print(f"Post-pass duplicate removals: {post_pass_removed}")

    total_with_recordings = created_count + updated_count + already_exists_count
    if len(all_songs) > 0:
        success_rate = (total_with_recordings / len(all_songs)) * 100
        print(f"Songs with video recordings: {total_with_recordings}/{len(all_songs)} ({success_rate:.1f}%)")

    if not_found_count > 0:
        print("\nTIP: Songs without recordings may need manual review.")
        print("Check if song titles in ChordPro files match those in VideoIndex History.html")

if __name__ == "__main__":
    main()
