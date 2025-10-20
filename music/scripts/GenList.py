#! python
import subprocess
from first import first
from pathlib import Path
from posixpath import basename, splitext
import sys
import os
import argparse
from re import M
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument("musicFolder")
parser.add_argument("outputFile")
parser.add_argument("--intro", action=argparse.BooleanOptionalAction, default=True)
parser.add_argument("--genPDF", action=argparse.BooleanOptionalAction, default=False)
parser.add_argument("--forcePDF", action=argparse.BooleanOptionalAction, default=False)
parser.add_argument("--filter", choices=["none", "hidden", "timestamp"], default="timestamp",
                    help="Filter method: 'none' (show all files), 'hidden' (hide files with .hide), 'timestamp' (show newest versions only)")
args = parser.parse_args()

print("Generating Music List (this takes a few seconds)", file=sys.stderr)
print(f"Using filter method: {args.filter}", file=sys.stderr)

musicFolder = args.musicFolder
outputFile = args.outputFile
intro = args.intro
forceNewPDF = args.forcePDF
genPDF = args.genPDF
filterMethod = args.filter

now = datetime.now().strftime("%Y.%m.%d.%H.%M.%S")

# lambda filename accepts a path and returns just the filename without an extension
filename = lambda p: str(os.path.splitext(os.path.basename(p))[0])

# lambda ext is like lambda filename, except it returns the file extension
ext = lambda p: str(os.path.splitext(os.path.basename(p))[1]).lower()

def createPDFs():
  linuxpath = ["perl",
               "/home/paul/chordpro/script/chordpro.pl",
               "--config=/home/paul/chordpro/lib/ChordPro/res/config/ukulele.json",
               "--config=/home/paul/chordpro/lib/ChordPro/res/config/ukulele-ly.json"
               ]

  winpath = ["chordpro",
            "--config=Ukulele",
            "--config=Ukulele-ly"
            ]

  chordproSettings=[
    "--define=pdf:diagrams:show=top",
    "--define=settings:inline-chords=true",
    "--define=pdf:margintop=70",
    "--define=pdf:marginbottom=0",
    "--define=pdf:marginleft=20",
    "--define=pdf:marginright=20",
    "--define=pdf:headspace=50",
    "--define=pdf:footspace=10",
    "--define=pdf:head-first-only=true",
    "--define=pdf:fonts:chord:color=red",
    "--text-font=helvetica",
    "--chord-font=helvetica"
  ]

  if os.name == "nt":
    chordproSettings = winpath + chordproSettings
  else:
    chordproSettings = linuxpath + chordproSettings

  extensions = [".chopro", ".cho"]
  for p in Path(musicFolder).rglob('*'):
    if ext(p) in (extension.lower() for extension in extensions):
      pdfFile = str(os.path.splitext(str(p))[0]) + ".pdf"
      if not os.path.exists(pdfFile) or forceNewPDF:
        print("Generating " + pdfFile)
        subprocess.run(chordproSettings + [str(p)])

# A file with the extension ".hide" will prevent other files within the same
# folder with the same name (but all extensions) from being adding to the
# archive table. This is a way to conceal older versions of a song, without
# breaking old links to the older versions (the files still exist, but there
# will be no HTML links to them in the new archive table).

# A file with the extension ".easy" will mark other files within the same
# folder with the same name as "easy" songs for filtering purposes.
def getEasySongs(allFiles):
  # Use set comprehension for better performance
  return {str(os.path.splitext(f)[0]).lower() 
          for f in allFiles if ext(f).lower() == ".easy"}

def getAllGitTimestamps(files):
  """Get git timestamps for all files in one batch operation using a single git command"""
  timestamps = {}
  git_root = os.path.dirname(os.path.abspath(__file__)) + "/../.."
  
  try:
    # Convert all file paths to relative paths
    relative_files = {}
    for f in files:
      abs_path = os.path.abspath(f)
      try:
        rel_path = os.path.relpath(abs_path, git_root)
        # Normalize path separators for git
        rel_path = rel_path.replace('\\', '/')
        relative_files[rel_path] = f
      except:
        # If we can't get relative path, fall back to mtime
        timestamps[f] = int(os.path.getmtime(f))
    
    if not relative_files:
      return timestamps
    
    # Use git log with --name-only and custom format to get all timestamps at once
    # Format: timestamp on one line, then changed files on following lines
    result = subprocess.run(
      ["git", "log", "--name-only", "--pretty=format:%ct"],
      capture_output=True,
      text=True,
      cwd=git_root,
      timeout=30  # Longer timeout for the full log
    )
    
    if result.returncode == 0 and result.stdout:
      # Parse the output: timestamp followed by list of files
      lines = result.stdout.strip().split('\n')
      current_timestamp = None
      
      for line in lines:
        line = line.strip()
        if not line:
          continue
        
        # Check if line is a timestamp (all digits)
        if line.isdigit():
          current_timestamp = int(line)
        elif current_timestamp and line in relative_files:
          # This is a file path and we don't have its timestamp yet
          orig_path = relative_files[line]
          if orig_path not in timestamps:
            timestamps[orig_path] = current_timestamp
    
    # For any files not found in git log, use file modification time
    for rel_path, orig_path in relative_files.items():
      if orig_path not in timestamps:
        timestamps[orig_path] = int(os.path.getmtime(orig_path))
    
    return timestamps
    
  except Exception as e:
    print(f"Error getting git timestamps: {e}", file=sys.stderr)
    # Return mtimes as fallback for all files
    return {f: int(os.path.getmtime(f)) for f in files}

def keepNewestVersionsOnly(allFiles):
  """Keep only the newest version of each song file by extension type"""
  # Group files by base name (without extension) and extension
  from collections import defaultdict
  filesByBasenameAndExt = defaultdict(list)
  
  for f in allFiles:
    if ext(f).lower() in [".hide", ".easy"]:
      continue  # Skip marker files
    
    baseName = dictCompare(filename(f))
    extension = ext(f).lower()
    filesByBasenameAndExt[(baseName, extension)].append(f)
  
  # Collect all files that need timestamps (files with duplicates)
  filesNeedingTimestamps = []
  for (baseName, extension), files in filesByBasenameAndExt.items():
    if len(files) > 1:
      filesNeedingTimestamps.extend(files)
  
  # Get all timestamps in batch if there are any files with duplicates
  if filesNeedingTimestamps:
    print(f"Fetching git timestamps for {len(filesNeedingTimestamps)} files with duplicates...", file=sys.stderr)
    gitTimestamps = getAllGitTimestamps(filesNeedingTimestamps)
  else:
    gitTimestamps = {}
  
  # For each group, keep only the file with the newest git timestamp
  newestFiles = []
  for (baseName, extension), files in filesByBasenameAndExt.items():
    if len(files) == 1:
      newestFiles.extend(files)
    else:
      # Multiple files with same basename and extension - keep the newest
      filesWithTimestamps = []
      for f in files:
        timestamp = gitTimestamps.get(f, 0)
        filesWithTimestamps.append((timestamp, f))
      
      # Sort by timestamp (newest first) and take the first one
      filesWithTimestamps.sort(reverse=True)
      newestFile = filesWithTimestamps[0][1]
      newestFiles.append(newestFile)
      
      print(f"Multiple versions found for {baseName}{extension}:", file=sys.stderr)
      for timestamp, f in filesWithTimestamps:
        marker = "* KEPT" if f == newestFile else "  ignored"
        print(f"  {marker}: {f} (timestamp: {timestamp})", file=sys.stderr)
  
  # Add back the marker files (.hide, .easy)
  for f in allFiles:
    if ext(f).lower() in [".hide", ".easy"]:
      newestFiles.append(f)
  
  return newestFiles

def removeHiddenFiles(allFiles):
  # Use set for O(1) lookup instead of list with O(n) lookup
  hideFiles = set()
  visibleFiles = []
  
  # Single pass to collect hide files
  for f in allFiles:
    if ext(f).lower() == ".hide":
      hideFiles.add(str(os.path.splitext(f)[0]).lower())
  
  # Second pass to filter visible files
  for f in allFiles:
    basename = str(os.path.splitext(f)[0]).lower()
    if basename not in hideFiles:
      visibleFiles.append(f)

  return visibleFiles

# dictCompare removes articles that appear as the first word in a filename
articles = {'a', 'an', 'the'}  # Use set for faster lookup
def dictCompare(s):
  sWords = s.split()
  if sWords and sWords[0].lower() in articles:
    formattedS = ' '.join(sWords[1:])
  else:
    formattedS = s

  # Remove punctuation in one pass using translate
  return formattedS.translate(str.maketrans('', '', '\',\'')).lower()

with open("HTMLheader.txt", "r") as headerText:
  header = headerText.readlines()

introduction = """
<h1>Tuesday Ukes' Archive of Ukulele Songs and Chords</h1>

<section class="archive card">
<div class="archive-intro card">

<p>Whether you're a beginner ukulele player looking for easy songs or a longtime
player searching for fun songs, this is the resource for you. Here you will find
ukulele chords and chord diagrams for uke players of all levels.</p>

<p>This collection of the best ukulele songs has been built over time by members
of Austin's Tuesday Ukulele Group. </p>

<h2>Lots of Popular Songs</h2>
<p>There's a big range: Easy ukulele songs with simple chords for beginner
ukulele players with just 3 chords or 4 chords. You will find great songs by
Paul McCartney, Neil Diamond, Bob Dylan, John Denver, and Bob Marley turned into
ukulele music. More-advanced ukulele music players can find finger-stretching
chord changes and chord shapes applied to popular ukulele songs. </p>
"""

searchControls = """
<div class="search-controls">
    <h2>Search & Filter</h2>
    <input type="text" id="searchInput" placeholder="🔍 Search songs by title...">
    <div class="filter-checkbox">
        <input type="checkbox" id="easyFilter">
        <label for="easyFilter">🎵 Show only easy songs (perfect for beginners!)</label>
    </div>""" + ("""
    <div class="filter-checkbox">
        <input type="checkbox" id="showAllVersions">
        <label for="showAllVersions">🗂️ Show all versions (including older duplicates)</label>
    </div>""" if filterMethod != "none" else "") + """
    <div id="searchStats" class="search-stats" style="display: none;">
        Showing <span id="visibleCount">0</span> of <span id="totalCount">0</span> songs
    </div>
</div>
"""

searchScript = """
</div>
</section>
<script>
    const searchInput = document.getElementById('searchInput');
    const easyFilter = document.getElementById('easyFilter');
    const showAllVersions = document.getElementById('showAllVersions');
    const table = document.getElementById('dataTable');
    const rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');
    const searchStats = document.getElementById('searchStats');
    const visibleCountSpan = document.getElementById('visibleCount');
    const totalCountSpan = document.getElementById('totalCount');

    // Set total count
    totalCountSpan.textContent = rows.length;

    function updateSearchStats(visibleCount) {
        visibleCountSpan.textContent = visibleCount;
        searchStats.style.display = (searchInput.value || easyFilter.checked || (showAllVersions && showAllVersions.checked)) ? 'block' : 'none';
    }

    function filterRows() {
        const searchFilter = searchInput.value.toLowerCase();
        const easyOnly = easyFilter.checked;
        const showAll = showAllVersions ? showAllVersions.checked : true;
        let visibleCount = 0;

        // Add loading effect
        table.classList.add('table-loading');

        setTimeout(() => {
            for (let i = 0; i < rows.length; i++) {
                let rowText = rows[i].textContent.toLowerCase();
                let isEasy = rows[i].classList.contains('easy-song');

                let showBySearch = !searchFilter || rowText.includes(searchFilter);
                let showByEasy = !easyOnly || isEasy;

                const shouldShow = showBySearch && showByEasy;
                rows[i].style.display = shouldShow ? '' : 'none';

                if (shouldShow) {
                    visibleCount++;
                    
                    // Show/hide additional file versions within this row
                    const additionalVersions = rows[i].querySelectorAll('.additional-version');
                    additionalVersions.forEach(link => {
                        link.style.display = showAll ? '' : 'none';
                    });
                }
            }

            updateSearchStats(visibleCount);
            table.classList.remove('table-loading');
        }, 50);
    }

    // Enhanced input with debouncing
    let searchTimeout;
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(filterRows, 300);
    });

    easyFilter.addEventListener('change', filterRows);
    if (showAllVersions) {
        showAllVersions.addEventListener('change', filterRows);
    }

    // Initialize with default filtering based on server-side filter method
    // Hide additional versions by default unless filter method was "none"
    const defaultFilterMethod = '""" + filterMethod + """';
    if (defaultFilterMethod !== 'none') {
        // Hide additional file versions by default
        const additionalVersions = document.querySelectorAll('.additional-version');
        additionalVersions.forEach(link => {
            link.style.display = 'none';
        });
    }
    
    // Update initial stats
    filterRows();
</script>
"""

if genPDF:
  createPDFs()

# Pre-convert extensions to lowercase for faster comparison
extensions = {".pdf", ".chopro", ".cho", ".mscz", ".urltxt", ".hide", ".easy"}
allFiles = []
# Use a single rglob call and filter more efficiently
for p in Path(musicFolder).rglob('*'):
  if p.suffix.lower() in extensions:
    allFiles.append(p.as_posix())

# Determine which files should be filtered out for JavaScript handling
# Always include all files in HTML, but mark filtered ones with CSS classes
visibleFiles = allFiles

# Determine which files would be filtered by timestamp filtering
newestFiles = keepNewestVersionsOnly(allFiles)
hiddenByTimestamp = set(allFiles) - set(newestFiles)

# Determine which files would be filtered by .hide files  
visibleByHide = removeHiddenFiles(allFiles)
hiddenByHideFiles = set(allFiles) - set(visibleByHide)

# Apply the selected filtering method for the default view state
if filterMethod == "none":
  defaultHiddenFiles = set()
elif filterMethod == "hidden":
  defaultHiddenFiles = hiddenByHideFiles
elif filterMethod == "timestamp":
  # Files hidden by timestamp OR by .hide files
  defaultHiddenFiles = hiddenByTimestamp | hiddenByHideFiles
else:
  # Fallback to timestamp method if somehow an invalid value gets through
  defaultHiddenFiles = hiddenByTimestamp | hiddenByHideFiles

easySongs = getEasySongs(allFiles)

# return the first file that matches basename (there should be only zero or one
# matches). Return None if no matches found.
def findMatchingBasename(files, basename):
  return first((f for f in files if dictCompare(f[0]) == dictCompare(filename(basename))))

# allTitles will be an array of arrays. Each element's [0] entry will be the
# song title. The other entries will be file paths that contain that title.
# Use dictionary for faster lookup, then convert to list
titleDict = {}
for p in visibleFiles:
  title = filename(p)
  titleKey = dictCompare(title)
  if titleKey in titleDict:
    titleDict[titleKey].append(str(p))
  else:
    titleDict[titleKey] = [title, str(p)]

allTitles = list(titleDict.values())

downloadExtensions = [".cho", ".chopro"]
sortedTitles = sorted(allTitles, key=(lambda e: dictCompare(e[0]).casefold()))
with open(outputFile, "w", encoding='utf-8') as htmlOutput:
  htmlOutput.writelines(header)
  if intro:
    htmlOutput.writelines(introduction)
  htmlOutput.writelines(searchControls)
  htmlOutput.write('<table id="dataTable">')
  htmlOutput.write("<thead>\n")
  htmlOutput.write("<tr><th>#</th><th>Song Title</th><th>Downloads</th></tr>\n")
  htmlOutput.write("</thead>\n")
  htmlOutput.write("<tbody>\n")
  row_number = 1
  for f in sortedTitles:
    try:
      # Check if this song is marked as easy
      isEasy = any(str(os.path.splitext(file)[0]).lower() in easySongs for file in f[1:])
      
      # Check if this song has additional versions that were filtered out
      # This means there are files available when "show all versions" is checked
      hasAdditionalVersions = any(file in defaultHiddenFiles for file in f[1:])
      
      # Only mark as hidden-version if there are additional filtered versions available
      # This helps users know they can see more by checking "show all versions"
      isHiddenVersion = hasAdditionalVersions
      
      # Build CSS classes
      cssClasses = []
      if isEasy:
        cssClasses.append("easy-song")
      if isHiddenVersion:
        cssClasses.append("hidden-version")
      
      classAttr = f' class="{" ".join(cssClasses)}"' if cssClasses else ''

      htmlOutput.write(f"<tr{classAttr}>")
      # first table column contains the row number
      htmlOutput.write(f"  <td>{row_number}</td>")
      # second table column contains the song title (f[0])
      htmlOutput.write(f"  <td>{f[0]}</td>\n<td>")
      # the remainder of f's elements are files that match the title in f[0]
      # Sort the files to ensure consistent ordering across operating systems
      # Sort by extension first, then by the complete normalized path
      sorted_files = sorted(f[1:], key=lambda x: (ext(x), x.lower().replace('\\', '/')))
      for i in sorted_files:
        # Skip .easy and .hide marker files - they shouldn't appear as downloads
        if ext(i) in [".easy", ".hide"]:
          continue
        
        # Determine if this file is hidden by the current filter method
        fileClass = ' class="additional-version"' if i in defaultHiddenFiles else ''
        
        if ext(i) == ".urltxt":
          with open(i, "r") as urlFile:
            label = urlFile.readline().strip()
            address = urlFile.readline().strip()
          htmlOutput.write(f"<a href=\"{address}\" target=\"_blank\"{fileClass}>{label}</a><br>\n")
        elif ext(i) in downloadExtensions:
          htmlOutput.write(f" <a href=\"{str(i).replace(' ','%20')}?v={now}\" download=\"{filename(i)}{ext(i)}\" target=\"_blank\"{fileClass}>{ext(i)}</a><br>\n")
        else:
          htmlOutput.write(f"  <a href=\"{str(i).replace(' ','%20')}?v={now}\" target=\"_blank\"{fileClass}>{ext(i)}</a><br>\n")

      # close each table row (and the table data containing file links)
      htmlOutput.write("</td></tr>\n")
      row_number += 1
    except:
      print(f"failed to write {f[1:]}")

  #close the table etc.
  htmlOutput.write("</tbody>")
  htmlOutput.write("</table>")
  htmlOutput.write(searchScript)
  htmlOutput.write("</div>\n")
  htmlOutput.write("</div>\n")
  htmlOutput.write("</body>\n")

print("Done!", file=sys.stderr)
