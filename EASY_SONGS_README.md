# Easy Songs Filtering System

## Overview
The ukulele song archive now includes an "easy songs" filtering feature that allows users to view only songs that are marked as beginner-friendly.

## How to Mark Songs as Easy

To mark a song as "easy", create a `.easy` file with the same base name as your song file in the same directory.

### Examples:

1. **For a ChordPro file:**
   - Song file: `music/ChordPro/2025/July/Peaceful Easy Feeling.chopro`
   - Easy marker: `music/ChordPro/2025/July/Peaceful Easy Feeling.easy`

2. **For a PDF file:**
   - Song file: `music/PDFs/Spring 2024/Amazing Grace.pdf`
   - Easy marker: `music/PDFs/Spring 2024/Amazing Grace.easy`

3. **For multiple formats of the same song:**
   - Song files: 
     - `music/ChordPro/Summer 2023/Happy Birthday.chopro`
     - `music/PDFs/Summer 2023/Happy Birthday.pdf`
   - Easy marker: `music/ChordPro/Summer 2023/Happy Birthday.easy`
   - (One `.easy` file marks all formats of that song as easy)

## How to Create Easy Markers

### Command Line (from TUG directory):
```bash
# Mark a single song as easy
touch "music/ChordPro/2025/July/Peaceful Easy Feeling.easy"

# Mark multiple songs as easy
touch "music/ChordPro/Fall 2023/Twinkle Twinkle Little Star.easy"
touch "music/PDFs/Spring 2024/Mary Had a Little Lamb.easy"
```

### File Explorer:
1. Navigate to the song's directory
2. Create a new empty file with the same name as the song but with `.easy` extension

## How Users Filter Easy Songs

1. **Checkbox Filter**: Users can check the "Show only easy songs" checkbox to see only songs marked as easy
2. **Combined with Search**: The easy filter works together with the text search - users can search for specific easy songs
3. **Row Numbers Preserved**: Even when filtering, the original row numbers are maintained

## Technical Details

- Easy markers work the same way as `.hide` files
- The `.easy` files can be empty - only their presence matters
- Songs marked as easy get the CSS class `easy-song` in the HTML table
- The filtering is done client-side with JavaScript for fast performance

## Maintenance

- To unmark a song as easy: delete the corresponding `.easy` file
- Easy markers are automatically detected when running `GenList.py`
- No need to modify the song files themselves
