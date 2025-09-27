#!/usr/bin/env python3
"""
Script to extract song data from index.html tables and format it like Music Links.txt
"""

import re
from bs4 import BeautifulSoup
import urllib.parse

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

def format_song_entry(song, timestamp="0:00"):
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
    submitted_songs = extract_submitted_songs(soup)
    
    # Combine all songs
    all_songs = practice_songs + submitted_songs
    
    if not all_songs:
        print("No songs found in the HTML tables")
        return
    
    # Generate output
    print("Extracted song data in Music Links.txt format:")
    print("=" * 60)
    
    for song in all_songs:
        print(format_song_entry(song))
    
    # Also save to file
    output_filename = "extracted_music_links.txt"
    try:
        with open(output_filename, 'w', encoding='utf-8') as f:
            for song in all_songs:
                f.write(format_song_entry(song) + '\n')
        print(f"\nOutput also saved to: {output_filename}")
    except Exception as e:
        print(f"Error saving to file: {e}")
    
    print(f"\nTotal songs extracted: {len(all_songs)}")
    print(f"Practice songs: {len(practice_songs)}")
    print(f"Submitted songs: {len(submitted_songs)}")

if __name__ == "__main__":
    main()