submit_songs.py
=================

Overview
--------
Automates adding song submissions to the submitted-songs table in `index.html` following the Tuesday Ukes submission rules.

Requirements
------------
- Python 3.8+ (or any recent 3.x)
- Install runtime deps:

```bash
pip install -r requirements.txt
```

Usage
-----
Make a quick backup before running:

```bash
cp index.html index.html.bak
```

Add one or more submissions:

```bash
python submit_songs.py --submitter Roy "Casey Jones - Grateful Dead" "Same Thing Happened to Me"
```

Options
-------
- `--index path/to/index.html` — use an alternate index file (default: `index.html`).

Behavior / Key points
---------------------
- Searches `music/` recursively for matching PDF files (preferred) or `.chopro` files; matching is fuzzy (title words must appear in the filename).
- Preserves existing metadata in the table: any PDF hrefs and YouTube "Most recent recording" anchors found in the table are preserved.
- Only YouTube links (anchors containing `youtu`/`youtube.com`) are considered valid recordings.
- A `<br>` is inserted before any recording link so the recording appears on its own line in the same cell as the PDF.
- Idempotent and safe: the script avoids creating duplicate submitter+title rows. If the same submitter+title already exists the script will promote that row into the earliest valid round and update any missing metadata (pdf/recording) instead of inserting a duplicate.
- Ordering: partitions the table into rounds so every active submitter appears once before any second-round repeats; new submissions are inserted into the first round where the submitter is missing, otherwise appended.
- Only the `submitted-songs-table` region of `index.html` is replaced to minimize unrelated formatting changes.
- The output table is pretty-printed: each `<tr>` is a block and each `<td>`/`<th>` is written on its own line for readability.

Safety & workflow
-----------------
- Always back up `index.html` (or commit) before running.
- The script writes the updated table back into the specified index file; it is safe to run repeatedly (idempotent), but test on a copy if you're unsure.
- A `--dry-run` flag is not implemented yet (planned).

Developer notes
---------------
- Main entry: `submit_songs.py`
- Helpful functions:
	- `parse_submitted_rows(table_tag)` — parse rows and preserve `pdf`/`recording` metadata
	- `find_best_file(title)` — search `music/` for matching PDF/.chopro
	- `find_most_recent_recording(title)` — scan the ukulele song archive for YouTube recordings
	- `insert_submission(rows, submitter, title, pdf)` — round-aware insertion logic
	- `row_to_tag(soup, row)` — build the `<tr>` element for a row
	- `format_table_html(table_tag)` — pretty-print the table before writing

Changelog
---------
- 2026-09-05: Preserve existing PDFs and YouTube recording links; dedupe and promote existing rows rather than duplicating; replace only the table region; pretty-print table; insert `<br>` before recordings.
