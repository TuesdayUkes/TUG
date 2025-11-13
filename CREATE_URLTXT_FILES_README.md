````markdown
# Create URL Text Files Script Documentation

The `create_urltxt_files.py` script creates `.urltxt` files for songs that contain YouTube links pointing to their most recent recordings in the VideoIndex History.html. This script has been enhanced to process **all songs** in the music library, not just easy songs.

## 🎯 Purpose

This script bridges the gap between ChordPro song files and video recordings by:

1. **Finding Songs** - Locates all ChordPro files in the music directory
2. **Video Index Parsing** - Extracts song recordings from VideoIndex History.html
3. **Smart Matching** - Links ChordPro songs to their recorded performances
4. **URL File Creation** - Creates `.urltxt` files with YouTube timestamp links

### User Benefits
- **Direct Access**: Click on a song to jump to its latest performance
- **Comprehensive Coverage**: 86.5% of all TUG songs have video examples
- **Learning Aid**: Watch how songs are played in actual TUG sessions
- **Performance Examples**: See how different members perform the same song

## 📊 Coverage Statistics

### Current Status
- **1,467 ChordPro files** processed total
- **1,269 songs have .urltxt files** (86.5% coverage)
- **198 songs** without recordings or matches
- **1,648 different songs** found in VideoIndex History.html

### Evolution of Coverage
- **Before (Easy Songs Only)**: ~250 songs (~17% of collection)
- **After (All Songs)**: 1,467 songs with 86.5% coverage
- **Impact**: Comprehensive video integration across entire TUG song collection

## 📥 Input Requirements

### Required Files
- **ChordPro files** - All `.chopro` files in `music/ChordPro/` directory
- **`music/scripts/VideoIndex History.html`** - Contains all TUG video recordings
- **ChordPro title directives** - Files should have `{title:}` directives for proper matching

### VideoIndex History.html Structure
Expected HTML format with date headers and song tables:
```html
<h2>November 4, 2025</h2>
<table>
<tr><td><a href="https://youtu.be/VIDEO_ID?t=35m45s">35:45</a></td>
    <td>Performer Name</td>
    <td><a href="PDF_LINK">Song Title</a></td></tr>
</table>
```

## 📤 Output

### .urltxt Files
- **Location**: Same directory as corresponding `.chopro` file
- **Naming**: `songname.urltxt` (matches `songname.chopro`)
- **Content**: YouTube URL with timestamp + metadata

### File Format Example
```
# Most recent recording: October 28, 2025
https://youtu.be/wWgTfdLvwPA?t=1h21m20s
```

**Note**: The script only updates `.urltxt` files that contain the comment `# Most recent recording:` which indicates they were created by the script. Manually created `.urltxt` files are preserved and never overwritten.

### Console Output
```bash
Finding all ChordPro songs...
Found 1467 ChordPro files
Parsing VideoIndex History.html...
Found recordings for 1648 different songs
Creating .urltxt files for songs with recordings...
CREATED: .urltxt for: Fall 2021\Rhiannon.chopro -> October 21, 2025
CREATED: .urltxt for: TUG Archive\Long Black Veil.chopro -> October 28, 2025
NOT FOUND: No recording for: Fall 2023\Devil Woman.chopro (title: 'devil woman')

SUMMARY:
ChordPro files processed: 1467
New .urltxt files created: 0
Existing .urltxt files updated: 15
Already up-to-date .urltxt files: 1254
Songs without recordings: 198
Songs with video recordings: 1269/1467 (86.5%)
```

## 🚀 Usage

### Prerequisites
```bash
# Install required dependency
pip install beautifulsoup4

# No need to run find_easy_songs.py first - processes all songs
```

### Basic Usage
```bash
# Navigate to TUG directory
cd /path/to/TUG

# Create URL files for all songs with recordings
python create_urltxt_files.py
```

### Updating with New Recordings
When new TUG sessions are recorded and added to VideoIndex History.html:

```bash
# Rerun the script to update with newer recordings
python create_urltxt_files.py

# The script will:
# - Create new .urltxt files for songs that didn't have recordings before
# - Update existing script-generated .urltxt files if newer recordings are available
# - Preserve manually created .urltxt files (those without "# Most recent recording:" comment)
```

### Legacy Easy Songs Mode
The script automatically processes all songs, but the system maintains backward compatibility with the easy song workflow where `.easy` marker files indicate beginner-friendly songs.

## 🔧 Technical Details

### Dependencies
- **BeautifulSoup4**: HTML parsing for VideoIndex History
- **datetime**: Chronological sorting of recordings
- **pathlib**: File system operations
- **re**: Regular expressions for title cleaning

### Update Behavior
The script intelligently handles existing `.urltxt` files:

1. **Script-generated files**: Files with `# Most recent recording:` comment are updated if newer recordings are found
2. **Manually created files**: Files without the comment are preserved and never overwritten
3. **Same date**: If the most recent recording date matches the existing file, no update is performed
4. **Error handling**: If a file cannot be read, it is preserved (safe default)

### Key Functions

#### `get_all_songs()`
- Finds all `.chopro` files in `music/ChordPro/` directory
- Replaced the previous `get_easy_songs()` function
- Returns list of all ChordPro file paths

#### `parse_video_index()`
- Parses VideoIndex History.html for all recordings
- Extracts performer, song title, YouTube URL, and timestamp
- Groups recordings by song title with chronological sorting

#### `find_best_match(song_title, recordings)`
- Implements fuzzy matching algorithm
- Tries exact match first, then word overlap matching
- Requires minimum 50% word overlap for fuzzy matches

### Smart Matching Algorithm

#### 1. Title Extraction
```python
# From ChordPro files - looks for {title:} or {t:} directives
title_match = re.search(r'\{(?:title|t):\s*([^}]+)\}', content, re.IGNORECASE)
```

#### 2. Title Normalization
- Remove file extensions (`.pdf`, `.chopro`)
- Strip parentheses and version indicators
- Normalize whitespace and convert to lowercase
- Handle common variations and aliases

#### 3. Matching Strategy
1. **Exact match**: Direct title comparison
2. **Fuzzy matching**: Word overlap algorithm (minimum 50% overlap)
3. **Chronological selection**: Always chooses most recent recording

### Enhanced Features
- **Unicode handling**: Properly handles special characters and emoji
- **Progress reporting**: Shows processing status and results
- **Error recovery**: Gracefully handles unreadable files
- **Batch processing**: Efficiently processes large numbers of files

## 📊 Analysis of Missing Songs (198 total)

### Distribution by Directory
- **TUG Archive**: 61 songs (likely older/archived songs)
- **Summer 2020**: 15 songs (early pandemic period)
- **ChordPro root**: 13 songs (miscellaneous files)
- **Fall 2020**: 10 songs (early pandemic period)
- **Various seasonal folders**: 4-8 songs each

### Common Reasons for Missing Recordings
1. **Archive songs** that may not have been performed recently
2. **Early pandemic songs** (2020) when recording patterns were different
3. **Very recent songs** that haven't been performed yet
4. **Songs with title matching issues** between ChordPro files and VideoIndex

## 🎵 Use Cases

### Learning Enhancement
```bash
# Create video links for all songs
python create_urltxt_files.py

# Users can now:
# 1. Browse any song in the collection
# 2. Click .urltxt file to watch most recent performance
# 3. Jump directly to song start in video
# 4. See how different performers play the same song
```

### Practice Sessions
- **Individual practice**: Watch how others play any song
- **Group preparation**: Review songs before TUG meetings
- **Teaching tool**: Show students real performance examples
- **Song exploration**: Discover new songs through video examples

### Content Management
```bash
# Update all links after new VideoIndex History.html
python create_urltxt_files.py

# Verify recent recordings are properly linked
# Ensure comprehensive coverage across all songs
```

## 📈 Impact and Benefits

### Comprehensive Video Integration
- **86.5% of all TUG songs** now have direct links to video recordings
- Each `.urltxt` file contains the most recent performance with date
- Easy navigation from song files to actual performances
- Automatic timestamp jumping to exact song performance

### Improved Workflow
- Musicians can quickly find video examples of any song
- New members can see how songs are typically performed
- Practice sessions can reference actual TUG performances
- Song selection aided by availability of video examples

### File Structure Enhancement
Each song now potentially has three related files:
- `Song.chopro` - The ChordPro sheet music
- `Song.easy` - Easy song marker (if applicable)
- `Song.urltxt` - Link to most recent video recording

This creates a comprehensive song ecosystem where sheet music, difficulty level, and performance examples are all interconnected.

## 🔍 Troubleshooting

### Common Issues

#### "VideoIndex History.html not found"
```bash
# Solution: Check file location
ls music/scripts/VideoIndex\ History.html
# Ensure the file exists and is readable
```

#### Songs not matching recordings
- **Check title format**: Ensure ChordPro files have `{title:}` directives
- **Manual review**: Compare song titles in ChordPro vs VideoIndex History
- **Title variations**: Some songs may need manual `.urltxt` creation

#### Unicode encoding errors
- **Fixed in current version**: Script now handles Unicode characters properly
- **If issues persist**: Check that files are saved in UTF-8 encoding

### Quality Assurance
```bash
# Check processing results
python create_urltxt_files.py | tail -10

# Verify URL format in created files
find music/ChordPro -name "*.urltxt" | head -5 | xargs head -2

# Count total coverage
find music/ChordPro -name "*.urltxt" | wc -l
```

## 🔗 Related Tools

### TUG Ecosystem Integration
- **find_easy_songs.py**: Creates `.easy` markers for beginner songs
- **VideoIndex History.html**: Source of all video recording data
- **Website integration**: URL files can be used for direct video linking
- **formatIndex.py**: Creates the VideoIndex History content

### Workflow Integration
1. **Record TUG session** → Video uploaded to YouTube
2. **Update VideoIndex History.html** → Add new session data
3. **Run create_urltxt_files.py** → Link all songs to recordings
4. **Website deployment** → Users can access comprehensive video links

## 📝 Example Full Session

```bash
$ python create_urltxt_files.py
Finding all ChordPro songs...
Found 1467 ChordPro files
Parsing VideoIndex History.html...
Found recordings for 1648 different songs
Creating .urltxt files for songs with recordings...
NOT FOUND: No recording for: Black.chopro (title: 'black')
NOT FOUND: No recording for: Cat Accountant.chopro (title: 'cat accountant')
... (showing only first 20 'not found' messages)

SUMMARY:
ChordPro files processed: 1467
New .urltxt files created: 3
Already had .urltxt files: 1266  
Songs without recordings: 198
Songs with video recordings: 1269/1467 (86.5%)

TIP: Songs without recordings may need manual review.
Check if song titles in ChordPro files match those in VideoIndex History.html
```

### Success Metrics
- **1,269 songs** with direct video links
- **86.5% coverage** across entire song collection
- **Comprehensive integration** between sheet music and performance videos
- **Enhanced learning experience** for all skill levels

---

*For information about marking easy songs, see [Find Easy Songs Documentation](FIND_EASY_SONGS_README.md).*  
*For VideoIndex formatting fixes, see [VideoIndex Fixes Report](VIDEOINDEX_FIXES_FINAL_REPORT.md).*

````
