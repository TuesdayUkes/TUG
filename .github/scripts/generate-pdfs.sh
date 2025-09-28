#!/bin/bash
# Helper script for generating ChordPro PDFs
# This script replicates the logic from GenList.py's createPDFs() function

set -e  # Exit on error

MUSIC_FOLDER="${1:-music}"
FORCE_REGENERATE="${2:-false}"
CONFIG_FILE="music/ChordPro/myconfig.json"

echo "🎵 ChordPro PDF Generator"
echo "========================"
echo "Music folder: $MUSIC_FOLDER"
echo "Force regenerate: $FORCE_REGENERATE"
echo "Config file: $CONFIG_FILE"
echo ""

# ChordPro command arguments (matching GenList.py settings)
CHORDPRO_ARGS=(
    "--define=pdf:diagrams:show=top"
    "--define=settings:inline-chords=true"
    "--define=pdf:margintop=70"
    "--define=pdf:marginbottom=0"
    "--define=pdf:marginleft=20"
    "--define=pdf:marginright=20"
    "--define=pdf:headspace=50"
    "--define=pdf:footspace=10"
    "--define=pdf:head-first-only=true"
    "--define=pdf:fonts:chord:color=red"
    "--text-font=helvetica"
    "--chord-font=helvetica"
)

# Add config file if it exists
if [ -f "$CONFIG_FILE" ]; then
    CHORDPRO_ARGS+=("--config=$CONFIG_FILE")
    echo "✓ Using config file: $CONFIG_FILE"
else
    echo "⚠ Config file not found: $CONFIG_FILE"
fi

# Find all ChordPro files
echo "🔍 Finding ChordPro files..."
CHOPRO_FILES=$(find "$MUSIC_FOLDER" -type f \( -name "*.chopro" -o -name "*.cho" \) 2>/dev/null || true)

if [ -z "$CHOPRO_FILES" ]; then
    echo "ℹ No ChordPro files found in $MUSIC_FOLDER"
    exit 0
fi

TOTAL_FILES=$(echo "$CHOPRO_FILES" | wc -l)
PROCESSED=0
GENERATED=0
SKIPPED=0
ERRORS=0

echo "📁 Found $TOTAL_FILES ChordPro files"
echo ""

# Process each file
while IFS= read -r chopro_file; do
    if [ -z "$chopro_file" ]; then
        continue
    fi
    
    # Generate PDF path
    pdf_file="${chopro_file%.*}.pdf"
    
    # Check if PDF needs to be generated
    if [ "$FORCE_REGENERATE" = "true" ] || [ ! -f "$pdf_file" ] || [ "$chopro_file" -nt "$pdf_file" ]; then
        echo "📄 Processing: $(basename "$chopro_file")"
        
        # Create output directory if needed
        mkdir -p "$(dirname "$pdf_file")"
        
        # Generate PDF
        if chordpro "${CHORDPRO_ARGS[@]}" --output="$pdf_file" "$chopro_file" 2>/dev/null; then
            echo "  ✓ Generated: $(basename "$pdf_file")"
            ((GENERATED++))
        else
            echo "  ✗ Failed: $(basename "$pdf_file")"
            ((ERRORS++))
        fi
    else
        echo "⏩ Skipping: $(basename "$chopro_file") (PDF up to date)"
        ((SKIPPED++))
    fi
    
    ((PROCESSED++))
done <<< "$CHOPRO_FILES"

echo ""
echo "📊 Summary:"
echo "  Total files: $TOTAL_FILES"
echo "  Processed: $PROCESSED"
echo "  Generated: $GENERATED"
echo "  Skipped: $SKIPPED"
echo "  Errors: $ERRORS"

if [ $ERRORS -gt 0 ]; then
    echo ""
    echo "⚠ $ERRORS files failed to process"
    exit 1
fi

echo ""
echo "🎉 Done!"
