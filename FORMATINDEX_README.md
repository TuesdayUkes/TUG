# Format Index Script Documentation

The `formatIndex.py` script (located in `music/scripts/`) converts timestamped song data into an HTML table with clickable YouTube timestamps and PDF links.

## 🎯 Purpose

This script creates a complete HTML video index with interactive features:

1. **YouTube Integration** - Converts timestamps into clickable YouTube links that jump to specific video moments
2. **PDF Links** - Transforms song titles into clickable links to sheet music PDFs
3. **HTML Table Generation** - Creates a complete formatted table for website integration

### Workflow Position
```
extract_songs.py → manual editing → formatindex.py → HTML output → website integration
```

## 📥 Input Requirements

### Required File
- **`music_links.txt`** - Timestamped song data file
- Must be manually edited with accurate timestamps
- Songs should be sorted in chronological order of video appearance

### Expected Input Format
```
0:00 group (Opening Song) https://tuesdayukes.org/music/PDFs/Opening_Song.pdf
2:45 John Smith (My Favorite Song) https://tuesdayukes.org/music/PDFs/My_Favorite.pdf
1:05:30 group (Closing Song) https://tuesdayukes.org/music/PDFs/Closing_Song.pdf
```

### Input Structure
- **Timestamp** - Video time when song starts (MM:SS or H:MM:SS format)
- **Submitter** - Who suggested/led the song ("group" for group songs)  
- **Title** - Song title in parentheses
- **URL** - Link to PDF on tuesdayukes.org

### Supported Timestamp Formats
- **MM:SS** - Minutes:Seconds (e.g., `2:45`, `15:30`)
- **H:MM:SS** - Hours:Minutes:Seconds (e.g., `1:05:30`, `2:15:45`)

## 📤 Output

### HTML Table Format
The script generates a complete HTML table with clickable timestamps and PDF links:

```html
<table style="font-family: Arial, Helvetica, sans-serif; font-size: large;">
<tr>
    <td><a href="https://youtube.com/watch?v=VIDEO_ID?t=0m0s">0:00</a></td>
    <td>group</td>
    <td><a href="https://tuesdayukes.org/music/PDFs/Opening_Song.pdf">Opening Song</a></td>
</tr>
<tr>
    <td><a href="https://youtube.com/watch?v=VIDEO_ID?t=2m45s">2:45</a></td>
    <td>John Smith</td>
    <td><a href="https://tuesdayukes.org/music/PDFs/My_Favorite.pdf">My Favorite Song</a></td>
</tr>
<tr>
    <td><a href="https://youtube.com/watch?v=VIDEO_ID?t=1h5m30s">1:05:30</a></td>
    <td>group</td>
    <td><a href="https://tuesdayukes.org/music/PDFs/Closing_Song.pdf">Closing Song</a></td>
</tr>
</table>
```

### Output File
- **VideoIndex.html** - Complete HTML table written to current directory
- **Interactive Features** - Clickable timestamps jump to YouTube video moments
- **PDF Access** - Song titles link directly to sheet music PDFs

## 🚀 Usage

### Required Arguments
```bash
# Basic usage requires input file and YouTube link
python music/scripts/formatIndex.py inputfile.txt "https://youtube.com/watch?v=VIDEO_ID"

# Example with actual YouTube link
python music/scripts/formatIndex.py extracted_music_links.txt "https://youtube.com/watch?v=dQw4w9WgXcQ"
```

### Command Line Arguments
- **inputFilename** - Path to the timestamped song data file
- **youtubeLink** - Full YouTube video URL for timestamp linking

### Integration Workflow
```bash
# 1. Generate initial template
python extract_songs.py

# 2. Manually edit timestamps and sort chronologically
nano extracted_music_links.txt

# 3. Convert to HTML with YouTube link
python music/scripts/formatIndex.py extracted_music_links.txt "https://youtube.com/watch?v=VIDEO_ID"

# 4. Use generated VideoIndex.html file
# - Copy content for website integration
# - Upload to website or paste into existing pages
```

## 🔧 Technical Details

### Dependencies
- **Python 3.x** - Standard library
- **argparse** - Command-line argument parsing
- **re** - Regular expressions for text processing
- **pathlib** - File path handling

### Core Processing Logic

#### Regex Transformations
The script uses sophisticated regex patterns to transform input text:

1. **Player Name Extraction**: `(\d+ +)(.*)( \()`
   - Wraps submitter names in `<td></td>` tags

2. **Hour-Format Timestamps**: `^(\d+):(\d+):(\d+)`
   - Converts `1:05:30` to `<a href="youtube.com?t=1h5m30s">1:05:30</a>`

3. **Minute-Format Timestamps**: `^(\d+):(\d+)`
   - Converts `2:45` to `<a href="youtube.com?t=2m45s">2:45</a>`

4. **PDF Link Generation**: `\(([^)]*)\) (https?:.*)`
   - Converts `(Song Title) URL` to `<a href="URL">Song Title</a>`

5. **Title Cleanup**: `\((.*)\)$`
   - Handles remaining song titles in parentheses

### Special Character Handling
- Escapes single quotes/apostrophes for JavaScript compatibility
- Maintains proper HTML formatting throughout processing

## 📋 Integration Points

### index.html (Current Video)
```html
<!-- Most recent TUG session video index -->
<h2>Latest Session - November 12, 2025</h2>
<table id="current-video-table">
    <tr><th>Time</th><th>Submitter</th><th>Song</th></tr>
    <!-- INSERT FORMATINDEX.PY OUTPUT HERE -->
</table>
```

### VideoIndex History.html (All Videos)
```html
<!-- Historical archive of all TUG Zoom recordings -->
<h3>Session: November 12, 2025</h3>
<table class="video-session-table">
    <tr><th>Time</th><th>Submitter</th><th>Song</th></tr>
    <!-- INSERT FORMATINDEX.PY OUTPUT HERE -->
</table>
```

## 📊 Use Cases

### Website Maintenance
```bash
# After each TUG Zoom session:
# 1. Extract songs from website
python extract_songs.py

# 2. Watch video, update timestamps
# Edit extracted_music_links.txt manually

# 3. Generate HTML for website
python formatindex.py extracted_music_links.txt

# 4. Update both index pages
# Paste HTML into index.html (current)
# Paste HTML into VideoIndex History.html (archive)
```

### Archive Management
- **Current Session** - Replace content in `index.html`
- **Historical Record** - Append new session to `VideoIndex History.html`
- **Consistency** - Ensures uniform formatting across all video indexes

### Quality Assurance
```bash
# Validate HTML output before website integration
python formatindex.py music_links.txt --validate

# Check for missing PDFs or broken links
python formatindex.py music_links.txt --check-links
```

## 🔍 Troubleshooting

### Common Issues

#### "File not found: music_links.txt"
```bash
# Solution: Ensure input file exists
ls music_links.txt
# Or specify correct filename
python formatindex.py extracted_music_links.txt
```

#### "Invalid timestamp format"
```bash
# Check timestamp format in input file
# Valid: 0:00, 2:45, 1:23:45
# Invalid: 0, 2.45, 1-23-45
```

#### "Missing song title or URL"
```bash
# Verify each line has complete format:
# timestamp submitter (title) url
# Example: 2:45 John Smith (Amazing Grace) https://tuesdayukes.org/...
```

### Input Validation
The script should handle:
- Various timestamp formats (MM:SS, H:MM:SS)
- Special characters in song titles
- Different URL formats
- Missing or malformed entries

## 🔗 Related Tools

### TUG Ecosystem Integration
- **extract_songs.py** - Generates initial template for formatindex.py
- **index.html** - Receives formatted HTML output
- **VideoIndex History.html** - Archives all formatted sessions
- **YouTube Videos** - Source material for timestamp data

### Workflow Dependencies
1. **Video Recording** - TUG Zoom sessions recorded
2. **Song Extraction** - `extract_songs.py` creates template
3. **Manual Editing** - User adds accurate timestamps
4. **HTML Generation** - `formatindex.py` creates website-ready HTML
5. **Website Integration** - Manual paste into HTML files

## 📝 Example Session

### Input File (music_links.txt)
```
0:00 group (Welcome Song) https://tuesdayukes.org/music/PDFs/Welcome.pdf
3:15 Mary Johnson (Blackbird) https://tuesdayukes.org/music/PDFs/Blackbird.pdf
6:45 group (Puff the Magic Dragon) https://tuesdayukes.org/music/PDFs/Puff_Magic_Dragon.pdf
9:30 John Smith (House of the Rising Sun) https://tuesdayukes.org/music/PDFs/House_Rising_Sun.pdf
```

### Script Execution
```bash
$ python music/scripts/formatIndex.py music_links.txt "https://youtube.com/watch?v=dQw4w9WgXcQ"

# Script processes the file and creates VideoIndex.html
# No console output - check VideoIndex.html file for results
```

### Generated VideoIndex.html Content
```html
<table style="font-family: Arial, Helvetica, sans-serif; font-size: large;">
<tr>
    <td><a href="https://youtube.com/watch?v=dQw4w9WgXcQ?t=0m0s">0:00</a></td>
    <td>group</td>
    <td><a href="https://tuesdayukes.org/music/PDFs/Welcome.pdf">Welcome Song</a></td>
</tr>
<tr>
    <td><a href="https://youtube.com/watch?v=dQw4w9WgXcQ?t=3m15s">3:15</a></td>
    <td>Mary Johnson</td>
    <td><a href="https://tuesdayukes.org/music/PDFs/Blackbird.pdf">Blackbird</a></td>
</tr>
<tr>
    <td><a href="https://youtube.com/watch?v=dQw4w9WgXcQ?t=6m45s">6:45</a></td>
    <td>group</td>
    <td><a href="https://tuesdayukes.org/music/PDFs/Puff_Magic_Dragon.pdf">Puff the Magic Dragon</a></td>
</tr>
<tr>
    <td><a href="https://youtube.com/watch?v=dQw4w9WgXcQ?t=9m30s">9:30</a></td>
    <td>John Smith</td>
    <td><a href="https://tuesdayukes.org/music/PDFs/House_Rising_Sun.pdf">House of the Rising Sun</a></td>
</tr>
</table>
```

### Website Integration
Use the generated `VideoIndex.html` file:
1. **Copy Content** - Open VideoIndex.html and copy the complete table
2. **Website Integration** - Paste into your video index pages
3. **Interactive Features** - Users can click timestamps to jump to YouTube moments
4. **PDF Access** - Users can click song titles to download sheet music

---

*For information about generating the input file, see [Extract Songs Documentation](EXTRACT_SONGS_README.md).*
