#!/usr/bin/env python3
"""
Script to find ChordPro files with 3 or fewer unique chords and create .easy marker files
"""

import re
import os
from pathlib import Path

def extract_chords_from_chopro(file_path):
    """
    Extract unique chords from a ChordPro file
    Returns a set of unique chord names
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return set()
    
    # Find all chord patterns in square brackets
    chord_pattern = r'\[([^\]]+)\]'
    matches = re.findall(chord_pattern, content)
    
    # Clean up chord names and filter out non-chord content
    chords = set()
    for match in matches:
        chord = match.strip()
        
        # Skip if it's likely not a chord (contains spaces, common non-chord patterns)
        if ' ' in chord or len(chord) == 0:
            continue
            
        # Skip common ChordPro directives that might be in brackets
        if chord.lower() in ['t:', 'st:', 'c:', 'comment:', 'title:', 'subtitle:']:
            continue
            
        # Add to chord set
        chords.add(chord)
    
    return chords

def has_easy_marker(chopro_file):
    """Check if a .easy marker file already exists for this ChordPro file"""
    easy_file = chopro_file.with_suffix('.easy')
    return easy_file.exists()

def create_easy_marker(chopro_file):
    """Create a .easy marker file for the given ChordPro file"""
    easy_file = chopro_file.with_suffix('.easy')
    try:
        easy_file.touch()
        return True
    except Exception as e:
        print(f"Error creating {easy_file}: {e}")
        return False

def main():
    # Start from the ChordPro directory
    chopro_dir = Path(".")
    
    if not chopro_dir.exists():
        print(f"ChordPro directory not found: {chopro_dir}")
        return
    
    # Find all .chopro files recursively
    chopro_files = list(chopro_dir.rglob("*.chopro"))
    print(f"Found {len(chopro_files)} ChordPro files to analyze...")
    
    easy_candidates = []
    already_marked = []
    created_markers = []
    errors = []
    
    for chopro_file in chopro_files:
        try:
            # Extract chords from the file
            chords = extract_chords_from_chopro(chopro_file)
            
            # Check if it has 3 or fewer chords
            if len(chords) <= 3 and len(chords) > 0:
                easy_candidates.append((chopro_file, chords))
                
                # Check if .easy marker already exists
                if has_easy_marker(chopro_file):
                    already_marked.append(chopro_file)
                else:
                    # Create .easy marker file
                    if create_easy_marker(chopro_file):
                        created_markers.append(chopro_file)
                        print(f"✅ Created .easy marker for: {chopro_file.name} ({len(chords)} chords: {', '.join(sorted(chords))})")
                    else:
                        errors.append(chopro_file)
        
        except Exception as e:
            print(f"Error processing {chopro_file}: {e}")
            errors.append(chopro_file)
    
    # Summary report
    print(f"\n📊 SUMMARY:")
    print(f"Total ChordPro files analyzed: {len(chopro_files)}")
    print(f"Songs with 3 or fewer chords: {len(easy_candidates)}")
    print(f"Already had .easy markers: {len(already_marked)}")
    print(f"New .easy markers created: {len(created_markers)}")
    print(f"Errors encountered: {len(errors)}")
    
    if easy_candidates:
        print(f"\n🎵 EASY SONGS (3 or fewer chords):")
        for chopro_file, chords in sorted(easy_candidates, key=lambda x: len(x[1])):
            status = "✅ marked" if chopro_file in created_markers else "already marked"
            relative_path = chopro_file.relative_to(chopro_dir)
            print(f"  {len(chords)} chords - {relative_path} ({', '.join(sorted(chords))}) - {status}")
    
    if errors:
        print(f"\n❌ ERRORS:")
        for error_file in errors:
            relative_path = error_file.relative_to(chopro_dir)
            print(f"  {relative_path}")

if __name__ == "__main__":
    main()
