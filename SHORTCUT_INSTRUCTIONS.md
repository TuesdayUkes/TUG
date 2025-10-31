# Windows Shortcut Setup for TUG Timestamp Updater

## Files Created

1. **`update_timestamps.bat`** - Windows batch file that runs the Python script
2. **`create_shortcut.ps1`** - PowerShell script to create the desktop shortcut
3. **`Update TUG Timestamps.lnk`** - Desktop shortcut (created on your desktop)

## Usage

### Using the Desktop Shortcut
1. Double-click the **"Update TUG Timestamps"** shortcut on your desktop
2. A command window will open showing the update progress
3. The script will update timestamps in both the practice songs and submitted songs tables
4. No backup file is created by default (for speed and simplicity)
5. Press any key to close the window when done

### Manual Usage
You can also run the batch file directly:
1. Navigate to `C:\repos\TuesdayUkes\TUG\`
2. Double-click `update_timestamps.bat`

### Advanced Usage
For more options, you can still use the Python script directly:
```bash
# Preview changes without making them
python update_timestamps.py --dry-run

# Update all timestamps in the entire file
python update_timestamps.py --all

# Create backup file (not created by default)
python update_timestamps.py --backup
```

## What the Shortcut Does

The shortcut:
- Runs from the correct working directory (`C:\repos\TuesdayUkes\TUG\`)
- Updates v= timestamps in the practice-songs-table and submitted-songs-table
- Does not create backup files by default (for speed and simplicity)
- Shows progress and results in a command window
- Waits for you to press a key before closing

## Troubleshooting

If the shortcut doesn't work:
1. Make sure Python is installed and accessible from the command line
2. Verify the TUG repository is at `C:\repos\TuesdayUkes\TUG\`
3. Check that `update_timestamps.py` exists in the TUG directory
4. Try running the batch file directly to see any error messages
