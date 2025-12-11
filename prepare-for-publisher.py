#!/usr/bin/env python3
"""
Script to prepare book files for publisher:
1. Extract all image references from each .qmd file
2. Copy all images to publisher_images/ folder
3. Add a "Figures included" section at the top of each chapter
"""

import os
import re
import shutil
from pathlib import Path

def extract_images_from_qmd(qmd_path):
    """Extract all image references from a .qmd file."""
    with open(qmd_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match ![...](path/to/image.ext)
    pattern = r'!\[.*?\]\((.*?\.(?:jpg|jpeg|png|JPG|JPEG|PNG))(?:\{[^}]*\})?\)'
    matches = re.findall(pattern, content)

    return matches

def get_chapter_title(qmd_path):
    """Extract the chapter title from the .qmd file."""
    with open(qmd_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Look for ## heading (main chapter title)
            if line.startswith('## '):
                return line.strip('# \n')
    # Fallback to filename
    return Path(qmd_path).stem

def add_figures_list_to_chapter(qmd_path, images):
    """Add a 'Figures included' section at the top of the chapter."""
    if not images:
        return  # No images to list

    with open(qmd_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if figures list already exists
    if '**Figures included in this chapter:**' in content:
        print(f"  Figures list already exists in {Path(qmd_path).name}, skipping...")
        return

    # Find the first ## heading
    lines = content.split('\n')
    insert_index = None

    for i, line in enumerate(lines):
        if line.startswith('## '):
            # Insert after the heading (skip blank lines)
            insert_index = i + 1
            while insert_index < len(lines) and lines[insert_index].strip() == '':
                insert_index += 1
            break

    if insert_index is None:
        print(f"  Warning: No ## heading found in {Path(qmd_path).name}, skipping...")
        return

    # Create the figures list
    figures_section = ['\n**Figures included in this chapter:**\n']
    for img_path in images:
        # Convert path to filename
        filename = Path(img_path).name
        figures_section.append(f'- {filename}')
    figures_section.append('\n')

    # Insert the figures list
    lines.insert(insert_index, '\n'.join(figures_section))

    # Write back to file
    with open(qmd_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print(f"  Added figures list to {Path(qmd_path).name}")

def copy_images_to_publisher_folder(qmd_files, output_dir='publisher_images'):
    """Copy all images referenced in .qmd files to a publisher folder."""
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # Track all images and which chapters use them
    all_images = {}  # {image_path: [chapters]}

    for qmd_file in qmd_files:
        chapter_name = get_chapter_title(qmd_file)
        images = extract_images_from_qmd(qmd_file)

        for img_path in images:
            if img_path not in all_images:
                all_images[img_path] = []
            all_images[img_path].append(chapter_name)

    # Copy images
    print(f"\nCopying {len(all_images)} unique images to {output_dir}/...")
    copied_count = 0

    for img_path, chapters in all_images.items():
        src = Path(img_path)
        if not src.exists():
            print(f"  Warning: Image not found: {img_path}")
            continue

        # Determine destination based on source directory
        if 'maps/' in img_path:
            dest_dir = output_path / 'maps'
        elif 'illustrations/' in img_path:
            dest_dir = output_path / 'illustrations'
        elif 'img/' in img_path:
            dest_dir = output_path / 'img'
        else:
            dest_dir = output_path / 'other'

        dest_dir.mkdir(exist_ok=True)
        dest = dest_dir / src.name

        shutil.copy2(src, dest)
        copied_count += 1

    print(f"  Copied {copied_count} images successfully!")

    # Create a manifest file
    manifest_path = output_path / 'image_manifest.txt'
    with open(manifest_path, 'w', encoding='utf-8') as f:
        f.write("Image Manifest - Which chapters use which images\n")
        f.write("=" * 60 + "\n\n")

        for img_path in sorted(all_images.keys()):
            f.write(f"{img_path}\n")
            for chapter in all_images[img_path]:
                f.write(f"  - Used in: {chapter}\n")
            f.write("\n")

    print(f"  Created manifest file: {manifest_path}")

    return all_images

def main():
    # Get all .qmd files
    qmd_files = sorted(Path('.').glob('*.qmd'))

    print(f"Found {len(qmd_files)} .qmd files\n")

    # Step 1: Copy images to publisher folder
    print("=" * 60)
    print("STEP 1: Copying images to publisher_images folder")
    print("=" * 60)
    all_images = copy_images_to_publisher_folder(qmd_files)

    # Step 2: Add figures list to each chapter
    print("\n" + "=" * 60)
    print("STEP 2: Adding figures list to chapters")
    print("=" * 60)

    for qmd_file in qmd_files:
        images = extract_images_from_qmd(qmd_file)
        if images:
            print(f"\n{qmd_file.name}: {len(images)} images")
            add_figures_list_to_chapter(qmd_file, images)

    print("\n" + "=" * 60)
    print("COMPLETE!")
    print("=" * 60)
    print(f"\nSummary:")
    print(f"  - {len(all_images)} unique images copied to publisher_images/")
    print(f"  - Image manifest created at publisher_images/image_manifest.txt")
    print(f"  - Figures lists added to chapters with images")

if __name__ == '__main__':
    main()
