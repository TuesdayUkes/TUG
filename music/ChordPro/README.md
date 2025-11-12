# Music Library Organization

This directory contains the Tuesday Ukulele Group's complete music library in ChordPro format.

## 📂 Directory Structure

### Current Organization
All music files are organized in a centralized structure:
- **Primary Location**: `music/ChordPro/` - All ChordPro source files
- **Generated PDFs**: `music/PDFs/` - Auto-generated PDF files (mirrors ChordPro structure)
- **Collections**: Seasonal and themed subfolders for organization

### Folder Categories

#### Seasonal Collections
- **`Spring YYYY/`** - Spring songbook collections
- **`Summer YYYY/`** - Summer songbook collections  
- **`Fall YYYY/`** - Fall songbook collections
- **`Winter YYYY-YY/`** - Winter songbook collections

#### Special Collections
- **`TUG Archive/`** - Historical songs and classics
- **`Kevin's Memorial/`** - Memorial collection
- **`Two Chord Songs/`** - Beginner-friendly songs
- **`YYYY/`** - Current year monthly additions

## 🎵 File Formats

### ChordPro Files (`.chopro`, `.cho`)
- **Purpose**: Source files with lyrics and chord notation
- **Format**: Industry-standard ChordPro markup
- **Processing**: Automatically generates PDFs when committed

### Example ChordPro Format
```chordpro
{title: Amazing Grace}
{artist: Traditional}
{key: G}

A[G]mazing [G7]grace how [C]sweet the [G]sound
That [G]saved a [D]wretch like [G]me
I [G]once was [G7]lost but [C]now I'm [G]found
Was [G]blind but [D]now I [G]see
```

## 🏷️ File Tagging System

### Easy Song Markers (`.easy`)
- **Purpose**: Mark beginner-friendly songs
- **Usage**: Create `.easy` file alongside song file
- **Example**: `Amazing Grace.chopro` + `Amazing Grace.easy`

### Hidden Songs (`.hide`)
- **Purpose**: Exclude songs from public listing
- **Usage**: Create `.hide` file alongside song file
- **Example**: `Work in Progress.chopro` + `Work in Progress.hide`

## 🔄 Automated Processing

### PDF Generation
1. **Trigger**: ChordPro file committed to repository
2. **Process**: genpdf-butler generates PDF automatically
3. **Output**: PDF placed in corresponding `music/PDFs/` folder
4. **Website**: Archive automatically updated

### Website Integration
- **Song Archive**: Generated automatically from ChordPro files
- **Search Function**: Indexes all songs for real-time search
- **Filtering**: Easy songs filter, version control

## 📚 Adding New Songs

### Step-by-Step Process
1. **Create ChordPro File**
   ```bash
   # Choose appropriate folder
   cd "music/ChordPro/2025/November/"
   
   # Create song file
   nano "New Song Title.chopro"
   ```

2. **Add ChordPro Content**
   - Include title, artist, key metadata
   - Add lyrics with chord annotations
   - Follow ChordPro format standards

3. **Mark as Easy (Optional)**
   ```bash
   # For beginner songs
   touch "New Song Title.easy"
   ```

4. **Commit Changes**
   ```bash
   git add "New Song Title.chopro"
   git add "New Song Title.easy"  # if applicable
   git commit -m "Add: New Song Title"
   git push
   ```

5. **Automatic Processing**
   - PDF generates automatically
   - Website updates with new song
   - Archive rebuilds with search indexing

## 🎯 Best Practices

### File Naming
- Use descriptive titles with proper capitalization
- Include artist in filename if ambiguous
- Use consistent date/version suffixes when needed

### ChordPro Content
- Include complete metadata (`{title}`, `{artist}`, `{key}`)
- Use standard chord notation
- Include capo information if applicable
- Add tempo and style hints in comments

### Organization
- Place songs in appropriate seasonal folders
- Use current year folder for new additions
- Keep related versions together

## 🔍 Finding Songs

### Search Methods
1. **Website Search**: Real-time search at [tuesdayukes.org](https://tuesdayukes.org/)
2. **File Explorer**: Browse folders by season/theme
3. **Command Line**: `find` or `grep` commands
4. **GitHub Search**: Use repository search functionality

### File Statistics
- **Total Songs**: 800+ ChordPro files
- **Collections**: 15+ organized songbooks
- **Easy Songs**: 50+ beginner-friendly marked songs
- **Formats**: ChordPro source + auto-generated PDFs

---

For technical details about automated processing, see [CI/CD Documentation](../docs/CICD_README.md).
