# Filename Validation Report
**Generated:** January 14, 2026

## Summary

The validation script found **10 files** with cross-platform compatibility issues in the TUG repository.

## Issues by Type

### Unicode Apostrophes (9 files)
Files containing RIGHT SINGLE QUOTATION MARK (U+2019 `'`) instead of standard apostrophe (ASCII 39 `'`):

1. `music/ChordPro/2025/October/Let's Misbehave.chopro`
2. `music/ChordPro/2025/October/Let's Misbehave.pdf`
3. `music/ChordPro/2026/January/For What It's Worth.chopro` ⚠️ **Causes broken links**
4. `music/ChordPro/2026/January/For What It's Worth.pdf` ⚠️ **Causes broken links**
5. `music/ChordPro/Fall 2022/I Still Haven't Found What I'm Looking For.chopro`
6. `music/ChordPro/Summer 2024/Cheer Up - Good Times Are Comin'.chopro`
7. `music/PDFs/Fall 2022/I Still Haven't Found What I'm Looking For.pdf`
8. `music/PDFs/Summer 2024/Cheer Up - Good Times Are Comin'.pdf`

### Unicode En Dash (2 files)
Files containing EN DASH (U+2013 `–`) instead of standard hyphen-minus (ASCII 45 `-`):

1. `music/ChordPro/Fall 2022/Moonshadow – Cat Stevens - 1970.chopro`
2. `music/PDFs/Fall 2022/Moonshadow – Cat Stevens - 1970.pdf`

## Impact

### Broken Links Confirmed
The files `For What It's Worth.pdf` and `For What It's Worth.chopro` are causing broken links in:
- `index.html` (line 733)
- `ukulele-song-archive.html`
- `music/scripts/VideoIndex History.html` (line 284)

**Why?** The HTML links use URL-encoded standard apostrophe (`For%20What%20It's%20Worth.pdf`) but the actual filename contains a Unicode curly apostrophe.

### Potential Issues
The other files may cause:
- Link resolution failures on some web servers
- Git conflicts when collaborating across different OS
- File access problems when shared between Windows/Linux/macOS
- Search and indexing issues

## Recommended Fixes

### High Priority (Broken Links)
```bash
# Fix For What It's Worth files (broken links)
cd "c:/repos/TuesdayUkes/TUG/music/ChordPro/2026/January"
git mv "For What It's Worth.chopro" "For What It's Worth.chopro"
git mv "For What It's Worth.pdf" "For What It's Worth.pdf"
```

Then update HTML files to fix links (see below).

### Medium Priority (Preventive)
```bash
# Fix Let's Misbehave
cd "c:/repos/TuesdayUkes/TUG/music/ChordPro/2025/October"
git mv "Let's Misbehave.chopro" "Let's Misbehave.chopro"
git mv "Let's Misbehave.pdf" "Let's Misbehave.pdf"

# Fix I Still Haven't Found What I'm Looking For
cd "c:/repos/TuesdayUkes/TUG/music/ChordPro/Fall 2022"
git mv "I Still Haven't Found What I'm Looking For.chopro" "I Still Haven't Found What I'm Looking For.chopro"

cd "c:/repos/TuesdayUkes/TUG/music/PDFs/Fall 2022"
git mv "I Still Haven't Found What I'm Looking For.pdf" "I Still Haven't Found What I'm Looking For.pdf"

# Fix Moonshadow
cd "c:/repos/TuesdayUkes/TUG/music/ChordPro/Fall 2022"
git mv "Moonshadow – Cat Stevens - 1970.chopro" "Moonshadow - Cat Stevens - 1970.chopro"

cd "c:/repos/TuesdayUkes/TUG/music/PDFs/Fall 2022"
git mv "Moonshadow – Cat Stevens - 1970.pdf" "Moonshadow - Cat Stevens - 1970.pdf"

# Fix Cheer Up
cd "c:/repos/TuesdayUkes/TUG/music/ChordPro/Summer 2024"
git mv "Cheer Up - Good Times Are Comin'.chopro" "Cheer Up - Good Times Are Comin'.chopro"

cd "c:/repos/TuesdayUkes/TUG/music/PDFs/Summer 2024"
git mv "Cheer Up - Good Times Are Comin'.pdf" "Cheer Up - Good Times Are Comin'.pdf"
```

### Update HTML Links

After renaming files, update these HTML files:

#### index.html
Find and replace:
```html
<!-- OLD (line 733) -->
<a href="https://tuesdayukes.org/music/ChordPro/2026/January/For%20What%20It's%20Worth.pdf?v=2026.01.13.17.30.37">For What It's Worth</a>

<!-- NEW -->
<a href="https://tuesdayukes.org/music/ChordPro/2026/January/For%20What%20It's%20Worth.pdf?v=2026.01.13.17.30.37">For What It's Worth</a>
```

#### VideoIndex History.html
Find and replace:
```html
<!-- OLD (line 284) -->
<a href="https://tuesdayukes.org/music/ChordPro/2026/January/For%20What%20It's%20Worth.pdf?v=2026.01.13.17.30.37">For What It's Worth</a>

<!-- NEW -->
<a href="https://tuesdayukes.org/music/ChordPro/2026/January/For%20What%20It's%20Worth.pdf?v=2026.01.13.17.30.37">For What It's Worth</a>
```

#### ukulele-song-archive.html
Search for "For What It" and update any matching links.

## Prevention

To prevent future issues:

1. **Before committing new files**, run:
   ```bash
   python validate_filenames.py --fix --extensions .pdf .chopro .cho
   ```

2. **Configure your text editor** to use straight quotes:
   - VS Code: Search for "smart quotes" in settings and disable
   - Word: File → Options → Proofing → AutoCorrect Options → AutoFormat As You Type → uncheck "Straight quotes" with "smart quotes"

3. **When creating filenames**, use only:
   - Letters: A-Z, a-z
   - Numbers: 0-9
   - Basic punctuation: `- _ . ( ) ' ,`
   - Avoid: Curly quotes, em/en dashes, special Unicode

4. **Set up pre-commit hook** (optional):
   ```bash
   # Create .git/hooks/pre-commit
   #!/bin/bash
   python validate_filenames.py --extensions .pdf .chopro .cho
   if [ $? -ne 0 ]; then
       echo "❌ Fix filename issues before committing"
       exit 1
   fi
   ```

## Testing

After fixing files, verify:

1. **Run validation again**:
   ```bash
   python validate_filenames.py --extensions .pdf .chopro .cho
   ```
   Should show: `✅ No filename compatibility issues found!`

2. **Test web links**:
   - Visit the affected HTML pages
   - Click on the song links
   - Verify PDFs load correctly

3. **Check git status**:
   ```bash
   git status
   ```
   Should show renamed files, not deletions/additions

## Character Reference

| Bad Character | Good Replacement | Where It Comes From |
|---------------|------------------|---------------------|
| `'` (U+2019) | `'` (ASCII 39) | Microsoft Word, macOS auto-correction |
| `'` (U+2018) | `'` (ASCII 39) | Microsoft Word, macOS auto-correction |
| `"` (U+201C) | `"` (ASCII 34) | Microsoft Word, macOS auto-correction |
| `"` (U+201D) | `"` (ASCII 34) | Microsoft Word, macOS auto-correction |
| `–` (U+2013) | `-` (ASCII 45) | Microsoft Word em/en dash auto-replace |
| `—` (U+2014) | `-` (ASCII 45) | Microsoft Word em/en dash auto-replace |
| `…` (U+2026) | `...` (ASCII) | macOS auto-correction, copy-paste |

## Next Steps

1. ✅ Validation script created and tested
2. ⏳ Fix high-priority broken links (For What It's Worth)
3. ⏳ Update HTML files with corrected links
4. ⏳ Fix remaining files (optional but recommended)
5. ⏳ Add validation to git workflow
6. ⏳ Document filename guidelines for contributors

---

**Questions?** See [FILENAME_VALIDATION_README.md](FILENAME_VALIDATION_README.md) for detailed documentation.
