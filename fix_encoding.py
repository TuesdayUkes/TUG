#!/usr/bin/env python3
"""
Fix encoding issues and problematic Unicode characters in ChordPro files.

This script combines functionality to:
1. Detect and convert files from Windows-1252 encoding to UTF-8
2. Replace problematic Unicode characters (especially U+2019 apostrophes) with ASCII equivalents
3. Handle other special characters that cause issues in ChordPro processing

Usage:
    python fix_encoding.py <file_path>     # Process a single file
    python fix_encoding.py                 # Process all .chopro files in music/ChordPro/

Note: This script consolidates the functionality previously split between
fix_encoding.py and fix_apostrophes.py for better maintainability.
"""

import os
import sys
from pathlib import Path

def fix_encoding(file_path):
    """
    Fix encoding issues in a file by trying different encodings and converting to UTF-8.
    """
    encodings_to_try = [
        'utf-8',
        'utf-16-le',      # UTF-16 Little Endian (common on Windows)
        'utf-16-be',      # UTF-16 Big Endian
        'utf-16',         # UTF-16 with BOM detection
        'windows-1252',
        'iso-8859-1',
        'cp1252'
    ]
    
    content = None
    original_encoding = None
    
    # First, check if this might be a UTF-16 file by examining raw bytes
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read()
            
        # Check for UTF-16 patterns (null bytes between characters)
        if len(raw_data) > 10 and raw_data[1::2].count(0) > len(raw_data[1::2]) * 0.3:
            print(f"🔍 File appears to be UTF-16 encoded (detected null byte pattern)")
            # Force UTF-16 detection first
            encodings_to_try = ['utf-16-le', 'utf-16-be', 'utf-16'] + [e for e in encodings_to_try if not e.startswith('utf-16')]
    except Exception as e:
        print(f"⚠️ Could not examine raw bytes: {e}")
    
    # Try to read with different encodings
    for encoding in encodings_to_try:
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
                original_encoding = encoding
                print(f"✅ Successfully read {file_path} with {encoding} encoding")
                break
        except UnicodeDecodeError as e:
            print(f"❌ Failed to read with {encoding}: {e}")
            continue
    
    if content is None:
        print(f"⚠️ Could not read {file_path} with any encoding")
        return False
    
    # Always convert to UTF-8 for consistency, even if originally UTF-8
    needs_conversion = original_encoding != 'utf-8'
    if not needs_conversion:
        # Check if the file has any issues that need fixing anyway
        with open(file_path, 'rb') as f:
            raw_data = f.read()
        # Check for artifacts that need fixing
        artifact_patterns = [b'\x00', b'\xbf\xc3', b'\xbe\xc3']  # null bytes, BOM artifacts
        has_artifacts = any(pattern in raw_data for pattern in artifact_patterns)
        
        # Also check for UTF-16 line ending artifacts in the decoded content
        utf16_artifacts = ['\uBFC3', '\uBEC3', '\u0A0D', '\u0D00']
        has_content_artifacts = any(artifact in content for artifact in utf16_artifacts)
        
        # Check for excessive empty lines (3 or more consecutive newlines)
        import re
        has_excessive_lines = bool(re.search(r'\n{3,}', content))
        
        if has_artifacts or has_content_artifacts or has_excessive_lines:
            reason = []
            if has_artifacts: reason.append("byte artifacts")
            if has_content_artifacts: reason.append("UTF-16 artifacts") 
            if has_excessive_lines: reason.append("excessive empty lines")
            print(f"⚠️ {file_path} contains {', '.join(reason)} - needs cleaning")
            needs_conversion = True
        else:
            print(f"ℹ️ {file_path} is already clean UTF-8 encoded")
    
    if not needs_conversion:
        return True
    
    # Convert problematic characters using Unicode escape sequences for reliability
    replacements = {
        '\u2019': "'",   # Right single quotation mark (U+2019) - causes VS Code yellow highlighting
        '\u2018': "'",   # Left single quotation mark (U+2018)
        '\u201C': '"',   # Left double quotation mark (U+201C)
        '\u201D': '"',   # Right double quotation mark (U+201D)
        '\u2013': '-',   # En dash (U+2013)
        '\u2014': '--',  # Em dash (U+2014)
        '\u2026': '...', # Horizontal ellipsis (U+2026)
        '\uBFC3': '',    # UTF-16 conversion artifact (BOM remnant)
        '\uBEC3': '',    # UTF-16 conversion artifact (BOM remnant)
        '\u0A0D': '\n',  # UTF-16 line ending artifact (LF + CR combined)
        '\u0D00': '',    # UTF-16 line ending artifact (CR + NULL)
    }
    
    # Special handling for UTF-16 files - normalize line endings first
    if original_encoding and original_encoding.startswith('utf-16'):
        # UTF-16 files often have messy line endings when converted
        # First normalize all line ending variations
        content = content.replace('\r\n', '\n')  # Windows CRLF -> LF
        content = content.replace('\r', '\n')    # Mac CR -> LF
        # Remove any remaining null character artifacts
        content = content.replace('\x00', '')
        print("🔧 Normalized UTF-16 line endings and removed null characters")
    
    total_replacements = 0
    for old_char, new_char in replacements.items():
        count = content.count(old_char)
        if count > 0:
            content = content.replace(old_char, new_char)
            char_name = {
                '\u2019': 'right single quotes',
                '\u2018': 'left single quotes', 
                '\u201C': 'left double quotes',
                '\u201D': 'right double quotes',
                '\u2013': 'en dashes',
                '\u2014': 'em dashes',
                '\u2026': 'ellipsis'
            }.get(old_char, 'characters')
            print(f"🔄 Replaced {count} {char_name} with '{new_char}'")
            total_replacements += count
    
    if total_replacements > 0:
        print(f"✨ Total Unicode characters replaced: {total_replacements}")
    else:
        print("ℹ️ No problematic Unicode characters found")
    
    # Clean up excessive empty lines 
    import re
    original_lines = len(content.split('\n'))
    
    # For UTF-16 converted files, be more aggressive with cleanup
    if original_encoding and original_encoding.startswith('utf-16'):
        # Remove all sequences of 2 or more empty lines, replace with single empty line
        content = re.sub(r'\n{3,}', '\n\n', content)  # 3+ newlines -> 2 newlines
        content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)  # Remove whitespace-only lines between empty lines
    else:
        # For other files, just clean up excessive empty lines (3+ consecutive)
        content = re.sub(r'\n{4,}', '\n\n\n', content)  # 4+ newlines -> 3 newlines max
    
    new_lines = len(content.split('\n'))
    
    if original_lines != new_lines:
        lines_removed = original_lines - new_lines
        print(f"🧹 Cleaned up excessive empty lines (removed {lines_removed} extra lines)")
    
    # Write back as UTF-8
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ Successfully converted {file_path} to UTF-8")
        return True
    except Exception as e:
        print(f"❌ Failed to write {file_path}: {e}")
        return False

def find_chopro_files():
    """Find all .chopro files in the music/ChordPro directory."""
    chopro_files = []
    music_dir = os.path.join(os.getcwd(), 'music', 'ChordPro')
    
    if not os.path.exists(music_dir):
        return chopro_files
    
    for root, dirs, files in os.walk(music_dir):
        for file in files:
            if file.endswith('.chopro'):
                chopro_files.append(os.path.join(root, file))
    
    return chopro_files

def main():
    import sys
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if os.path.exists(file_path):
            print(f"🔍 Analyzing encoding for: {file_path}")
            if fix_encoding(file_path):
                print(f"🎉 File encoding fixed successfully!")
            else:
                print(f"� Failed to fix file encoding")
                sys.exit(1)
        else:
            print(f"❌ File not found: {file_path}")
            sys.exit(1)
    else:
        # Find all .chopro files
        chopro_files = find_chopro_files()
        if not chopro_files:
            print("ℹ️ No .chopro files found in music/ChordPro/")
            return
        
        print(f"� Found {len(chopro_files)} .chopro files")
        print("🔧 Processing encoding fixes and Unicode character replacements...")
        
        success_count = 0
        for file_path in chopro_files:
            print(f"\n� Processing: {os.path.basename(file_path)}")
            if fix_encoding(file_path):
                success_count += 1
        
        print(f"\n🎉 Successfully processed {success_count}/{len(chopro_files)} files")

if __name__ == "__main__":
    main()
