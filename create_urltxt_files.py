#!/usr/bin/env python3
"""
Script to create .urltxt files for easy songs that point to their most recent recording 
in VideoIndex History.html
"""

import re
import os
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import unquote
import datetime

def get_easy_songs():
    """Find all ChordPro files that have .easy marker files"""
    chopro_dir = Path("music/ChordPro")
    
    if not chopro_dir.exists():
        print(f"ChordPro directory not found: {chopro_dir}")
        return []
    
    # Find all .easy files
    easy_files = list(chopro_dir.rglob("*.easy"))
    easy_songs = []
    
    for easy_file in easy_files:
        # Get the corresponding .chopro file
        chopro_file = easy_file.with_suffix('.chopro')
        if chopro_file.exists():
            easy_songs.append((chopro_file, easy_file))
    
    return easy_songs

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
    print("🔍 Finding easy songs...")
    easy_songs = get_easy_songs()
    print(f"Found {len(easy_songs)} songs with .easy markers")
    
    if not easy_songs:
        print("No easy songs found. Run find_easy_songs.py first.")
        return
    
    print("📺 Parsing VideoIndex History.html...")
    recordings = parse_video_index()
    print(f"Found recordings for {len(recordings)} different songs")
    
    if not recordings:
        print("No recordings found in VideoIndex History.html")
        return
    
    created_count = 0
    not_found_count = 0
    already_exists_count = 0
    
    print("🔗 Creating .urltxt files...")
    
    for chopro_file, easy_file in easy_songs:
        urltxt_file = chopro_file.with_suffix('.urltxt')
        
        # Skip if .urltxt already exists
        if urltxt_file.exists():
            already_exists_count += 1
            continue
        
        # Extract song title from ChordPro file
        song_title = extract_title_from_chopro(chopro_file)
        if not song_title:
            print(f"⚠️  Could not extract title from: {chopro_file.name}")
            not_found_count += 1
            continue
        
        # Find matching recording
        match = find_best_match(song_title, recordings)
        
        if match:
            date_obj, date_str, youtube_url = match
            if create_urltxt_file(chopro_file, youtube_url, date_str):
                created_count += 1
                relative_path = chopro_file.relative_to(Path("music/ChordPro"))
                print(f"✅ Created .urltxt for: {relative_path} -> {date_str}")
            else:
                not_found_count += 1
        else:
            not_found_count += 1
            relative_path = chopro_file.relative_to(Path("music/ChordPro"))
            print(f"❌ No recording found for: {relative_path} (title: '{song_title}')")
    
    # Summary report
    print(f"\n📊 SUMMARY:")
    print(f"Easy songs processed: {len(easy_songs)}")
    print(f"New .urltxt files created: {created_count}")
    print(f"Already had .urltxt files: {already_exists_count}")
    print(f"Songs without recordings: {not_found_count}")
    
    if not_found_count > 0:
        print(f"\n💡 TIP: Songs without recordings may need manual review.")
        print(f"Check if song titles in ChordPro files match those in VideoIndex History.html")

if __name__ == "__main__":
    main()
