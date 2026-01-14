#!/usr/bin/env python3
"""
Filename Validation Script for Cross-Platform Compatibility

This script checks all files in the repository for characters or patterns
that could cause issues across Windows, Linux, and macOS platforms.

It flags filenames with:
- Unicode characters (especially curly quotes, em/en dashes, etc.)
- Windows reserved characters: < > : " | ? * 
- Control characters (ASCII 0-31)
- Trailing spaces or periods (problematic on Windows)
- Reserved Windows names (CON, PRN, AUX, NUL, etc.)
- Case-only differences that could cause collisions
- Path length issues (Windows has 260 character path limit)

Usage:
    python validate_filenames.py [--fix] [--path PATH]
    
Options:
    --fix           Suggest fixes for problematic filenames
    --path PATH     Specific path to check (default: entire repository)
    --extensions    Only check specific extensions (e.g., --extensions .pdf .chopro)
"""

import os
import sys
import re
import unicodedata
from pathlib import Path
from collections import defaultdict
import argparse

# Fix Windows console encoding issues
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


# Reserved Windows filenames
WINDOWS_RESERVED_NAMES = {
    'CON', 'PRN', 'AUX', 'NUL',
    'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9',
    'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'
}

# Characters that are problematic on Windows
WINDOWS_INVALID_CHARS = '<>:"|?*'

# Unicode characters that commonly cause issues
PROBLEMATIC_UNICODE = {
    '\u2018': "'",  # LEFT SINGLE QUOTATION MARK
    '\u2019': "'",  # RIGHT SINGLE QUOTATION MARK (curly apostrophe)
    '\u201C': '"',  # LEFT DOUBLE QUOTATION MARK
    '\u201D': '"',  # RIGHT DOUBLE QUOTATION MARK
    '\u2013': '-',  # EN DASH
    '\u2014': '-',  # EM DASH
    '\u2026': '...',  # HORIZONTAL ELLIPSIS
    '\u00A0': ' ',  # NO-BREAK SPACE
    '\u00AB': '"',  # LEFT-POINTING DOUBLE ANGLE QUOTATION MARK
    '\u00BB': '"',  # RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
}

# Maximum path length for Windows
WINDOWS_MAX_PATH = 260


class FilenameValidator:
    def __init__(self, root_path='.', extensions=None):
        self.root_path = Path(root_path)
        self.extensions = extensions
        self.issues = []
        self.case_map = defaultdict(list)  # Track case-insensitive duplicates
        
    def is_ascii_printable(self, char):
        """Check if character is printable ASCII"""
        return 32 <= ord(char) <= 126
    
    def has_control_chars(self, filename):
        """Check for ASCII control characters (0-31)"""
        return any(ord(c) < 32 for c in filename)
    
    def has_windows_invalid_chars(self, filename):
        """Check for Windows invalid characters"""
        return any(c in WINDOWS_INVALID_CHARS for c in filename)
    
    def has_problematic_unicode(self, filename):
        """Check for common problematic Unicode characters"""
        found = []
        for char in filename:
            if char in PROBLEMATIC_UNICODE:
                found.append((char, PROBLEMATIC_UNICODE[char], 
                            f"U+{ord(char):04X}", 
                            unicodedata.name(char, "UNKNOWN")))
        return found
    
    def has_non_ascii(self, filename):
        """Check for any non-ASCII characters"""
        return [char for char in filename if not self.is_ascii_printable(char)]
    
    def has_trailing_space_or_period(self, filename):
        """Check for trailing spaces or periods (problematic on Windows)"""
        name_without_ext = os.path.splitext(filename)[0]
        return name_without_ext.endswith((' ', '.'))
    
    def is_reserved_name(self, filename):
        """Check if filename is a Windows reserved name"""
        name_without_ext = os.path.splitext(filename)[0].upper()
        return name_without_ext in WINDOWS_RESERVED_NAMES
    
    def exceeds_path_length(self, filepath):
        """Check if full path exceeds Windows path length limit"""
        return len(str(filepath.absolute())) > WINDOWS_MAX_PATH
    
    def suggest_fix(self, filename):
        """Suggest a fixed version of the filename"""
        fixed = filename
        
        # Replace problematic Unicode characters
        for bad_char, good_char in PROBLEMATIC_UNICODE.items():
            fixed = fixed.replace(bad_char, good_char)
        
        # Replace Windows invalid characters with underscores
        for char in WINDOWS_INVALID_CHARS:
            fixed = fixed.replace(char, '_')
        
        # Remove control characters
        fixed = ''.join(c for c in fixed if ord(c) >= 32)
        
        # Remove trailing spaces and periods from name (but keep extension)
        name, ext = os.path.splitext(fixed)
        name = name.rstrip(' .')
        fixed = name + ext
        
        return fixed if fixed != filename else None
    
    def validate_file(self, filepath):
        """Validate a single file and record any issues"""
        filename = filepath.name
        issues_found = []
        
        # Check for control characters
        if self.has_control_chars(filename):
            issues_found.append("Contains control characters")
        
        # Check for Windows invalid characters
        if self.has_windows_invalid_chars(filename):
            invalid = [c for c in filename if c in WINDOWS_INVALID_CHARS]
            issues_found.append(f"Contains Windows invalid characters: {', '.join(repr(c) for c in invalid)}")
        
        # Check for problematic Unicode
        unicode_issues = self.has_problematic_unicode(filename)
        if unicode_issues:
            for char, replacement, code, name in unicode_issues:
                issues_found.append(
                    f"Contains problematic Unicode: {repr(char)} ({code} {name}) -> suggest: {repr(replacement)}"
                )
        
        # Check for non-ASCII characters
        non_ascii = self.has_non_ascii(filename)
        if non_ascii and not unicode_issues:  # Don't duplicate if already caught above
            chars_detail = ', '.join(f"{repr(c)} (U+{ord(c):04X})" for c in non_ascii[:5])
            if len(non_ascii) > 5:
                chars_detail += f" ... and {len(non_ascii) - 5} more"
            issues_found.append(f"Contains non-ASCII characters: {chars_detail}")
        
        # Check for trailing spaces or periods
        if self.has_trailing_space_or_period(filename):
            issues_found.append("Filename (without extension) ends with space or period (problematic on Windows)")
        
        # Check for reserved names
        if self.is_reserved_name(filename):
            issues_found.append(f"Reserved Windows filename")
        
        # Check path length
        if self.exceeds_path_length(filepath):
            issues_found.append(f"Path length ({len(str(filepath.absolute()))}) exceeds Windows limit ({WINDOWS_MAX_PATH})")
        
        # Track for case-insensitive duplicates
        self.case_map[str(filepath.parent / filename.lower())].append(str(filepath))
        
        if issues_found:
            self.issues.append({
                'path': filepath,
                'filename': filename,
                'issues': issues_found,
                'suggested_fix': self.suggest_fix(filename)
            })
    
    def check_case_duplicates(self):
        """Check for filenames that differ only in case"""
        duplicates = {k: v for k, v in self.case_map.items() if len(v) > 1}
        if duplicates:
            for paths in duplicates.values():
                for path in paths:
                    self.issues.append({
                        'path': Path(path),
                        'filename': Path(path).name,
                        'issues': [f"Case-insensitive duplicate with: {', '.join(str(Path(p).name) for p in paths if p != path)}"],
                        'suggested_fix': None
                    })
    
    def scan(self):
        """Scan all files in the repository"""
        print(f"Scanning files in: {self.root_path}")
        
        # Find all files
        if self.extensions:
            files = []
            for ext in self.extensions:
                files.extend(self.root_path.rglob(f'*{ext}'))
        else:
            files = [f for f in self.root_path.rglob('*') if f.is_file()]
        
        # Skip hidden files and directories
        files = [f for f in files if not any(part.startswith('.') for part in f.parts)]
        
        print(f"Found {len(files)} files to validate")
        
        for filepath in files:
            self.validate_file(filepath)
        
        # Check for case duplicates
        self.check_case_duplicates()
        
        return self.issues
    
    def report(self, show_fixes=False):
        """Print a report of all issues found"""
        if not self.issues:
            print("\n✅ No filename compatibility issues found!")
            return True
        
        print(f"\n❌ Found {len(self.issues)} file(s) with compatibility issues:\n")
        
        # Group by issue type for better readability
        by_path = defaultdict(list)
        for issue in self.issues:
            by_path[str(issue['path'])].append(issue)
        
        for path in sorted(by_path.keys()):
            issue_data = by_path[path][0]  # Get first (should only be one per path)
            print(f"📁 {path}")
            for issue_text in issue_data['issues']:
                print(f"   ⚠️  {issue_text}")
            
            if show_fixes and issue_data['suggested_fix']:
                print(f"   💡 Suggested fix: {issue_data['suggested_fix']}")
            print()
        
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Validate filenames for cross-platform compatibility',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument('--fix', action='store_true',
                       help='Show suggested fixes for problematic filenames')
    parser.add_argument('--path', default='.',
                       help='Path to scan (default: current directory)')
    parser.add_argument('--extensions', nargs='*',
                       help='Only check files with these extensions (e.g., .pdf .chopro)')
    
    args = parser.parse_args()
    
    # Convert to Path and validate
    scan_path = Path(args.path)
    if not scan_path.exists():
        print(f"Error: Path does not exist: {scan_path}")
        return 1
    
    # Run validation
    validator = FilenameValidator(scan_path, args.extensions)
    validator.scan()
    success = validator.report(show_fixes=args.fix)
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
