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
Ensure that each submitter appears once in the list before any submitter appears a second time. If a submitter already exists in the table, place their additional songs after all submitters who appear only once.

## Disambiguation
- If multiple versions exist, prefer the most recent PDF unless the user specifies a version.
- Always prefer PDF links over .chopro when both are available.
- If the title in the archive differs, use the archive title verbatim.

## Quality Checks
- Verify links are copied exactly (including query strings and timestamps).
- Keep HTML formatting consistent with existing rows.
