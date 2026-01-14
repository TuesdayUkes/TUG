# Filename Validation Script

## Overview

The `validate_filenames.py` script ensures all files in the repository use filenames that are compatible across Windows, Linux, and macOS platforms. This prevents broken links and file access issues caused by problematic characters in filenames.

## Problem

Unicode characters like curly apostrophes ('), en/em dashes (–/—), and smart quotes ("") can cause issues:
- **Broken HTML links**: URL encoding mismatches between filesystem and web links
- **Git conflicts**: Different character representations across platforms
- **File access issues**: Some characters are invalid on Windows
- **Case sensitivity**: macOS/Linux are case-sensitive, Windows is not

### Example Issue

The file `For What It's Worth.pdf` contains a Unicode RIGHT SINGLE QUOTATION MARK (U+2019) instead of a regular apostrophe. This causes:
- Links in `index.html` to fail (looking for `For%20What%20It's%20Worth.pdf`)
- Inconsistent behavior across operating systems
- Potential git merge conflicts

## Usage

### Basic Scan

Check all files in the repository:
```bash
python validate_filenames.py
```

### Check Specific File Types

Only validate PDF and ChordPro files:
```bash
python validate_filenames.py --extensions .pdf .chopro .cho
```

### Show Suggested Fixes

Display recommended filename corrections:
```bash
python validate_filenames.py --fix
```

### Check Specific Directory

Scan only a specific folder:
```bash
python validate_filenames.py --path music/ChordPro
```

### Combine Options

Check only music files with fix suggestions:
```bash
python validate_filenames.py --fix --extensions .pdf .chopro .cho
```

## What It Checks

The script validates filenames for:

### 1. Problematic Unicode Characters
- ` ' ` (U+2018/U+2019) - Curly apostrophes → replace with `'`
- ` " " ` (U+201C/U+201D) - Smart quotes → replace with `"`
- ` – ` (U+2013) - En dash → replace with `-`
- ` — ` (U+2014) - Em dash → replace with `-`
- ` … ` (U+2026) - Ellipsis → replace with `...`
- Non-breaking spaces → replace with regular spaces

### 2. Windows Invalid Characters
These characters are forbidden in Windows filenames:
- `< > : " | ? *`

### 3. Control Characters
ASCII characters 0-31 (invisible/control characters)

### 4. Trailing Spaces or Periods
Windows doesn't allow filenames ending with spaces or periods (before the extension)

### 5. Reserved Windows Names
Files named: `CON`, `PRN`, `AUX`, `NUL`, `COM1-9`, `LPT1-9`

### 6. Path Length Limits
Full path exceeding Windows' 260-character limit

### 7. Case-Only Duplicates
Multiple files that differ only in case (problematic when moving between case-sensitive and case-insensitive filesystems)

## Output Format

```
❌ Found 10 file(s) with compatibility issues:

📁 music\ChordPro\2026\January\For What It's Worth.chopro
   ⚠️  Contains problematic Unicode: ''' (U+2019 RIGHT SINGLE QUOTATION MARK) -> suggest: "'"
   💡 Suggested fix: For What It's Worth.chopro
```

Each issue shows:
- 📁 Full file path
- ⚠️ Description of the issue
- 💡 Suggested filename fix (with `--fix` option)

## Exit Codes

- `0` - No issues found (safe for use in CI/CD)
- `1` - Issues found or error occurred

## Integration into Workflow

### Pre-Submission Check

Before adding new files to git:
```bash
python validate_filenames.py --extensions .pdf .chopro
```

### Git Pre-Commit Hook

Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
python validate_filenames.py --extensions .pdf .chopro .cho
if [ $? -ne 0 ]; then
    echo "❌ Filename validation failed. Please fix filenames before committing."
    exit 1
fi
```

### Automated CI/CD

Add to your continuous integration pipeline:
```yaml
- name: Validate Filenames
  run: python validate_filenames.py
```

## Fixing Issues

### Manual Rename

1. Run validation to identify issues:
   ```bash
   python validate_filenames.py --fix --extensions .pdf .chopro
   ```

2. For each file, rename using the suggested fix:
   ```bash
   # Example: rename "For What It's Worth.pdf" to "For What It's Worth.pdf"
   git mv "music/ChordPro/2026/January/For What It's Worth.pdf" \
          "music/ChordPro/2026/January/For What It's Worth.pdf"
   ```

3. Update any HTML links that reference the old filename

### Important Notes

- **Use `git mv`** instead of regular file rename to preserve git history
- **Update all references**: Check HTML files, scripts, and documentation
- **Test links**: Verify all web links work after renaming
- **Communicate**: Notify team members of filename changes

## Common Scenarios

### Curly Apostrophes in Song Titles

**Problem**: Songs like "Don't Stop", "I'm Yours" saved with curly apostrophes

**Solution**: Use straight apostrophe (') instead
```
❌ Don't Stop.pdf  (U+2019)
✅ Don't Stop.pdf  (ASCII 39)
```

### En/Em Dashes in Song Titles

**Problem**: Artist separators using special dashes

**Solution**: Use regular hyphen-minus (-)
```
❌ Moonshadow – Cat Stevens.pdf  (U+2013 en dash)
✅ Moonshadow - Cat Stevens.pdf  (ASCII 45)
```

### Smart Quotes

**Problem**: Quotes from copying text from formatted documents

**Solution**: Use straight quotes
```
❌ "Hello" World.pdf  (U+201C/U+201D)
✅ "Hello" World.pdf  (ASCII 34)
```

## Prevention Tips

1. **Configure your editor** to use straight quotes instead of smart quotes
2. **Copy from plain text** sources when possible
3. **Run validation** before committing new files
4. **Use ASCII characters** for song titles when creating files
5. **Verify in terminal** - if the filename looks unusual, check it

## Technical Details

### Character Encoding

The script checks for characters outside printable ASCII range (32-126):
- Allows: `A-Z a-z 0-9 ! # $ % & ' ( ) + , - . ; = @ [ ] ^ _ ` { } ~`
- Flags: Unicode characters, control characters, extended ASCII

### Platform-Specific Issues

| Platform | Issue | Example |
|----------|-------|---------|
| Windows | Invalid chars: `< > : " \| ? *` | `Song: Title.pdf` ❌ |
| Windows | Reserved names | `CON.pdf`, `NUL.txt` ❌ |
| Windows | Path length limit | > 260 characters ❌ |
| macOS/Linux | Case sensitivity | `song.pdf` vs `Song.pdf` (different files) |
| All | Unicode normalization | `é` (U+00E9) vs `é` (U+0065 U+0301) |

## Related Scripts

- `update_timestamps.py` - Updates version timestamps in HTML files
- `create_urltxt_files.py` - Creates recording links for songs
- `GenList.py` - Generates song archive HTML

These scripts may need updates if filenames change.

## Troubleshooting

### "No issues found" but links are broken

Check if:
1. URL encoding in HTML matches actual filename
2. Web server encoding settings
3. File actually exists at the expected path

### Can't rename file (permission denied)

- Close any programs using the file
- Check file isn't locked by another process
- Run as administrator (Windows) or use `sudo` (Linux/macOS)

### Git shows file as deleted and added

Use `git mv` instead of regular rename to preserve history:
```bash
git mv "old name.pdf" "new name.pdf"
```

## Support

For issues or questions:
1. Check this documentation
2. Review the script output carefully
3. Test on a small subset of files first
4. Verify HTML links after renaming files
