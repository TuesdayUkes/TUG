# Extract Songs Script Documentation

The `extract_songs.py` script is a utility tool that parses the TUG website's `index.html` file to extract song data from HTML tables and format it for analysis or backup purposes.

## 🎯 Purpose

This script extracts song information from the TUG website's HTML tables to create a **template for YouTube video descriptions** with timestamp chapter markers. The output serves two main purposes:

1. **YouTube Description Template** - Creates timestamped entries for video chapter markers
2. **Input for formatindex.py** - After manual editing, serves as input for further processing

### Workflow
1. **Extract** - Script generates initial template with placeholder timestamps (0:00)
2. **Manual Edit** - User updates with accurate timestamps and sorts by appearance order
3. **YouTube Upload** - Use edited file as video description with chapter markers
4. **Further Processing** - Edited file becomes input for `formatindex.py`

## 📥 Input Requirements

### Required File
- **`index.html`** - Must be present in the same directory as the script
- Contains HTML tables with song data and PDF links

### Expected HTML Structure
The script looks for these specific table elements:
```html
<table id="practice-songs-table">
  <tr><th>Title</th><th>PDF</th></tr>
  <tr><td>Song Title</td><td><a href="path/to/song.pdf">PDF</a></td></tr>
</table>

<table id="submitted-songs-table">
  <tr><th>Submitter</th><th>Title</th><th>PDF</th></tr>
  <tr><td>Member Name</td><td>Song Title</td><td><a href="path/to/song.pdf">PDF</a></td></tr>
</table>
```

## 📤 Output

### Console Output
- Displays all extracted songs in formatted text
- Shows summary statistics (total songs, practice songs, submitted songs)
- Reports any errors encountered

### File Output
- **`music/scripts/Music Links.txt`** - YouTube video description template
- Format: `0:00:00 submitter (title) url`
- One song per line with placeholder timestamps
- Ready for manual editing with actual video timestamps

### Output Format Example (Initial Template)
```
0:00:00 group (Amazing Grace) https://tuesdayukes.org/music/PDFs/Amazing_Grace.pdf
0:00:00 John Smith (House of the Rising Sun) https://tuesdayukes.org/music/PDFs/House_Rising_Sun.pdf
0:00:00 group (Puff the Magic Dragon) https://tuesdayukes.org/music/PDFs/Puff_Magic_Dragon.pdf
```

### After Manual Editing (YouTube Ready)
```
0:00:00 group (Amazing Grace) https://tuesdayukes.org/music/PDFs/Amazing_Grace.pdf
0:02:45 group (Puff the Magic Dragon) https://tuesdayukes.org/music/PDFs/Puff_Magic_Dragon.pdf
0:05:30 John Smith (House of the Rising Sun) https://tuesdayukes.org/music/PDFs/House_Rising_Sun.pdf
```

## 🚀 Usage

### Basic Usage
```bash
# Navigate to TUG directory
cd /path/to/TUG

# Ensure index.html is present
ls index.html

# Run the extraction script
python extract_songs.py
```

### Python Environment
```bash
# Using configured Python environment
python extract_songs.py

# Or with specific Python version
python3 extract_songs.py
```

## 🔧 Technical Details

### Dependencies
- **BeautifulSoup4** - HTML parsing
- **urllib.parse** - URL handling (standard library)
- **re** - Regular expressions (standard library)

### Install Dependencies
```bash
pip install beautifulsoup4
```

### Key Functions

#### `extract_pdf_url(td_element)`
- Extracts the first PDF URL from a table cell
- Handles relative and absolute URLs
- Converts relative paths to full tuesdayukes.org URLs

#### `extract_practice_songs(soup)`
- Parses the practice-songs-table
- Returns list of songs with 'group' as submitter
- Expects 2+ columns: Title, PDF link

#### `extract_submitted_songs(soup)`
- Parses the submitted-songs-table  
- Returns list of songs with actual submitter names
- Expects 3+ columns: Submitter, Title, PDF link

#### `format_song_entry(song, timestamp="0:00:00")`
- Formats song data into Music Links.txt format
- Default timestamp is "0:00:00" for all songs

## 📊 Use Cases

### YouTube Video Production
```bash
# 1. Generate initial template from website
python extract_songs.py

# 2. Manually edit timestamps (example workflow)
# - Watch recorded TUG session video
# - Note actual start time of each song
# - Update music/scripts/Music Links.txt with real timestamps
# - Sort lines by chronological order of appearance

# 3. Use as YouTube video description for chapter markers
# Copy content to YouTube video description
```

### Video Chapter Markers
The edited file creates clickable chapter markers in YouTube videos:
- **0:00:00** - Viewers can jump to video start
- **0:02:45** - Click to jump to "Puff the Magic Dragon"  
- **0:05:30** - Click to jump to "House of the Rising Sun"

### Integration with formatindex.py
```bash
# After manual timestamp editing, file becomes input for:
python formatindex.py "music/scripts/Music Links.txt"
# This processes the timestamped data for website integration
```

*For complete formatindex.py documentation, see [Format Index Script Documentation](FORMATINDEX_README.md).*

## 🔍 Troubleshooting

### Common Issues

#### "index.html not found"
```bash
# Solution: Ensure you're in the TUG directory
ls index.html
# If missing, the file may be in a different location
```

#### "No songs found in the HTML tables"
- Check that `index.html` contains the expected table IDs
- Verify table structure matches expected format
- Ensure PDF links are present in table cells

#### URL Conversion Issues
The script handles these URL formats:
- `music/PDFs/song.pdf` → `https://tuesdayukes.org/music/PDFs/song.pdf`
- `https://tuesdayukes.org/...` → unchanged
- Other relative paths → `https://tuesdayukes.org/music/{path}`

### Debugging
```bash
# Run with Python's verbose mode
python -v extract_songs.py

# Check BeautifulSoup installation
python -c "import bs4; print(bs4.__version__)"
```

## 🔗 Related Tools

### TUG Ecosystem Integration
- **Website Archive** - Source data for extraction
- **PDF Generation** - Creates PDFs referenced in extraction
- **Music Links.txt** - Compatible output format
- **Song Database** - Can import extracted data

### Workflow Integration
1. **Record TUG Session** → Video file created
2. **Extract Song List** → `python extract_songs.py` generates template
3. **Manual Timestamp Editing** → Watch video, update timestamps, sort chronologically
4. **YouTube Upload** → Use edited file as video description with chapter markers
5. **Website Integration** → `python formatindex.py extracted_music_links.txt`

## 📝 Example Session

### Initial Template Generation
```bash
$ python extract_songs.py
Extracted song data in Music Links.txt format:
============================================================
0:00:00 group (Amazing Grace) https://tuesdayukes.org/music/PDFs/Amazing_Grace.pdf
0:00:00 John Smith (House of the Rising Sun) https://tuesdayukes.org/music/PDFs/House_Rising_Sun.pdf
0:00:00 group (Puff the Magic Dragon) https://tuesdayukes.org/music/PDFs/Puff_Magic_Dragon.pdf
0:00:00 Mary Johnson (Blackbird) https://tuesdayukes.org/music/PDFs/Blackbird.pdf

Output also saved to: music/scripts/Music Links.txt

Total songs extracted: 4
Practice songs: 2
Submitted songs: 2
```

### Manual Editing Process
```bash
# 1. Watch the recorded TUG session video
# 2. Note when each song actually starts
# 3. Edit music/scripts/Music Links.txt:

# Before (generated template):
0:00:00 group (Amazing Grace) https://tuesdayukes.org/music/PDFs/Amazing_Grace.pdf
0:00:00 John Smith (House of the Rising Sun) https://tuesdayukes.org/music/PDFs/House_Rising_Sun.pdf
0:00:00 group (Puff the Magic Dragon) https://tuesdayukes.org/music/PDFs/Puff_Magic_Dragon.pdf
0:00:00 Mary Johnson (Blackbird) https://tuesdayukes.org/music/PDFs/Blackbird.pdf

# After (edited with real timestamps, sorted chronologically):
0:00:00 group (Amazing Grace) https://tuesdayukes.org/music/PDFs/Amazing_Grace.pdf
0:03:15 Mary Johnson (Blackbird) https://tuesdayukes.org/music/PDFs/Blackbird.pdf
0:06:45 group (Puff the Magic Dragon) https://tuesdayukes.org/music/PDFs/Puff_Magic_Dragon.pdf
0:09:30 John Smith (House of the Rising Sun) https://tuesdayukes.org/music/PDFs/House_Rising_Sun.pdf
```

### YouTube Integration
Copy the edited content to YouTube video description for automatic chapter markers.

---

*For more information about the TUG website structure and automation, see [CI/CD Documentation](docs/CICD_README.md).*
