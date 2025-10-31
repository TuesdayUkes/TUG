#!/usr/bin/env python3
"""
Enhanced script to update v= timestamps in URLs within HTML files.
This script can update timestamps in specific tables or throughout the entire file.
"""

import re
import os
import argparse
from datetime import datetime
from pathlib import Path

def generate_timestamp():
    """Generate a timestamp in the format YYYY.MM.DD.HH.MM.SS"""
    return datetime.now().strftime("%Y.%m.%d.%H.%M.%S")

def update_v_timestamps_in_content(content):
    """
    Update v= timestamps in URLs within content.
    Only updates URLs that contain .pdf and have v= parameters.
    """
    # Pattern to match URLs with v= parameters (focusing on PDF links)
    pattern = r'(href="[^"]*\.pdf\?v=)([^"]*)"'
    
    new_timestamp = generate_timestamp()
    updated_count = 0
    
    def replace_timestamp(match):
        nonlocal updated_count
        url_start = match.group(1)  # Everything up to and including "v="
        old_timestamp = match.group(2)  # The old timestamp
        
        print(f"  Updating: {old_timestamp} -> {new_timestamp}")
        updated_count += 1
        return f'{url_start}{new_timestamp}"'
    
    # Replace all v= timestamps in PDF URLs
    updated_content = re.sub(pattern, replace_timestamp, content)
    
    return updated_content, updated_count

def update_timestamps_in_tables(html_content, table_ids):
    """
    Update v= timestamps only within specific HTML tables.
    
    Args:
        html_content (str): The HTML content
        table_ids (list): List of table IDs to update
    
    Returns:
        tuple: (updated_content, total_updates)
    """
    updated_content = html_content
    total_updates = 0
    
    for table_id in table_ids:
        # Find the table with the specified ID
        table_pattern = rf'(<table[^>]*id="{table_id}"[^>]*>.*?</table>)'
        table_match = re.search(table_pattern, updated_content, re.DOTALL | re.IGNORECASE)
        
        if table_match:
            table_content = table_match.group(1)
            print(f"\nProcessing table: {table_id}")
            
            # Update timestamps within this table
            updated_table, count = update_v_timestamps_in_content(table_content)
            total_updates += count
            
            # Replace the table in the full content
            updated_content = updated_content.replace(table_content, updated_table)
            
            if count == 0:
                print(f"  No v= timestamps found in table '{table_id}'")
            else:
                print(f"  Updated {count} timestamp(s) in table '{table_id}'")
        else:
            print(f"Warning: Table with ID '{table_id}' not found")
    
    return updated_content, total_updates

def update_all_timestamps(html_content):
    """
    Update all v= timestamps in the entire HTML content.
    
    Args:
        html_content (str): The HTML content
    
    Returns:
        tuple: (updated_content, total_updates)
    """
    print("\nProcessing entire file...")
    return update_v_timestamps_in_content(html_content)

def main():
    """Main function to update timestamps in HTML file"""
    parser = argparse.ArgumentParser(description='Update v= timestamps in HTML file URLs')
    parser.add_argument('--file', '-f', default='index.html', 
                       help='HTML file to process (default: index.html)')
    parser.add_argument('--all', '-a', action='store_true',
                       help='Update all v= timestamps in the entire file')
    parser.add_argument('--tables', '-t', nargs='*', 
                       default=['practice-songs-table', 'submitted-songs-table'],
                       help='Table IDs to update (default: practice-songs-table submitted-songs-table)')
    parser.add_argument('--backup', action='store_true',
                       help='Create backup file (default: no backup)')
    parser.add_argument('--dry-run', '-n', action='store_true',
                       help='Show what would be updated without making changes')
    
    args = parser.parse_args()
    
    script_dir = Path(__file__).parent
    html_file = script_dir / args.file
    
    if not html_file.exists():
        print(f"Error: {html_file} not found!")
        return 1
    
    print(f"Reading {html_file}")
    
    # Read the HTML file
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except UnicodeDecodeError:
        # Try with different encoding if UTF-8 fails
        try:
            with open(html_file, 'r', encoding='iso-8859-1') as f:
                html_content = f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return 1
    
    # Create backup only if --backup is specified
    if args.backup and not args.dry_run:
        backup_file = html_file.with_suffix(f'.html.backup.{generate_timestamp()}'[:19].replace(":", "-"))
        print(f"Creating backup: {backup_file}")
        with open(backup_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
    
    print(f"\nNew timestamp will be: {generate_timestamp()}")
    
    # Update timestamps based on mode
    if args.all:
        updated_content, total_updates = update_all_timestamps(html_content)
    else:
        updated_content, total_updates = update_timestamps_in_tables(html_content, args.tables)
    
    if total_updates == 0:
        print("\nNo v= timestamps found to update.")
        return 0
    
    print(f"\nTotal updates: {total_updates}")
    
    if args.dry_run:
        print("\nDry run mode - no changes made to file.")
        return 0
    
    # Write the updated content back to the file
    print(f"\nWriting updated content to {html_file}")
    try:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        print("Timestamp update completed successfully!")
    except Exception as e:
        print(f"Error writing file: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
