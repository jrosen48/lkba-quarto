#!/usr/bin/env python3
"""
Script to collect only the images referenced in the book for publisher delivery.
This creates a clean set of images without the extras from the writing process.
"""

import os
import shutil
import glob
from pathlib import Path

OUTPUT_DIR = "publisher_images"

# Statistics
total_found = 0
total_copied = 0
total_missing = 0

def copy_image(image_ref, source_file):
    """Find and copy an image file to the output directory."""
    global total_found, total_copied, total_missing

    # Strip whitespace and "- " prefix
    image_ref = image_ref.strip().lstrip('- ').strip()

    # Skip empty lines
    if not image_ref:
        return

    total_found += 1

    # Check if the reference already has a directory path
    if '/' in image_ref:
        # Has a path (e.g., maps/filename.jpg)
        if os.path.isfile(image_ref):
            dest = os.path.join(OUTPUT_DIR, image_ref)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy2(image_ref, dest)
            print(f"✓ Copied: {image_ref} (from {source_file})")
            total_copied += 1
        else:
            print(f"✗ Missing: {image_ref} (referenced in {source_file})")
            total_missing += 1
    else:
        # No path - search in img/, maps/, and illustrations/
        found = False

        for directory in ['img', 'maps', 'illustrations']:
            filepath = os.path.join(directory, image_ref)
            if os.path.isfile(filepath):
                dest = os.path.join(OUTPUT_DIR, filepath)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.copy2(filepath, dest)
                print(f"✓ Copied: {filepath} (from {source_file})")
                total_copied += 1
                found = True
                break

        if not found:
            print(f"✗ Missing: {image_ref} (referenced in {source_file}, searched img/, maps/, illustrations/)")
            total_missing += 1

def main():
    """Main function to collect images."""
    global total_found, total_copied, total_missing

    # Remove old output directory if it exists
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)

    # Create fresh directory structure
    os.makedirs(os.path.join(OUTPUT_DIR, 'maps'), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, 'img'), exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, 'illustrations'), exist_ok=True)

    print("Collecting images referenced in .qmd files...")
    print()

    # Process all .qmd files
    qmd_files = glob.glob('*.qmd')

    for qmd_file in qmd_files:
        with open(qmd_file, 'r', encoding='utf-8') as f:
            in_figures_section = False
            seen_first_line = False  # Track if we've seen the first line after the header

            for line in f:
                # Check if we're entering the figures section
                if 'Figures included in this chapter:' in line:
                    in_figures_section = True
                    seen_first_line = False
                    continue

                # If we're in the figures section
                if in_figures_section:
                    # Skip the first blank line after the section header
                    if not seen_first_line and line.strip() == '':
                        seen_first_line = True
                        continue

                    # Mark that we've seen content
                    if line.strip() != '':
                        seen_first_line = True

                    # Check for end of section (blank line after seeing content, or new section header)
                    if seen_first_line and (line.strip() == '' or line.strip().startswith('#')):
                        in_figures_section = False
                        continue

                    # Process image references (lines starting with "- ")
                    if line.strip().startswith('- '):
                        copy_image(line, qmd_file)

    print()
    print("=" * 41)
    print("Summary:")
    print(f"  Images referenced: {total_found}")
    print(f"  Images copied:     {total_copied}")
    print(f"  Images missing:    {total_missing}")
    print("=" * 41)
    print()
    print(f"Publisher images collected in: {OUTPUT_DIR}/")

    # Show directory structure and file count
    print()
    print("Directory contents:")
    for directory in ['maps', 'img', 'illustrations']:
        dir_path = os.path.join(OUTPUT_DIR, directory)
        count = len([f for f in Path(dir_path).rglob('*') if f.is_file()])
        print(f"  {directory}/: {count} files")

if __name__ == '__main__':
    main()
