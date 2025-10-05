#!/usr/bin/env python3
"""Analyze characters in ChordPro file to identify what VS Code is highlighting"""

import re

def analyze_unicode_chars(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Look for common problematic Unicode characters
    problematic_chars = {
        ''': 'RIGHT SINGLE QUOTATION MARK',
        ''': 'LEFT SINGLE QUOTATION MARK', 
        '"': 'LEFT DOUBLE QUOTATION MARK',
        '"': 'RIGHT DOUBLE QUOTATION MARK',
        '–': 'EN DASH',
        '—': 'EM DASH',
        '…': 'HORIZONTAL ELLIPSIS',
    }
    
    print(f"🔍 Analyzing: {file_path}")
    print(f"📊 File length: {len(content)} characters")
    print()
    
    found_any = False
    for char, name in problematic_chars.items():
        positions = [m.start() for m in re.finditer(re.escape(char), content)]
        if positions:
            found_any = True
            print(f"⚠️  Found {len(positions)} instances of '{char}' ({name}) at positions: {positions[:10]}{'...' if len(positions) > 10 else ''}")
            # Show context around first occurrence
            pos = positions[0]
            start = max(0, pos - 20)
            end = min(len(content), pos + 20)
            context = content[start:end].replace('\n', '\\n')
            print(f"   Context: ...{context}...")
            print(f"   Unicode: U+{ord(char):04X}")
            print()
    
    if not found_any:
        print("✅ No problematic Unicode characters found")
        
        # Check for any non-ASCII characters
        non_ascii = []
        for i, char in enumerate(content):
            if ord(char) > 127:
                non_ascii.append((i, char, ord(char)))
        
        if non_ascii:
            print(f"ℹ️  Found {len(non_ascii)} non-ASCII characters:")
            for pos, char, code in non_ascii[:10]:  # Show first 10
                print(f"   Position {pos}: '{char}' (U+{code:04X})")
        else:
            print("✅ File contains only ASCII characters")

if __name__ == "__main__":
    analyze_unicode_chars("music/ChordPro/It's All Going to Pot.chopro")
