#!/bin/bash
# Helper script for generating ChordPro PDFs
# This script replicates the logic from GenList.py's createPDFs() function

# Note: Removed 'set -e' to allow graceful error handling

MUSIC_FOLDER="${1:-music}"
FORCE_REGENERATE="${2:-false}"

echo "🎵 ChordPro PDF Generator"
echo "========================"
echo "Music folder: $MUSIC_FOLDER"
echo "Force regenerate: $FORCE_REGENERATE"
echo ""

# ChordPro command arguments (matching GenList.py settings)
CHORDPRO_ARGS=(
    "--config=ukulele"
    "--config=ukulele-ly"
    "--define=pdf:diagrams:show=top"
    "--define=settings:inline-chords=true"
    "--define=pdf:margintop=70"
    "--define=pdf:marginbottom=0"
    "--define=pdf:marginleft=10"
    "--define=pdf:marginright=20"
    "--define=pdf:headspace=50"
    "--define=pdf:footspace=10"
    "--define=pdf:head-first-only=true"
    "--define=pdf:fonts:chord:color=red"
    "--define=pdf:papersize=a5"
    "--text-font=helvetica"
    "--chord-font=helvetica"
)

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

        # Generate PDF (ignore exit codes)
        chordpro "${CHORDPRO_ARGS[@]}" --output="$pdf_file" "$chopro_file" 2>/dev/null || true

        # Check if PDF was actually created
        if [ -f "$pdf_file" ]; then
            echo "  ✓ Generated: $(basename "$pdf_file")"
            GENERATED=$((GENERATED + 1))
        else
            echo "  ⚠ Failed: $(basename "$pdf_file") (no output file)"
            ERRORS=$((ERRORS + 1))
        fi
    else
        echo "⏩ Skipping: $(basename "$chopro_file") (PDF up to date)"
        SKIPPED=$((SKIPPED + 1))
    fi

    PROCESSED=$((PROCESSED + 1))
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
    echo "⚠ $ERRORS files failed to process (but continuing)"
fi

echo ""
echo "🎉 Done!"
