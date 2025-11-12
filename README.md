# TUG - Technical Documentation

This is the technical documentation for the Tuesday Ukulele Group repository.

> **Note**: The main repository introduction is displayed from [.github/README.md](.github/README.md) on the GitHub homepage.

## 📂 Repository Structure

```
TUG/
├── .github/
│   ├── README.md           # Main repository introduction (displayed on GitHub)
│   └── workflows/          # GitHub Actions workflows
├── docs/
│   └── CICD_README.md      # CI/CD and automation documentation  
├── music/
│   ├── ChordPro/           # Source ChordPro files (.chopro, .cho)
│   └── PDFs/               # Auto-generated PDF files
├── styles/                 # Website CSS files
├── *.html                  # Website pages
├── EASY_SONGS_README.md    # Easy song filtering system
├── TIMESTAMP_UPDATE_README.md  # Timestamp update tools
└── SHORTCUT_INSTRUCTIONS.md    # Windows shortcuts setup
```

## � Documentation Links

### Primary Documentation
- **[Repository Introduction](.github/README.md)** - Main README displayed on GitHub
- **[CI/CD & Workflows](docs/CICD_README.md)** - Automated systems documentation
- **[Music Library](music/ChordPro/README.md)** - Music organization and ChordPro files

### User Guides
- **[Easy Songs System](EASY_SONGS_README.md)** - Beginner song filtering
- **[Extract Songs Script](EXTRACT_SONGS_README.md)** - Website song data extraction tool
- **[Format Index Script](FORMATINDEX_README.md)** - Convert song timestamps to HTML for video indexes
- **[Timestamp Tools](TIMESTAMP_UPDATE_README.md)** - Version timestamp management  
- **[Windows Shortcuts](SHORTCUT_INSTRUCTIONS.md)** - Desktop shortcuts for common tasks

## 🚀 Quick Commands

### Development
```bash
# Clone repository
git clone https://github.com/TuesdayUkes/TUG.git

# Add new song (example)
cd "music/ChordPro/2025/November/"
nano "Song Title.chopro"

# Mark as easy song
touch "Song Title.easy"

# Commit changes
git add "Song Title.chopro" "Song Title.easy"
git commit -m "Add: Song Title"
git push
```

### Automated Processing
- **PDF Generation**: Automatic on ChordPro file commits
- **Website Deployment**: Automatic on content changes
- **Archive Updates**: Automatic with new song additions

## 🎯 For Developers

### Key Files
- **`music/scripts/GenList.py`** - Song archive generator
- **`update_timestamps.py`** - Version timestamp updater
- **`.github/workflows/`** - CI/CD automation

### Testing Locally
```bash
# Serve website locally
python -m http.server 8000
# Visit http://localhost:8000

# Generate song archive
python music/scripts/GenList.py music ukulele-song-archive.html --intro
```

---

*For the complete repository introduction and user guide, see [.github/README.md](.github/README.md)*
