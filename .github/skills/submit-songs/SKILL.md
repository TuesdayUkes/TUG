---
name: submit-songs
description: "Use when asked to submit songs or add a song submission (e.g., 'submit [song] for [person]') to the Tuesday Ukes submitted songs table in index.html."
---

# Submit Songs Skill

## Goal
Add song submissions to the submitted songs table in index.html using the authoritative links from ukulele-song-archive.html.

## Inputs
- Song title(s)
- Submitter name(s)

## Workflow
1. Run this command in the terminal to refresh the archive: `genlist music ukulele-song-archive.html`
2. Open index.html and locate the table with id submitted-songs-table.
3. Open ukulele-song-archive.html and find the exact song entry.
4. Capture the PDF link and the most recent recording link.
5. Insert a new table row for each submission.

## Row Format
Use this structure:

<tr>  <td>Submitter</td>  <td>Title</td>
<td>
<a href="PDF_LINK" target="_blank">.pdf</a><br>
<a href="RECORDING_LINK" target="_blank"># Most recent recording: DATE</a><br>
</td></tr>

If no recording link exists, omit that line.

## Ordering Rule
The table is ordered in rounds: no submitter gets a second song until every submitter has had one, no submitter gets a third song until every submitter has had two, and so on. Within each round, never place two consecutive rows from the same person. When inserting new songs, treat the existing rows as already-placed rounds and slot each new song into the correct round position.

Example: if the table already has Tom, Todd, Roy, Mary Jane then Walter and Mary Jane are each submitting one more song, the result is: Tom, Todd, Roy, Mary Jane, Walter, Mary Jane (not Tom, Todd, Roy, Mary Jane, Walter, Walter, Mary Jane).

## Disambiguation
- If multiple versions exist, prefer the most recently committed PDF unless the user specifies a version. Uncommitted or untracked files (i.e. files that appear in `git status` as new or modified) are always treated as newer than any committed file. To determine which PDF is most recent: first run `git status --short -- "music/**/*.pdf" "music/**/*.urltxt"` and treat any file listed there as the newest; if no relevant files are uncommitted, run `git log --diff-filter=AM --name-only --pretty=format: -- "music/**/*.pdf"` and pick the PDF for this song that appears in the most recent commit. For PDF links that point to an external website (e.g. Doctor Uke), use the commit date of the corresponding `.urltxt` file instead: run `git log --diff-filter=AM --name-only --pretty=format: -- "music/**/*.urltxt"` and find the `.urltxt` file whose name matches the song, then compare its commit date against the local PDF commit dates to determine which is newer; an uncommitted `.urltxt` file is treated as newer than any committed file.
- Always prefer PDF links over .chopro when both are available.
- If the title in the archive differs, use the archive title verbatim.

## Quality Checks
- Verify links are copied exactly (including query strings and timestamps).
- Keep HTML formatting consistent with existing rows.
