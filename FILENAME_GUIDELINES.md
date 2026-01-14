# Filename Guidelines - Quick Reference

## ✅ DO Use These Characters

- **Letters**: A-Z, a-z
- **Numbers**: 0-9
- **Safe punctuation**: 
  - Hyphen: `-`
  - Underscore: `_`
  - Period: `.`
  - Parentheses: `(` `)`
  - **Straight apostrophe**: `'` (Shift+7 key)
  - Comma: `,`
  - Space: ` `

## ❌ DON'T Use These Characters

| Character | Name | Why It's Bad | Use Instead |
|-----------|------|--------------|-------------|
| `'` `'` | Curly apostrophes | Breaks web links, URL encoding issues | `'` (straight) |
| `"` `"` | Smart quotes | Breaks web links | `"` (straight) |
| `–` | En dash | URL encoding issues | `-` (hyphen) |
| `—` | Em dash | URL encoding issues | `-` (hyphen) |
| `…` | Ellipsis | URL encoding issues | `...` (three dots) |
| `< > : " \| ? *` | Windows invalid | File won't save on Windows | Avoid entirely |
| Trailing space/period | | Windows truncates | Remove trailing |

## 🔍 How to Check Before Committing

### Option 1: Run Validation Script
```bash
# Check your files
python validate_filenames.py --fix --extensions .pdf .chopro

# If issues found, fix them before git add
```

### Option 2: Visual Check
Look carefully at apostrophes and dashes in filenames:
- Straight apostrophe `'` looks vertical
- Curly apostrophe `'` looks curved
- Hyphen `-` is short
- En/em dash `–` `—` is longer

### Option 3: Text Editor Test
Copy the filename and paste into Notepad (Windows) or TextEdit (Mac) in plain text mode:
- If it looks different, you have Unicode characters
- Compare character-by-character with keyboard characters

## 🛠️ How to Create Safe Filenames

### Method 1: Type Manually
When creating files, **type the filename yourself** using only keyboard keys - don't copy-paste from formatted documents.

### Method 2: Disable Smart Quotes

**VS Code:**
```
File → Preferences → Settings
Search: "smart quotes"
Disable: Editor: Auto Detect Quotes
```

**Microsoft Word:**
```
File → Options → Proofing → AutoCorrect Options
AutoFormat As You Type → uncheck "Straight quotes with smart quotes"
```

**macOS:**
```
System Preferences → Keyboard → Text
Uncheck "Use smart quotes and dashes"
```

## 📝 Good Examples

✅ Good filenames:
- `For What It's Worth.pdf` (straight apostrophe)
- `Don't Stop Believin'.chopro` (straight apostrophe)
- `Moonshadow - Cat Stevens.pdf` (hyphen, not en dash)
- `It's All Going to Pot.chopro` (straight apostrophe)

❌ Bad filenames:
- `For What It's Worth.pdf` (curly apostrophe U+2019)
- `Don't Stop Believin'.chopro` (left curly quote U+2018)
- `Moonshadow – Cat Stevens.pdf` (en dash U+2013)
- `Song "Title" Here.pdf` (smart quotes)

## 🚨 Common Sources of Bad Characters

1. **Copy-paste from Microsoft Word** - Uses smart quotes by default
2. **Copy-paste from web pages** - Often uses typographic quotes
3. **macOS auto-correction** - Converts straight quotes to curly
4. **Email clients** - May convert quotes automatically
5. **PDF text extraction** - Often preserves typographic characters

## 🔧 Quick Fixes

### Already Created a Bad Filename?

```bash
# Use git mv to rename (preserves history)
git mv "bad'filename.pdf" "good'filename.pdf"

# Then update any HTML/script references
```

### Copied Text from Word?

1. Paste into Notepad/TextEdit (plain text mode) first
2. Copy from plain text editor
3. Use for filename

### Not Sure If It's Safe?

Run the validator:
```bash
python validate_filenames.py --path "path/to/file"
```

## 💡 Remember

- **When in doubt, type it out** - Don't copy-paste filenames
- **Straight quotes only** - They're on your keyboard
- **Use hyphens** - Not en or em dashes
- **Test before commit** - Run `validate_filenames.py`

---

Need more details? See [FILENAME_VALIDATION_README.md](FILENAME_VALIDATION_README.md)
