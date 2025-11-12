# ChordPro PDF Generation CI/CD

This repository includes automated workflows to generate PDF files from ChordPro (.chopro and .cho) files whenever they are modified.

## How it works

### Triggers
The PDF generation workflow is triggered when:
- Any `.chopro` or `.cho` file is modified
- Changes are pushed to the main/master branch (not on pull requests)

### Configuration
The PDF generation uses genpdf-butler with the following settings:
- Page size: A5
- Chord placement: top
- No custom config file dependencies (uses genpdf-butler defaults)

### Behavior

#### For Push Events to Main Branch
- Generates PDFs for changed ChordPro files that don't have current PDFs
- Uses intelligent detection to avoid regenerating PDFs that are already up-to-date
- **Commits generated PDFs directly to the repository**
- Automatically triggers GitHub Pages deployment after PDF generation
- Uses genpdf-butler with A5 page size and chords displayed on top

#### Smart PDF Generation Logic
- Only regenerates PDFs when the ChordPro file is newer than the existing PDF
- Compares commit timestamps to determine if regeneration is needed
- Skips generation if PDF was updated in the same push as the ChordPro file

## Files

### Workflows
- `.github/workflows/auto-generate-pdfs.yml` - Main PDF generation workflow
- `.github/workflows/deploy-pages-action.yml` - GitHub Pages deployment workflow

## Setup

1. The workflows are automatically active once these files are in the repository
2. genpdf-butler and ChordPro will be installed automatically in the GitHub runner
3. Generated PDFs will appear in the same directory as their source .chopro files
4. PDFs are automatically committed to the repository and deployed to GitHub Pages

## Monitoring

Check the "Actions" tab in GitHub to monitor workflow runs. Each run provides:
- Summary of files processed
- Smart detection of which PDFs actually need regeneration
- Automatic commit of generated PDFs
- Triggered GitHub Pages deployment
- Any errors encountered

## Troubleshooting

If PDF generation fails:
1. Check the workflow logs in GitHub Actions
2. Verify your ChordPro files are valid syntax
3. Check that file paths don't contain unsupported characters
4. Ensure the repository has write permissions for the GitHub Actions workflow
