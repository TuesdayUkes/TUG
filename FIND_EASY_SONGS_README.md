# Find Easy Songs Script Documentation

The `find_easy_songs.py` script analyzes ChordPro files to identify songs with 3 or fewer unique chords and automatically creates `.easy` marker files for them.

## 🎯 Purpose

This script automates the process of marking beginner-friendly songs by:

1. **Chord Analysis** - Scans all ChordPro files to count unique chords
2. **Easy Song Identification** - Finds songs with 3 or fewer chords (ideal for beginners)
3. **Automatic Marking** - Creates `.easy` marker files for qualifying songs
4. **Comprehensive Reporting** - Provides detailed analysis and statistics

### Target Audience
- **New ukulele players** seeking songs with simple chord progressions
- **TUG administrators** maintaining the easy songs collection
- **Website users** using the easy songs filter feature

## 📥 Input Requirements

### Directory Structure
- **`music/ChordPro/`** - Must contain ChordPro files with `.chopro` extension
- **Recursive scanning** - Processes all subdirectories automatically

### ChordPro File Format
The script expects standard ChordPro format with chords in square brackets:
```chordpro
{title: Amazing Grace}
{artist: Traditional}

A[G]mazing [G7]grace how [C]sweet the [G]sound
That [G]saved a [D]wretch like [G]me
```

## 📤 Output

### .easy Marker Files
- **Purpose**: Mark songs as beginner-friendly for website filtering
- **Location**: Same directory as corresponding `.chopro` file
- **Naming**: `songname.easy` (matches `songname.chopro`)
- **Content**: Empty files that serve as markers

### Console Output
- **Real-time progress**: Shows each song being marked with chord count
- **Summary statistics**: Total files, easy songs found, new markers created
- **Detailed listing**: All easy songs sorted by chord count with file paths

## 🚀 Usage

### Basic Usage
```bash
# Navigate to TUG directory
cd /path/to/TUG

# Run the analysis
python find_easy_songs.py
```

### Expected Output
```bash
Found 1467 ChordPro files to analyze...
✅ Created .easy marker for: Eco Packrat.chopro (3 chords: A, D, G)
✅ Created .easy marker for: Texas Cookin.chopro (1 chords: G)
✅ Created .easy marker for: Buffalo Gals.chopro (2 chords: A7, D)

📊 SUMMARY:
Total ChordPro files analyzed: 1467
Songs with 3 or fewer chords: 250
Already had .easy markers: 61
New .easy markers created: 189
Errors encountered: 0
```

## 🔧 Technical Details

### Chord Extraction Algorithm
The script uses sophisticated regex patterns to identify chords:

```python
# Find all chord patterns in square brackets
chord_pattern = r'\[([^\]]+)\]'
```

### Filtering Logic
- **Valid chords**: Single words without spaces (e.g., `G`, `Am7`, `C#dim`)
- **Excluded content**: ChordPro directives (`{t:`, `{c:`, etc.)
- **Unique counting**: Each chord counted only once per song

### Difficulty Thresholds
- **1 chord**: Super easy (rare but perfect for absolute beginners)
- **2 chords**: Very easy (classic simple songs)
- **3 chords**: Easy (most common beginner songs)
- **4+ chords**: Not marked as easy

## 📊 Use Cases

### Website Integration
```bash
# Mark all easy songs for website filtering
python find_easy_songs.py

# Website automatically detects .easy files and shows "Easy Songs" filter
# Users can filter song archive to show only beginner-friendly songs
```

### Curriculum Development
- **Beginner classes**: Use 1-2 chord songs for first lessons
- **Intermediate progression**: Graduate to 3-chord songs
- **Practice material**: Organized by difficulty level

### Quality Assurance
```bash
# Re-run to check for new easy songs after adding ChordPro files
python find_easy_songs.py

# Review songs that weren't marked to ensure chord analysis was accurate
```

## 🎵 Song Categories

### Super Easy (1 chord)
Perfect for absolute beginners:
- **Texas Cookin** (G)
- **El Camino** (A)
- **Run Through the Jungle** (Dm)

### Very Easy (2 chords)
Classic simple progressions:
- **Buffalo Gals** (A7, D)
- **Iko Iko** (C, F)
- **Dream Baby** (C, G7)

### Easy (3 chords)
Common beginner progressions:
- **Amazing Grace** (C, F, G7)
- **Jambalaya** (C, F, G)
- **Bad Moon Rising** (C, D, G)

## 🔍 Troubleshooting

### Common Issues

#### "ChordPro directory not found"
```bash
# Solution: Ensure you're in the TUG root directory
ls music/ChordPro/
# Should show ChordPro files and folders
```

#### "No songs found"
- Check ChordPro file format - chords must be in `[chord]` brackets
- Verify files have `.chopro` extension
- Ensure files contain actual chord notations

#### "Error reading file"
- Check file encoding (should be UTF-8)
- Verify file permissions
- Look for corrupted or binary files

### Manual Review
Some songs may need manual review if:
- Complex chord variations aren't recognized
- Song has easy sections but difficult bridges
- Chord notation uses non-standard formats

## 🔗 Related Tools

### TUG Ecosystem Integration
- **Website Filter**: Uses `.easy` files for "Easy Songs" filter
- **PDF Generation**: Easy songs get special handling in PDF workflow
- **create_urltxt_files.py**: Creates YouTube links specifically for easy songs
- **Song Archive**: Displays easy song indicators

### Workflow Integration
1. **Add new ChordPro files** → Repository
2. **Run find_easy_songs.py** → Analyze and mark easy songs
3. **Website rebuild** → Easy songs appear in filtered results
4. **User experience** → Beginners can find appropriate songs

## 📝 Example Session

### Full Analysis Run
```bash
$ python find_easy_songs.py
Found 1467 ChordPro files to analyze...
✅ Created .easy marker for: Eco Packrat.chopro (3 chords: A, D, G)
✅ Created .easy marker for: It's All Going to Pot.chopro (3 chords: C, D, G)
✅ Created .easy marker for: Texas Cookin.chopro (1 chords: G)
✅ Created .easy marker for: O Death.chopro (2 chords: Am, Dm)
...

📊 SUMMARY:
Total ChordPro files analyzed: 1467
Songs with 3 or fewer chords: 250
Already had .easy markers: 61
New .easy markers created: 189
Errors encountered: 0

🎵 EASY SONGS (3 or fewer chords):
  1 chords - Kevin's Memorial\Texas Cookin.chopro (G) - ✅ marked
  2 chords - Fall 2022\O Death.chopro (Am, Dm) - ✅ marked
  3 chords - Eco Packrat.chopro (A, D, G) - ✅ marked
  ...
```

### Impact Assessment
- **189 new easy songs** marked for beginners
- **Total easy collection**: 250 songs across all difficulty levels
- **Coverage improvement**: Significantly expanded beginner-friendly options

---

*For information about creating YouTube links for easy songs, see [Create URL Text Files Documentation](CREATE_URLTXT_README.md).*
