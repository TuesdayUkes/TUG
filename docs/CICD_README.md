# CI/CD & Automated Workflows

This repository includes sophisticated automated workflows that handle PDF generation and website deployment whenever changes are made.

## 🔄 How It Works

### PDF Generation Workflow
- **Trigger**: When `.chopro` or `.cho` files are modified and pushed to main branch
- **Process**: Automatically generates PDFs using genpdf-butler
- **Output**: Commits generated PDFs directly to repository
- **Intelligence**: Only regenerates PDFs when ChordPro file is newer than existing PDF

### Website Deployment Workflow  
- **Trigger**: When website files (HTML, CSS, JS, images, PDFs) are modified
- **Process**: Builds complete website with generated song archive and sitemap
- **Output**: Deploys to GitHub Pages at [tuesdayukes.org](https://tuesdayukes.org/)

## ⚙️ Configuration

### PDF Generation Settings
- **Tool**: genpdf-butler
- **Page Size**: A5
- **Chord Placement**: Top of page
- **Dependencies**: No custom config files required

### Smart Detection Logic
- Compares commit timestamps between ChordPro and PDF files
- Skips regeneration if PDF was updated after ChordPro file in same push
- Prevents unnecessary processing and commit noise

## 📁 Workflow Files

### Main Workflows
- **`.github/workflows/auto-generate-pdfs.yml`** - PDF generation workflow
- **`.github/workflows/deploy-pages-action.yml`** - GitHub Pages deployment

### Key Features
- **Parallel Processing**: Handles multiple file changes efficiently  
- **Error Handling**: Graceful failure with detailed logging
- **Automatic Deployment**: Triggers website deployment after PDF generation
- **Commit Integration**: Clean commit messages with generated file lists

## 🚀 Setup & Usage

### Automatic Operation
1. Workflows activate automatically when files are committed
2. No manual intervention required for normal operations
3. Monitor progress in GitHub Actions tab

### Manual Triggers
- Website deployment can be triggered manually via GitHub Actions
- Force deployment option available for complete rebuilds

## 📊 Monitoring

### GitHub Actions Dashboard
Check the "Actions" tab for:
- **Workflow Status**: Success/failure of each run
- **Processing Details**: Which files were processed
- **Generated Files**: List of created/updated PDFs
- **Deployment Status**: Website deployment progress
- **Error Logs**: Detailed debugging information

### Typical Workflow Sequence
1. 📝 ChordPro file committed → PDF generation triggered
2. 🎵 PDF generated and committed → Website deployment triggered  
3. 🗺️ Site artifacts regenerated, including `ukulele-song-archive.html`, `xmas-songbook.html`, and `sitemap.xml`
4. 🚀 Website deployed with updated content
5. ✅ Process complete, changes live

## 🐛 Troubleshooting

### Common Issues
1. **PDF Generation Fails**
   - Check ChordPro file syntax
   - Verify file paths don't contain special characters
   - Review workflow logs in GitHub Actions

2. **Website Deployment Fails**
   - Check HTML file validity
   - Verify image/resource links are correct
   - Review Pages deployment logs

3. **Permission Errors**
   - Ensure repository has write permissions for workflows
   - Check GitHub token permissions in Settings

### Debug Steps
1. Check workflow logs in GitHub Actions tab
2. Verify file syntax and structure
3. Test changes in smaller batches
4. Review repository permissions settings

## 🔧 Advanced Configuration

### Workflow Permissions
```yaml
permissions:
  contents: write    # Allow committing generated PDFs
  pages: write      # Allow Pages deployment
  id-token: write   # Allow OIDC token for deployment
```

### Environment Variables
- **FORCE_COLOR**: Enables colored output in workflow logs
- **GitHub Tokens**: Automatically provided by GitHub Actions

## ⏳ Upstream Tracking (Node 20 Deprecation)

GitHub is deprecating Node 20 for JavaScript actions. This workflow opts into Node 24 via `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24=true`. We still see warnings because some upstream actions (or their internal dependencies) have not fully moved to Node 24 yet.

### Actions to Watch
- `actions/configure-pages@v5` (no newer major currently)
- `actions/upload-pages-artifact@v4` (bundles `actions/upload-artifact` internally)
- `actions/deploy-pages@v4` (no `v5` release currently)

### Follow-up
- Check for new majors that explicitly support Node 24.
- Update this repo when new majors are released.
- Reference: https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/

---

For more technical details, see the actual workflow files in `.github/workflows/`.
