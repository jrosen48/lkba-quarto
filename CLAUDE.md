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

**Note:** The `create-chapters.sh` script automatically generates the publisher manifest (see below) at the start of each run to ensure it stays synchronized with the book structure.

### Generate Publisher Manifest
To generate a table of contents showing the book's organization for the publisher:
```bash
python3 generate-manifest.py
```
This script:
- Reads the chapter structure from `_quarto.yml`
- Generates `PUBLISHER-MANIFEST.md` with sequential chapter numbering (1-46)
- Shows part divisions and geographic sections
- Includes both human-readable titles and source filenames
- Provides a summary of content breakdown (trails, sections, front/back matter)

The manifest is automatically regenerated when running `./create-chapters.sh`, ensuring it always reflects the current book structure.

### Collect Images for Publisher Delivery
To collect only the images that are actually referenced in the book (excludes unused images from the writing process):
```bash
python3 collect-images.py
```
This script:
- Scans all .qmd files for the "Figures included in this chapter:" sections
- Copies only the referenced images to `publisher_images/` directory
- Preserves the directory structure (`maps/`, `img/`, `illustrations/`)
- Provides a summary showing images found, copied, and any missing files

The output directory `publisher_images/` contains a clean set of images ready for publisher delivery, with 98 images organized by type (31 maps, 60 photos, 5 illustrations as of Dec 2025).

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

## Image Management

### How Images Work in This Book

Each chapter uses a two-part system for managing images:

1. **"Figures included in this chapter:" list** at the top of each .qmd file
   - This is the **single source of truth** for which images belong to a chapter
   - Used by `collect-images.py` to collect images for publisher delivery
   - Serves as a quick inventory for both authors and publisher

2. **Inline placement markers** in the content: `<!-- IMAGE: filename.jpg -->`
   - Marks where each image should be placed in the final layout
   - Images are NOT embedded in DOCX output (commented out for publisher)
   - Publisher will place images manually using these markers

### Updating Images

**To replace an image with the same filename:**
1. Replace the file in the appropriate directory (`maps/`, `img/`, or `illustrations/`)
2. Re-run `python3 collect-images.py`
3. No .qmd file changes needed

**To replace an image with a new filename:**
1. Add the new image file to the appropriate directory
2. Update the filename in the "Figures included in this chapter:" list
3. Update the corresponding `<!-- IMAGE: filename -->` comment in the content
4. Re-run `python3 collect-images.py`

Both references must match to ensure consistency between the collection script and publisher layout instructions.

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
