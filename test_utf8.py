#!/usr/bin/env python3
"""Test that the ChordPro file can be read as UTF-8"""

try:
    with open("music/ChordPro/It's All Going to Pot.chopro", 'r', encoding='utf-8') as f:
        content = f.read()
    print(f"✅ File successfully read as UTF-8")
    print(f"📊 Length: {len(content)} characters")
    print(f"📝 First 100 characters: {repr(content[:100])}")
except UnicodeDecodeError as e:
    print(f"❌ UTF-8 decode error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
