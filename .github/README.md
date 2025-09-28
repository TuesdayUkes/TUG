# ChordPro PDF Generation CI/CD

This repository includes automated workflows to generate PDF files from ChordPro (.chopro and .cho) files whenever they are modified.

## How it works

### Triggers
The workflow is triggered when:
- Any `.chopro` or `.cho` file is modified
- The `music/ChordPro/myconfig.json` configuration file is changed
- Changes are pushed to main/master branch or in pull requests

### Configuration
The PDF generation uses the same settings as `GenList.py`:
- Config file: `music/ChordPro/myconfig.json`
- Diagram placement: top
- Inline chords: enabled
- Margins: top=70, bottom=0, left=20, right=20
- Fonts: Helvetica for both text and chords
- Chord color: red

### Behavior

#### For All Events (Push and Pull Requests)
- Generates PDFs for changed ChordPro files
- If `myconfig.json` changes, regenerates ALL PDFs
- Uploads generated PDFs as downloadable artifacts
- Does NOT commit PDFs to the repository (artifacts only)

#### For Pull Requests
- Comments on the PR with list of generated PDFs
- Provides direct links to download artifacts

## Files

### Workflows
- `.github/workflows/generate-pdfs.yml` - Full-featured workflow with detailed logging
- `.github/workflows/generate-pdfs-optimized.yml` - Streamlined workflow (recommended)

### Scripts
- `.github/scripts/generate-pdfs.sh` - Bash script that replicates GenList.py PDF generation logic

## Setup

1. The workflows are automatically active once these files are in the repository
2. ChordPro will be installed automatically in the GitHub runner
3. Generated PDFs will appear in the same directory as their source .chopro files

## Monitoring

Check the "Actions" tab in GitHub to monitor workflow runs. Each run provides:
- Summary of files processed
- List of generated PDFs
- Any errors encountered

## Troubleshooting

If PDF generation fails:
1. Check the workflow logs in GitHub Actions
2. Verify your ChordPro files are valid
3. Ensure `music/ChordPro/myconfig.json` is valid JSON
4. Check that file paths don't contain unsupported characters
