# Timestamp Update Script

This directory contains a Python script to update v= timestamps in URLs within the index.html file. The script is designed to update version timestamps in PDF links within the practice songs table and submitted songs table.

## Script

### `update_timestamps.py`
A flexible script with multiple options for updating v= timestamps.

**Usage:**
```bash
# Basic usage - updates practice and submitted songs tables
python update_timestamps.py

# Update all v= timestamps in entire file
python update_timestamps.py --all

# Update specific tables only
python update_timestamps.py --tables "practice-songs-table" "submitted-songs-table"

# Dry run (preview changes without making them)
python update_timestamps.py --dry-run

# Process different HTML file
python update_timestamps.py --file "other-page.html"

# Create backup file (backups are NOT created by default)
python update_timestamps.py --backup
```

**Options:**
- `--file, -f`: Specify HTML file to process (default: index.html)
- `--all, -a`: Update all v= timestamps in the entire file
- `--tables, -t`: Specify table IDs to update (default: practice-songs-table submitted-songs-table)
- `--backup`: Create backup file (default: no backup)
- `--dry-run, -n`: Show what would be updated without making changes

## What Gets Updated

The scripts look for PDF links with v= parameters in the format:
```html
<a href="path/to/file.pdf?v=2024.03.02.15.07.18">PDF</a>
```

And updates them to:
```html
<a href="path/to/file.pdf?v=2025.10.31.10.16.09">PDF</a>
```

## Backup Files

By default, no backup files are created. If you want to create a backup, use the `--backup` option:
- `index.html.backup.YYYY-MM-DD-HH-MM-SS` (only created when `--backup` is specified)

## Examples

### Update only practice songs table:
```bash
python update_timestamps.py --tables "practice-songs-table"
```

### Preview what would be changed:
```bash
python update_timestamps.py --dry-run
```

### Update all PDF links in the entire file:
```bash
python update_timestamps.py --all
```

## Notes

- The scripts only update PDF links (URLs containing `.pdf`)
- They preserve the original URL structure, only changing the v= parameter value
- Timestamps are generated using the current date and time
- The script handles UTF-8 and ISO-8859-1 file encodings
- Provides detailed feedback about what was updated
