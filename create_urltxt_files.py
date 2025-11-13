#!/usr/bin/env python3
"""
Script to create .urltxt files for all songs that have recordings in VideoIndex History.html
"""

import re
import os
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import unquote
import datetime

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
    """Parse VideoIndex History.html and extract song recordings with dates"""
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
    
    # Dictionary to store song recordings: {song_title: [(date, youtube_url), ...]}
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
                
                # Extract song title
                song_cell = cells[2]
                song_link = song_cell.find('a')
                if song_link:
                    song_title = song_link.get_text().strip()
                else:
                    song_title = song_cell.get_text().strip()
                
                # Clean up song title for matching
                song_title = clean_song_title(song_title)
                
                if timestamp_link and song_title:
                    if song_title not in recordings:
                        recordings[song_title] = []
                    recordings[song_title].append((date_obj, current_date, timestamp_link))
    
    # Sort recordings by date (most recent first) for each song
    for song_title in recordings:
        recordings[song_title].sort(key=lambda x: x[0], reverse=True)
    
    return recordings

def clean_song_title(title):
    """Clean up song title for better matching"""
    # Remove common variations and normalize
    title = title.strip()
    
    # Remove file extensions if present
    title = re.sub(r'\.(pdf|chopro|cho)$', '', title, flags=re.IGNORECASE)
    
    # Remove version indicators
    title = re.sub(r'\s*\([^)]*\)\s*$', '', title)  # Remove trailing parentheses
    title = re.sub(r'\s*-\s*[^-]*$', '', title)     # Remove trailing dashes with text
    
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

def find_best_match(song_title, recordings):
    """Find the best matching recording for a song title"""
    song_title_clean = clean_song_title(song_title)
    
    # Try exact match first
    if song_title_clean in recordings:
        return recordings[song_title_clean][0]  # Most recent recording
    
    # Try fuzzy matching
    best_match = None
    best_score = 0
    
    for recorded_title in recordings:
        # Simple fuzzy matching - check if titles contain common words
        song_words = set(song_title_clean.split())
        recorded_words = set(recorded_title.split())
        
        if song_words and recorded_words:
            common_words = song_words.intersection(recorded_words)
            score = len(common_words) / max(len(song_words), len(recorded_words))
            
            if score > best_score and score > 0.5:  # At least 50% word overlap
                best_score = score
                best_match = recordings[recorded_title][0]
    
    return best_match

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
    
    created_count = 0
    updated_count = 0
    not_found_count = 0
    already_exists_count = 0
    
    print("Creating .urltxt files for songs with recordings...")
    
    for chopro_file in all_songs:
        urltxt_file = chopro_file.with_suffix('.urltxt')
        
        # Check if .urltxt already exists
        file_exists = urltxt_file.exists()
        
        # For existing files, we'll still process to check for newer recordings
        # but we'll track them separately
        
        # Extract song title from ChordPro file
        song_title = extract_title_from_chopro(chopro_file)
        if not song_title:
            print(f"WARNING: Could not extract title from: {chopro_file.name}")
            not_found_count += 1
            continue
        
        # Find matching recording
        match = find_best_match(song_title, recordings)
        
        if match:
            date_obj, date_str, youtube_url = match
            
            # Check if we should update an existing file
            should_update = True
            if file_exists:
                # Read existing file to check if it was created by script and if date is different
                try:
                    with open(urltxt_file, 'r', encoding='utf-8') as f:
                        first_line = f.readline().strip()
                        if "# Most recent recording:" in first_line:
                            # This file was created by the script, check if date is different
                            if f"# Most recent recording: {date_str}" in first_line:
                                # Same date, no need to update
                                should_update = False
                                already_exists_count += 1
                            # If different date, should_update remains True
                        else:
                            # This file was created manually, don't overwrite
                            should_update = False
                            already_exists_count += 1
                except Exception:
                    # If we can't read the file, don't update it (be safe)
                    should_update = False
                    already_exists_count += 1
            
            if should_update:
                if create_urltxt_file(chopro_file, youtube_url, date_str):
                    relative_path = chopro_file.relative_to(Path("music/ChordPro"))
                    if file_exists:
                        updated_count += 1
                        print(f"UPDATED: .urltxt for: {relative_path} -> {date_str}")
                    else:
                        created_count += 1
                        print(f"CREATED: .urltxt for: {relative_path} -> {date_str}")
                else:
                    not_found_count += 1
        else:
            not_found_count += 1
            # Only show first 20 "not found" messages to avoid spam
            if not_found_count <= 20:
                relative_path = chopro_file.relative_to(Path("music/ChordPro"))
                print(f"NOT FOUND: No recording for: {relative_path} (title: '{song_title}')")
            elif not_found_count == 21:
                print(f"... (showing only first 20 'not found' messages)")
    
    # Summary report
    print(f"\nSUMMARY:")
    print(f"ChordPro files processed: {len(all_songs)}")
    print(f"New .urltxt files created: {created_count}")
    print(f"Existing .urltxt files updated: {updated_count}")
    print(f"Already up-to-date .urltxt files: {already_exists_count}")
    print(f"Songs without recordings: {not_found_count}")
    
    # Show success rate
    total_with_recordings = created_count + updated_count + already_exists_count
    if len(all_songs) > 0:
        success_rate = (total_with_recordings / len(all_songs)) * 100
        print(f"Songs with video recordings: {total_with_recordings}/{len(all_songs)} ({success_rate:.1f}%)")
    
    if not_found_count > 0:
        print(f"\nTIP: Songs without recordings may need manual review.")
        print(f"Check if song titles in ChordPro files match those in VideoIndex History.html")

if __name__ == "__main__":
    main()
