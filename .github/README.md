# Tuesday Ukulele Group (TUG) Repository

Welcome to the Tuesday Ukulele Group's central repository! This repository contains the website, music library, and automated tools for Austin's premier ukulele community.

🎵 **Website**: [tuesdayukes.org](https://tuesdayukes.org/)  
🏠 **Location**: Austin, Texas  
📅 **Meeting**: Every Tuesday  

## What's Inside

This repository contains:
- **Website source code** - HTML pages, styling, and interactive features
- **Music library** - ChordPro files, PDFs, and song collections  
- **Automated workflows** - CI/CD for PDF generation and website deployment
- **Utility scripts** - Tools for managing timestamps, easy song filtering, and more

## 📚 Documentation Table of Contents

### Core Documentation
- **[Website CI/CD & PDF Generation](../docs/CICD_README.md)** - How automated PDF generation and website deployment works
- **[Music Library Organization](../music/ChordPro/README.md)** - How the ChordPro music files are organized

### User Guides & Tools
- **[Easy Songs System](../EASY_SONGS_README.md)** - How to mark and filter beginner-friendly songs
- **[Extract Songs Script](../EXTRACT_SONGS_README.md)** - Tool for extracting song data from website HTML
- **[Format Index Script](../FORMATINDEX_README.md)** - Convert timestamped song data to HTML for video indexes
- **[Timestamp Updater](../TIMESTAMP_UPDATE_README.md)** - Script documentation for updating version timestamps
- **[Windows Shortcuts](../SHORTCUT_INSTRUCTIONS.md)** - Desktop shortcuts for common tasks

## 🚀 Quick Start

### For Website Visitors
Visit [tuesdayukes.org](https://tuesdayukes.org/) to:
- Browse our song collection
- Download PDFs and ChordPro files
- Find information about our group
- Watch performance videos

### For Contributors
1. **Clone the repository**
   ```bash
   git clone https://github.com/TuesdayUkes/TUG.git
   cd TUG
   ```

2. **Add new songs**: Place `.chopro` files in `music/ChordPro/` - PDFs will be generated automatically

3. **Mark easy songs**: Create `.easy` files next to beginner-friendly songs

4. **Update website**: Modify HTML files and push - deployment is automatic

## 🎯 Key Features

### Automated Systems
- **🤖 PDF Generation**: ChordPro files automatically generate PDFs on commit
- **🚀 Website Deployment**: Changes automatically deploy to GitHub Pages  
- **🔄 Smart Timestamps**: Automatic cache-busting for updated files
- **🎯 Easy Song Filtering**: Mark and filter beginner-friendly songs

### Music Library
- **800+ Songs**: Extensive collection of ukulele arrangements
- **Multiple Formats**: ChordPro source files and generated PDFs
- **Organized Collections**: Seasonal songbooks and themed collections
- **Search & Filter**: Real-time search with easy song filtering

### Website Features
- **Responsive Design**: Mobile-friendly interface
- **Interactive Search**: Find songs quickly with live filtering
- **Performance Videos**: Links to member recordings
- **Resource Links**: External ukulele learning resources

## 🛠️ Technical Stack

- **Frontend**: HTML5, CSS3, JavaScript (vanilla)
- **Music Format**: ChordPro (.chopro/.cho files)
- **PDF Generation**: genpdf-butler
- **CI/CD**: GitHub Actions
- **Hosting**: GitHub Pages
- **Version Control**: Git/GitHub

## 📈 Repository Stats

- **Songs**: 800+ ChordPro files
- **Collections**: 15+ seasonal songbooks
- **Automated Workflows**: 2 GitHub Actions
- **Utility Scripts**: 5+ Python tools
- **Documentation**: 6 comprehensive guides

## 🤝 Contributing

We welcome contributions from TUG members and the broader ukulele community!

### Adding Songs
1. Create `.chopro` files using ChordPro format
2. Place in appropriate `music/ChordPro/` subfolder
3. Commit and push - PDFs generate automatically
4. Mark as easy with `.easy` file if beginner-friendly

### Improving Website
1. Edit HTML/CSS files as needed
2. Test locally using browser
3. Commit and push - deployment is automatic

### Reporting Issues
- Use GitHub Issues for bugs or feature requests
- Check existing documentation first
- Include specific examples when possible

## 📞 Contact

- **Website**: [tuesdayukes.org](https://tuesdayukes.org/)
- **GitHub**: [TuesdayUkes/TUG](https://github.com/TuesdayUkes/TUG)
- **Issues**: [Report problems or suggestions](https://github.com/TuesdayUkes/TUG/issues)

---

*This repository is maintained by the Tuesday Ukulele Group, Austin, Texas. All music arrangements are used with appropriate permissions or are in the public domain.*
