# Create URL Text Files Script Documentation

The `create_urltxt_files.py` script creates `.urltxt` files for easy songs that contain YouTube links pointing to their most recent recordings in the VideoIndex History.

## 🎯 Purpose

This script bridges the gap between easy song markers and video recordings by:

1. **Finding Easy Songs** - Locates all songs with `.easy` marker files
2. **Video Index Parsing** - Extracts song recordings from VideoIndex History.html
3. **Smart Matching** - Links ChordPro songs to their recorded performances
4. **URL File Creation** - Creates `.urltxt` files with YouTube timestamp links

### User Benefits
- **Direct Access**: Click on a song to jump to its latest performance
- **Beginner-Friendly**: Easy songs have immediate video examples
- **Learning Aid**: Watch how songs are played in actual TUG sessions

## 📥 Input Requirements

### Required Files
- **`.easy` marker files** - Created by `find_easy_songs.py`
- **`music/scripts/VideoIndex History.html`** - Contains all TUG video recordings
- **ChordPro files** - Must have `{title:}` directives for proper matching

### VideoIndex History.html Structure
Expected HTML format with date headers and song tables:
```html
<h2>November 4, 2025</h2>
<table>
<tr><td><a href="https://youtu.be/VIDEO_ID?t=35m45s">35:45</a></td>
    <td>group</td>
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

### Console Output
- **Progress tracking**: Shows each successful URL file creation
- **Match results**: Displays which recordings were found
- **Summary statistics**: Created files, already existing, not found

## 🚀 Usage

### Prerequisites
```bash
# Install required dependency
pip install beautifulsoup4

# Ensure easy songs are marked first
python find_easy_songs.py
```

### Basic Usage
```bash
# Navigate to TUG directory
cd /path/to/TUG

# Create URL files for all easy songs
python create_urltxt_files.py
```

### Expected Output
```bash
🔍 Finding easy songs...
Found 261 songs with .easy markers
📺 Parsing VideoIndex History.html...
Found recordings for 1588 different songs
🔗 Creating .urltxt files...
✅ Created .urltxt for: Fall 2021\Rhiannon.chopro -> October 21, 2025
✅ Created .urltxt for: TUG Archive\Long Black Veil.chopro -> October 28, 2025
❌ No recording found for: Fall 2023\Devil Woman.chopro (title: 'devil woman')

📊 SUMMARY:
Easy songs processed: 261
New .urltxt files created: 212
Already had .urltxt files: 3
Songs without recordings: 46
```

## 🔧 Technical Details

### Dependencies
- **BeautifulSoup4**: HTML parsing for VideoIndex History
- **datetime**: Chronological sorting of recordings
- **pathlib**: File system operations
- **re**: Regular expressions for title cleaning

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

### Date Parsing
```python
# Converts "November 4, 2025" to sortable datetime objects
date_obj = datetime.datetime.strptime(current_date, "%B %d, %Y")
```

## 📊 Use Cases

### Learning Enhancement
```bash
# Create video links for easy songs
python create_urltxt_files.py

# Students can now:
# 1. Browse easy songs
# 2. Click .urltxt file to watch performance
# 3. Jump directly to song start in video
```

### Practice Sessions
- **Individual practice**: Watch how others play the song
- **Group preparation**: Review songs before TUG meetings
- **Teaching tool**: Show students real performance examples

### Content Management
```bash
# Update all links after new VideoIndex History.html
python create_urltxt_files.py

# Verify recent recordings are properly linked
# Check that new easy songs get video references
```

## 🎵 Matching Examples

### Successful Matches
- **"Rhiannon"** → October 21, 2025 recording
- **"Long Black Veil"** → October 28, 2025 recording
- **"Dream Baby"** → October 21, 2025 recording
- **"Ain't Gonna Rain No More"** → November 4, 2025 recording

### Common Match Challenges
- **Variations in titles**: "House of the Rising Sun" vs "House of Rising Sun"
- **Version indicators**: "Bad Moon Rising - G" vs "Bad Moon Rising"
- **Parenthetical additions**: "Prairie Lullaby (Don Edwards)" vs "Prairie Lullaby"

## 🔍 Troubleshooting

### Common Issues

#### "VideoIndex History.html not found"
```bash
# Solution: Check file location
ls music/scripts/VideoIndex\ History.html
# Ensure the file exists and is readable
```

#### "No easy songs found"
```bash
# Solution: Run find_easy_songs.py first
python find_easy_songs.py
# This creates the .easy marker files needed
```

#### Songs not matching recordings
- **Check title format**: Ensure ChordPro files have `{title:}` directives
- **Manual review**: Compare song titles in ChordPro vs VideoIndex History
- **Title variations**: Some songs may need manual `.urltxt` creation

### Quality Assurance
```bash
# Check for songs without recordings
grep -l "No recording found" output.log

# Verify URL format in created files
head -2 music/ChordPro/*/Song.urltxt
```

## 🔗 Related Tools

### TUG Ecosystem Integration
- **find_easy_songs.py**: Creates the `.easy` markers this script depends on
- **VideoIndex History.html**: Source of all video recording data
- **Website integration**: URL files can be used for direct video linking
- **formatIndex.py**: Creates the VideoIndex History content

### Workflow Integration
1. **Record TUG session** → Video uploaded to YouTube
2. **Update VideoIndex History.html** → Add new session data
3. **Run find_easy_songs.py** → Mark easy songs if needed
4. **Run create_urltxt_files.py** → Link easy songs to recordings
5. **Website deployment** → Users can access video links

## 📝 Example Session

### Full Processing Run
```bash
$ python create_urltxt_files.py
🔍 Finding easy songs...
Found 261 songs with .easy markers
📺 Parsing VideoIndex History.html...
Found recordings for 1588 different songs
🔗 Creating .urltxt files...
✅ Created .urltxt for: Eco Packrat.chopro -> April 23, 2024
✅ Created .urltxt for: End of the Line.chopro -> May 6, 2025
✅ Created .urltxt for: Golden Ring.chopro -> July 29, 2025
✅ Created .urltxt for: Rhiannon.chopro -> October 21, 2025
❌ No recording found for: It's All Going to Pot.chopro (title: 'it's all going to pot')
...

📊 SUMMARY:
Easy songs processed: 261
New .urltxt files created: 212
Already had .urltxt files: 3
Songs without recordings: 46

💡 TIP: Songs without recordings may need manual review.
Check if song titles in ChordPro files match those in VideoIndex History.html
```

### Impact Assessment
- **212 easy songs** now have direct video links
- **81% success rate** in matching songs to recordings
- **Enhanced learning experience** for beginners with video examples

---

*For information about marking easy songs, see [Find Easy Songs Documentation](FIND_EASY_SONGS_README.md).*
