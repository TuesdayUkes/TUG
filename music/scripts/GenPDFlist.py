from pathlib import Path
from posixpath import basename, splitext
import sys
import os
import argparse
from re import M
from datetime import datetime

parser = argparse.ArgumentParser()
parser.add_argument("musicFolder")
args = parser.parse_args()

print("Generating Music List (this takes a few seconds)", file=sys.stderr)

musicFolder = args.musicFolder

now = datetime.now().strftime("%Y.%m.%d.%H.%M.%S")

# lambda l accepts a path and returns just the filename without an extension
l = lambda p: str(os.path.splitext(os.path.basename(p))[0])

# lambda ext is like lambda l, except it returns the file extension
ext = lambda p: str(os.path.splitext(os.path.basename(p))[1]).lower()

# dictCompare removes articles that appear as the first word in a filename
articles = ['a', 'an', 'the']
def dictCompare(s):
  formattedS = ''
  sWords = s.split()
  if sWords[0].lower() in articles:
    formattedS = ' '.join(sWords[1:])
  else:
    formattedS = s

  # Remove punctuation
  formattedS = formattedS.replace('\'','')
  formattedS = formattedS.replace(',','')

  return formattedS.lower()

with open(musicFolder + "/scripts/HTMLheader.txt", "r") as headerText:
  header = headerText.readlines()

header += """
<h1>TUG's Music Archive</h1>
<p>Pro tip: use your web browser's search function! Type CTRL-F (Command+F on the Mac) and type a portion of a song title.</p>
"""

extensions = [".PDF", ".chopro", ".cho", ".mscz", ".urltxt"]
allFiles = []
for p in Path(musicFolder).rglob('*'):
  if ext(p) in (extension.lower() for extension in extensions):
    allFiles.append(p)

def findMatchingBasename(files, basename):
  matches = [f for f in files if dictCompare(f[0]) == dictCompare(l(basename))]
  if matches:
    # matches should never have more than one entry, but there is no check to
    # verify that claim. The only way we intend to add a new file path to
    # "files" is when no entry already has a file with the same basename.
    return matches[0]
  else:
    return None

# allTitles will be an array of arrays. Each element's [0] entry will be the
# song title. The other entries will be file paths that contain that title.
allTitles = []
for p in allFiles:
  matchingTitle = findMatchingBasename(allTitles, p)
  if matchingTitle:
    # add a newly found file for a previously found song
    matchingTitle.append(str(p))
  else:
    # found a song for the first time. Add the title and the filename
    allTitles.append([l(p), str(p)])

downloadExtensions = [".cho", ".chopro"]
sortedTitles = sorted(allTitles, key=(lambda e: dictCompare(e[0]).casefold()))
with open("PDFLinks.html", "w") as htmlOutput:
  htmlOutput.writelines(header)
  htmlOutput.write("<table>")
  for f in sortedTitles:
    try:
      htmlOutput.write("<tr>")
      # first table column contains the song title (f[0])
      htmlOutput.write(f"  <td>{f[0]}</td>\n<td>")
      # the remainder of f's elements are files that match the title in f[0]
      for i in f[1:]:
        if ext(i) == ".urltxt":
          with open(i, "r") as urlFile:
            label = urlFile.readline().strip()
            address = urlFile.readline().strip()
          htmlOutput.write(f"<a href=\"{address}\">{label}</a><br>\n")
        elif ext(i) in downloadExtensions:
          htmlOutput.write(f" <a href=\"{str(i).replace(' ','%20')}?v={now}\" download=\"{l(i)}{ext(i)}\">{ext(i)}</a><br>\n")
        else:
          htmlOutput.write(f"  <a href=\"{str(i).replace(' ','%20')}?v={now}\">{ext(i)}</a><br>\n")

      # close each table row (and the table data containing file links)
      htmlOutput.write("</td></tr>\n")
    except:
      print(f"failed to write {f[1:]}")

  #close the table etc.
  htmlOutput.write("</table>")
  htmlOutput.write("</div>\n")
  htmlOutput.write("</div>\n")
  htmlOutput.write("</body>\n")

print("Done!", file=sys.stderr)
