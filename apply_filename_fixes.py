#!/usr/bin/env python3
"""
Apply filename fixes for cross-platform compatibility issues.
This script renames files identified by validate_filenames.py
"""

import os
import sys
import subprocess
from pathlib import Path

# Fix Windows console encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Define all the renames: (old_name, new_name)
# OLD filenames use Unicode characters (curly apostrophe \u2019, en dash \u2013)
# NEW filenames use ASCII characters (straight apostrophe ', hyphen -)
RENAMES = [
    # For What It's Worth (critical - broken links)
    # OLD uses U+2019 ('), NEW uses ASCII apostrophe (')
    ("music/ChordPro/2026/January/For What It\u2019s Worth.chopro", 
     "music/ChordPro/2026/January/For What It's Worth.chopro"),
    ("music/ChordPro/2026/January/For What It\u2019s Worth.pdf", 
     "music/ChordPro/2026/January/For What It's Worth.pdf"),
    
    # Let's Misbehave
    ("music/ChordPro/2025/October/Let\u2019s Misbehave.chopro",
     "music/ChordPro/2025/October/Let's Misbehave.chopro"),
    ("music/ChordPro/2025/October/Let\u2019s Misbehave.pdf",
     "music/ChordPro/2025/October/Let's Misbehave.pdf"),
    
    # I Still Haven't Found What I'm Looking For
    # Note: First apostrophe is U+2019, second is already ASCII
    ("music/ChordPro/Fall 2022/I Still Haven\u2019t Found What I'm Looking For.chopro",
     "music/ChordPro/Fall 2022/I Still Haven't Found What I'm Looking For.chopro"),
    ("music/PDFs/Fall 2022/I Still Haven\u2019t Found What I'm Looking For.pdf",
     "music/PDFs/Fall 2022/I Still Haven't Found What I'm Looking For.pdf"),
    
    # Moonshadow (already fixed in ChordPro and PDFs, but .urltxt still has en dash)
    ("music/ChordPro/Fall 2022/Moonshadow \u2013 Cat Stevens - 1970.urltxt",
     "music/ChordPro/Fall 2022/Moonshadow - Cat Stevens - 1970.urltxt"),
    
    # Cheer Up - Good Times Are Comin'
    ("music/ChordPro/Summer 2024/Cheer Up - Good Times Are Comin\u2019.chopro",
     "music/ChordPro/Summer 2024/Cheer Up - Good Times Are Comin'.chopro"),
    ("music/PDFs/Summer 2024/Cheer Up - Good Times Are Comin\u2019.pdf",
     "music/PDFs/Summer 2024/Cheer Up - Good Times Are Comin'.pdf"),
]


def rename_file(old_path_str, new_path_str, use_git=True):
    """Rename a file, optionally using git mv"""
    old_path = Path(old_path_str)
    new_path = Path(new_path_str)
    
    if not old_path.exists():
        print(f"⚠️  File not found: {old_path}")
        return False
    
    if new_path.exists():
        print(f"⚠️  Destination already exists: {new_path}")
        return False
    
    try:
        if use_git:
            # Try using git mv
            result = subprocess.run(
                ['git', 'mv', str(old_path), str(new_path)],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            
            if result.returncode == 0:
                print(f"✅ git mv: {old_path.name} → {new_path.name}")
                return True
            else:
                # Git mv failed, fall back to regular rename
                print(f"⚠️  git mv failed, using regular rename...")
                use_git = False
        
        if not use_git:
            # Use regular rename
            old_path.rename(new_path)
            print(f"✅ renamed: {old_path.name} → {new_path.name}")
            return True
            
    except Exception as e:
        print(f"❌ Error renaming {old_path.name}: {e}")
        return False


def main():
    print("Applying filename fixes for cross-platform compatibility...")
    print(f"Total files to rename: {len(RENAMES)}\n")
    
    success_count = 0
    fail_count = 0
    skip_count = 0
    
    for old_path, new_path in RENAMES:
        if old_path == new_path:
            print(f"⏭️  Skipping (no change needed): {Path(old_path).name}")
            skip_count += 1
            continue
        
        if rename_file(old_path, new_path, use_git=True):
            success_count += 1
        else:
            fail_count += 1
    
    print(f"\n{'='*60}")
    print(f"Results:")
    print(f"  ✅ Successfully renamed: {success_count}")
    print(f"  ❌ Failed: {fail_count}")
    print(f"  ⏭️  Skipped: {skip_count}")
    print(f"{'='*60}")
    
    if fail_count > 0:
        print("\n⚠️  Some files could not be renamed. Please check the errors above.")
        return 1
    
    print("\n✅ All files renamed successfully!")
    print("\nNext steps:")
    print("1. Run validation: python validate_filenames.py --extensions .pdf .chopro")
    print("2. Update HTML links in index.html, ukulele-song-archive.html, etc.")
    print("3. Test that all links work correctly")
    print("4. Commit changes: git commit -m 'Fix: Rename files with Unicode characters'")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
