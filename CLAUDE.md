# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Quarto book project titled "Little Kids, Big Adventures: A Guide to Family Hikes Around Knoxville" scheduled for publication by UT Press in 2026. The book contains 30 family-friendly hiking trails organized into three geographic regions: Knoxville, the Cumberland Plateau, and the Great Smoky Mountains National Park.

## Build and Render Commands

### Full Book Rendering
```bash
quarto render
```
This renders the entire book to HTML (outputs to `docs/`), DOCX, and PDF formats as configured in `_quarto.yml`.

### Individual Chapter Rendering
To render a single chapter as DOCX (useful for editorial review):
```bash
quarto render Trail_1__Seven_Islands.qmd --to docx
```

### Batch Chapter Export
To export all chapters as individual DOCX files (numbered sequentially):
```bash
./create-chapters.sh
```
This creates numbered DOCX files in `docx_chapters/` directory, preserving the book's chapter order.

### Preview the Book
```bash
quarto preview
```
Opens a live-reloading preview in your browser.

## Book Architecture

### Configuration Structure
- **`_quarto.yml`**: Main configuration file defining:
  - Book metadata (title, authors, date)
  - Output formats (HTML, DOCX, PDF)
  - Chapter structure organized by geographic regions
  - Output directory set to `docs/` for GitHub Pages deployment

### Content Organization
The book uses a prefix-based naming convention to control ordering:

1. **AAA-prefixed files**: Introductory material and user guide sections
2. **Sec-prefixed files**: Geographic section dividers (used as `part:` in config)
3. **Trail_N__Name.qmd**: Individual trail chapters (numbered 1-30)
4. **ZZZ-prefixed files**: End matter (acknowledgments, appendices, author info)
5. **zzz-prefixed files**: Additional back matter

### Chapter Structure
Each trail chapter follows a consistent template:
- **Overview**: Narrative description of the hike
- **Key Characteristics**: Structured table with trail metadata (distance, elevation, pet policy, accessibility, etc.)
- **Map**: Embedded image from `maps/` directory
- **Directions to the Trailhead**: GPS coordinates and parking information
- **Trail Description**: Mile-by-mile breakdown table
- **Callout boxes**: Educational content about flora, fauna, or geology (uses Quarto callout syntax)
- **Nearby**: Suggestions for additional activities or locations

### Callout Management
The repository includes a Python utility (`callouts.py`) for extracting and managing callout content:

```bash
python callouts.py . callouts.csv
```

This extracts all Quarto callout blocks from `.qmd` files and exports them to CSV for editorial review or content management.

## Deployment

The project uses GitHub Actions (`.github/workflows/publish.yml`) to:
1. Auto-render the book on every push to `master`
2. Commit the rendered output to `docs/`
3. Deploy via GitHub Pages

The workflow runs `quarto render` and automatically commits changes to the `docs/` directory.

## Key Directories

- **`docs/`**: Rendered HTML output for GitHub Pages (git-tracked)
- **`docx_chapters/`**: Individual chapter DOCX exports (git-ignored)
- **`img/`**: Photos for trail chapters
- **`maps/`**: Trail map images
- **`illustrations/`**: Educational illustrations for callout boxes
- **`final maps as of jan 26 2025/`**: Source map files
- **`site_libs/`**: Quarto-generated dependencies (being removed based on git status)

## Content Guidelines

When editing trail chapters, maintain:
- Consistent table structure for Key Characteristics and Trail Descriptions
- Callout boxes use `{.callout-note appearance="simple" icon="true"}` format
- Images referenced with relative paths: `img/filename.jpg` or `maps/trail-XX-map.jpeg`
- Mile markers in Trail Description tables match actual trail distances
- GPS coordinates in decimal format

## Important Notes

- The book is a work-in-progress with some sections still in draft form
- Copyright is held by Katie Rosenberg and Joshua Rosenberg (© 2025)
- Bibliography managed via `references.bib`
- Custom CSS styling in `style.css`
- Some content contains `.Rhistory` and `.Rproj` files indicating R/RStudio was previously used, but current workflow is pure Quarto
