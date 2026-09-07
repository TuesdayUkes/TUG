#!/usr/bin/env python3
"""
submit_songs.py

Add one or more song submissions to the submitted-songs table in index.html.

Usage:
  python submit_songs.py --submitter Roy "Casey Jones - Grateful Dead" "Same Thing Happened to Me"

Behavior (implements the skill rules):
- Finds the canonical PDF for the song under `music/` (prefers PDF over .chopro)
- Inserts a new table row for each submission into the `submitted-songs-table` in `index.html`
- Respects the round-order rule: every active submitter appears once before any second-round repeats
- Avoids placing two consecutive rows from the same submitter
"""
import argparse
from bs4 import BeautifulSoup
from pathlib import Path
import re
import sys
from typing import Optional, Dict
from urllib.parse import urlparse, unquote


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9 ]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def find_best_file(song_title: str) -> str | None:
    """Search the music tree for a PDF (preferred) or .chopro matching the song title.

    Chooses the best candidate by scoring filename closeness (exact match, substring,
    word overlap and sequence similarity). Prefers PDFs when scores tie.
    """
    base = Path('music')
    if not base.exists():
        return None

    want = normalize(song_title)
    want_words = want.split()

    # collect all candidate files
    candidates = [p for p in base.rglob('*') if p.is_file() and p.suffix.lower() in ('.pdf', '.chopro')]
    if not candidates:
        return None

    # score candidates
    from difflib import SequenceMatcher

    best = None
    best_score = -10**9
    for p in candidates:
        name = normalize(p.stem)
        name_words = name.split()
        # exact match
        score = 0
        if name == want:
            score += 2000
        # substring match (words in order)
        if want in name:
            score += 800
        # word overlap
        common = sum(1 for w in want_words if w in name_words)
        score += common * 150
        # similarity ratio for fuzzy matching
        ratio = SequenceMatcher(None, name, want).ratio()
        score += int(ratio * 200)
        # prefer PDFs slightly
        if p.suffix.lower() == '.pdf':
            score += 50

        if score > best_score:
            best_score = score
            best = p

    return str(best).replace('\\', '/') if best else None


def find_most_recent_recording(song_title: str) -> Optional[Dict[str, str]]:
    """Search the ukulele-song-archive for a recording link related to the song.

    Returns a dict {'href': href, 'date': date_str} or None.
    """
    candidates = [Path('ukulele-song-archive.html'), Path('_site/ukulele-song-archive.html')]
    for p in candidates:
        if not p.exists():
            continue
        soup = BeautifulSoup(p.read_text(encoding='utf-8'), 'html.parser')
        want = normalize(song_title)
        for tr in soup.find_all('tr'):
            txt = normalize(tr.get_text())
            want_words = want.split()
            if all(w in txt for w in want_words):
                # prefer youtube links
                anchors = [a for a in tr.find_all('a', href=True)]
                # only consider youtube links as valid recordings
                youtube = [a for a in anchors if 'youtu' in a['href'] or 'youtube.com' in a['href']]
                pick = youtube[0] if youtube else None
                if pick:
                    # try to extract a date like 'July 8, 2025' from the row text
                    full_text = tr.get_text()
                    m = re.search(r'([A-Z][a-z]+\s\d{1,2},\s\d{4})', full_text)
                    date = m.group(1) if m else ''
                    return {'href': pick['href'], 'date': date}
    return None


def parse_submitted_rows(table_tag):
    rows = []
    for tr in table_tag.find_all('tr'):
        tds = tr.find_all('td')
        if not tds or len(tds) < 2:
            continue
        submitter = tds[0].get_text(strip=True)
        title = tds[1].get_text(strip=True)
        # try to preserve any existing PDF link and a YouTube recording in the third column
        pdf = ''
        recording = None
        if len(tds) >= 3:
            anchors = [a for a in tds[2].find_all('a', href=True)]
            for a in anchors:
                href = a['href']
                href_l = href.lower()
                # prefer explicit PDF links -- accept query strings or fragments after .pdf
                if not pdf:
                    if re.search(r'\.pdf($|\?|#)', href_l) or a.get_text(strip=True).lower().startswith('.pdf'):
                        pdf = href
                # record YouTube-style recording links
                if 'youtu' in href_l or 'youtube.com' in href_l:
                    # try to extract a readable date from the anchor text
                    label = a.get_text(strip=True)
                    m = re.search(r'([A-Z][a-z]+\s\d{1,2},\s\d{4})', label)
                    date = m.group(1) if m else ''
                    recording = {'href': href, 'date': date}
        rows.append({'submitter': submitter, 'title': title, 'pdf': pdf, 'recording': recording})
    return rows


def partition_rounds(rows):
    rounds = []
    current = []
    seen = set()
    for r in rows:
        s = r['submitter']
        if s in seen:
            rounds.append(current)
            current = [r]
            seen = {s}
        else:
            current.append(r)
            seen.add(s)
    if current:
        rounds.append(current)
    return rounds


def insert_submission(rows, submitter, title, pdf_link):
    rounds = partition_rounds(rows)
    for i, rnd in enumerate(rounds):
        members = {r['submitter'] for r in rnd}
        if submitter not in members:
            insert_index = sum(len(r) for r in rounds[:i+1])
            if insert_index > 0 and rows[insert_index-1]['submitter'] == submitter:
                insert_index += 1
            rows.insert(insert_index, {'submitter': submitter, 'title': title, 'pdf': pdf_link})
            return rows

    rows.append({'submitter': submitter, 'title': title, 'pdf': pdf_link})
    return rows


def row_to_tag(soup, row):
    tr = soup.new_tag('tr')
    td1 = soup.new_tag('td')
    td1.string = row['submitter']
    td2 = soup.new_tag('td')
    td2.string = row['title']
    td3 = soup.new_tag('td')
    if row.get('pdf'):
        a = soup.new_tag('a', href=row['pdf'], target='_blank')
        a.string = '.pdf'
        td3.append(a)
    # optionally append recording link on its own line in the same cell
    if row.get('recording'):
        rec = row['recording']
        # insert a break before the recording link
        br = soup.new_tag('br')
        td3.append(br)
        ra = soup.new_tag('a', href=rec.get('href', '#'), target='_blank')
        label = '# Most recent recording'
        if rec.get('date'):
            label = f"# Most recent recording: {rec['date']}"
        ra.string = label
        td3.append(ra)
    tr.append(td1)
    tr.append(td2)
    tr.append(td3)
    return tr


def format_table_html(table_tag, indent='    '):
    """Return a human-friendly HTML string for the table where each <tr> is on its own
    block and each <td>/<th> appears on its own line.
    """
    def attrs_str(tag):
        parts = []
        for k, v in tag.attrs.items():
            if v is True:
                parts.append(k)
            elif isinstance(v, list):
                parts.append(f'{k}="{" ".join(v)}"')
            else:
                parts.append(f'{k}="{v}"')
        return (' ' + ' '.join(parts)) if parts else ''

    rows = table_tag.find_all('tr')
    lines = []
    lines.append(f"<table{attrs_str(table_tag)}>")
    for tr in rows:
        lines.append(indent + '<tr>')
        # use direct child cells in order
        for cell in tr.find_all(['th', 'td'], recursive=False):
            tagname = cell.name
            inner = ''.join(str(c) for c in cell.contents).strip()
            lines.append(indent * 2 + f"<{tagname}>{inner}</{tagname}>")
        lines.append(indent + '</tr>')
        lines.append('')
    lines.append('</table>')
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--submitter', required=True, help='Submitter name')
    parser.add_argument('titles', nargs='+', help='Song title(s) to submit')
    parser.add_argument('--index', default='index.html', help='Path to index.html')
    args = parser.parse_args()

    index_path = Path(args.index)
    if not index_path.exists():
        print('index.html not found at', index_path)
        sys.exit(1)

    html = index_path.read_text(encoding='utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', id='submitted-songs-table')
    if table is None:
        print('submitted-songs-table not found in', index_path)
        sys.exit(1)

    existing_rows = parse_submitted_rows(table)

    def file_title_from_href(href: str) -> str:
        if not href:
            return ''
        parsed = urlparse(href)
        # prefer the parsed path (works for URLs and relative hrefs with query strings)
        path = parsed.path if parsed.path else href
        try:
            return Path(unquote(path)).stem
        except Exception:
            return Path(path).stem

    # preserve existing pdf and recording fields when rebuilding; if a pdf href exists
    # use the file stem as the displayed title
    rows = []
    for r in existing_rows:
        pdf = r.get('pdf', '')
        title = r['title']
        if pdf:
            ft = file_title_from_href(pdf)
            if ft:
                title = ft
        rows.append({'submitter': r['submitter'], 'title': title, 'pdf': pdf, 'recording': r.get('recording')})

    for title in args.titles:
        pdf = find_best_file(title) or ''
        rec = find_most_recent_recording(title)

        # find existing row index for this submitter+title
        existing_idx = None
        for i, r in enumerate(rows):
            if r['submitter'] == args.submitter and normalize(r['title']) == normalize(title):
                existing_idx = i
                break

        if existing_idx is not None:
            # remove existing row and reinsert it into the earliest valid round
            existing_row = rows.pop(existing_idx)
            # update metadata if newly discovered
            if not existing_row.get('pdf') and pdf:
                existing_row['pdf'] = pdf
            if not existing_row.get('recording') and rec:
                existing_row['recording'] = rec

            # if we now have a pdf, set the displayed title to the file stem
            if existing_row.get('pdf'):
                ft = file_title_from_href(existing_row['pdf'])
                if ft:
                    existing_row['title'] = ft

            rows = insert_submission(rows, args.submitter, existing_row['title'], existing_row.get('pdf', ''))
            # attach recording to the reinserted row
            for r in rows:
                if r['submitter'] == args.submitter and normalize(r['title']) == normalize(existing_row['title']):
                    r['recording'] = existing_row.get('recording')
                    break
        else:
            # insert new row following round-order rules
            rows = insert_submission(rows, args.submitter, title, pdf)
            # if pdf was found, replace the displayed title with the file stem
            if pdf:
                ft = file_title_from_href(pdf)
                if ft:
                    for r in rows:
                        if r['submitter'] == args.submitter and normalize(r['title']) == normalize(title):
                            r['title'] = ft
                            break
            # attach recording info to the inserted row (find by title and submitter)
            for r in rows:
                if r['submitter'] == args.submitter and normalize(r['title']) == normalize(title) and not r.get('recording'):
                    if rec:
                        r['recording'] = rec
                    break

    # deduplicate by (submitter,title) keeping first occurrence, then write
    final_rows = []
    seen = set()
    for r in rows:
        key = (normalize(r['submitter']), normalize(r['title']))
        if key in seen:
            continue
        seen.add(key)
        final_rows.append(r)

    # Ensure missing PDFs are filled from the music tree when possible
    for r in final_rows:
        if not r.get('pdf'):
            pdf_candidate = find_best_file(r['title'])
            if pdf_candidate:
                r['pdf'] = pdf_candidate
                # update displayed title to file stem
                ft = file_title_from_href(pdf_candidate)
                if ft:
                    r['title'] = ft

    # remove existing data rows
    for tr in table.find_all('tr'):
        if tr.find('th'):
            continue
        tr.decompose()

    # append final rows
    for r in final_rows:
        tr = row_to_tag(soup, r)
        table.append(tr)

    # Replace only the submitted-songs table in the original HTML to avoid unrelated formatting changes
    orig_html = html
    new_table_html = format_table_html(table)
    pattern = re.compile(r'(<table\b[^>]*\bid=["\']submitted-songs-table["\'][^>]*>).*?(</table>)', re.DOTALL)
    new_html, n = pattern.subn(new_table_html, orig_html, count=1)
    if n:
        index_path.write_text(new_html, encoding='utf-8')
    else:
        # fallback to full write if pattern match failed
        index_path.write_text(str(soup), encoding='utf-8')
    print('Updated', index_path)


if __name__ == '__main__':
    main()
