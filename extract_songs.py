#!/usr/bin/env python3
"""
Script to extract song data from index.html tables and format it like Music Links.txt
"""

import re
from bs4 import BeautifulSoup
import urllib.parse


def _find_following_table(heading_tag):
    """Find the first <table> that follows a heading, before the next heading."""
    node = heading_tag
    while True:
        node = node.find_next_sibling()
        if node is None:
            return None
        if getattr(node, 'name', None) == 'table':
            return node
        if getattr(node, 'name', None) in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            return None

def extract_pdf_url(td_element):
    """Extract the first PDF URL from a table cell"""
    pdf_links = td_element.find_all('a', href=re.compile(r'\.pdf'))
    if pdf_links:
        href = pdf_links[0].get('href')
        # Handle relative URLs
        if href.startswith('music/'):
            return f"https://tuesdayukes.org/{href}"
        elif href.startswith('https://'):
            return href
        else:
            return f"https://tuesdayukes.org/music/{href}"
    return None

def extract_practice_songs(soup):
    """Extract songs from the practice-songs-table"""
    songs = []
    practice_table = soup.find('table', id='practice-songs-table')

    if practice_table:
        rows = practice_table.find_all('tr')[1:]  # Skip header row
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 2:
                title = cells[0].get_text(strip=True)
                pdf_url = extract_pdf_url(cells[1])
                if title and pdf_url:
                    songs.append({
                        'submitter': 'group',
                        'title': title,
                        'url': pdf_url
                    })

    return songs

def extract_submitted_songs(soup):
    """Extract songs from the submitted-songs-table"""
    songs = []
    submitted_table = soup.find('table', id='submitted-songs-table')

    if submitted_table:
        rows = submitted_table.find_all('tr')[1:]  # Skip header row
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 3:
                submitter = cells[0].get_text(strip=True)
                title = cells[1].get_text(strip=True)
                pdf_url = extract_pdf_url(cells[2])
                if title and pdf_url and submitter:
                    songs.append({
                        'submitter': submitter,
                        'title': title,
                        'url': pdf_url
                    })

    return songs


def extract_open_mic_practice_songs(soup):
    """Extract songs from the "Practice for ... Open Mic" table(s)."""
    songs = []

    # These tables aren't currently tagged with a stable id; locate them via the heading.
    # Example in index.html: <h2>Practice for February 21 Open Mic</h2> followed by a <table>.
    for heading in soup.find_all(['h2', 'h3']):
        heading_text = heading.get_text(strip=True)
        if not heading_text:
            continue
        if not re.search(r'^Practice\s+for\s+.*\bOpen\s+Mic\b', heading_text, flags=re.IGNORECASE):
            continue

        table = _find_following_table(heading)
        if not table:
            continue

        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) < 2:
                continue
            title = cells[0].get_text(strip=True)
            pdf_url = extract_pdf_url(cells[1])
            if title and pdf_url:
                songs.append({
                    'submitter': 'group',
                    'title': title,
                    'url': pdf_url
                })

    return songs

def format_song_entry(song, timestamp="0:00:00"):
    """Format a song entry in the Music Links.txt format"""
    return f"{timestamp} {song['submitter']} ({song['title']}) {song['url']}"

def main():
    # Read the HTML file
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print("Error: index.html not found in current directory")
        return
    except Exception as e:
        print(f"Error reading index.html: {e}")
        return

    # Parse HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract songs from both tables
    practice_songs = extract_practice_songs(soup)
    open_mic_practice_songs = extract_open_mic_practice_songs(soup)
    submitted_songs = extract_submitted_songs(soup)

    # Combine all songs
    all_songs = practice_songs + open_mic_practice_songs + submitted_songs

    if not all_songs:
        print("No songs found in the HTML tables")
        return

    # Generate output
    print("Extracted song data in Music Links.txt format:")
    print("=" * 60)

    for song in all_songs:
        print(format_song_entry(song))

    # Also save to file
    output_filename = "music/scripts/Music Links.txt"
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            for song in all_songs:
                f.write(format_song_entry(song) + '\n')
        print(f"\nOutput also saved to: {output_filename}")
    except Exception as e:
        print(f"Error saving to file: {e}")

    print(f"\nTotal songs extracted: {len(all_songs)}")
    print(f"Practice songs: {len(practice_songs)}")
    print(f"Open mic practice songs: {len(open_mic_practice_songs)}")
    print(f"Submitted songs: {len(submitted_songs)}")

if __name__ == "__main__":
    main()
