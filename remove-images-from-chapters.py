#!/usr/bin/env python3
"""
Script to remove image embeds from chapters while keeping the figure listings.
This prepares the .qmd files for publisher submission where images are separate.
"""

import re
from pathlib import Path

def remove_image_embeds(qmd_path):
    """
    Remove image markdown syntax from .qmd file.
    Replaces ![...](path) with a comment noting the image was removed.
    """
    with open(qmd_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to match ![...](path) including optional attributes like {width="300"}
    pattern = r'!\[([^\]]*)\]\(([^)]+\.(?:jpg|jpeg|png|JPG|JPEG|PNG))\)(?:\{[^}]*\})?'

    # Count matches
    matches = re.findall(pattern, content)
    if not matches:
        return 0  # No images to remove

    # Replace each image with a comment
    def replace_func(match):
        alt_text = match.group(1)
        img_path = match.group(2)
        filename = Path(img_path).name
        return f'<!-- IMAGE REMOVED FOR PUBLISHER: {filename} -->'

    new_content = re.sub(pattern, replace_func, content)

    # Write back to file
    with open(qmd_path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return len(matches)

def main():
    # Get all .qmd files
    qmd_files = sorted(Path('.').glob('*.qmd'))

    print("=" * 60)
    print("Removing image embeds from chapters")
    print("(Keeping 'Figures included' listings at top)")
    print("=" * 60)

    total_removed = 0

    for qmd_file in qmd_files:
        removed = remove_image_embeds(qmd_file)
        if removed > 0:
            print(f"  {qmd_file.name}: Removed {removed} image(s)")
            total_removed += removed

    print("\n" + "=" * 60)
    print(f"COMPLETE! Removed {total_removed} images from {len(qmd_files)} files")
    print("=" * 60)
    print("\nThe .qmd files now have:")
    print("  ✓ 'Figures included in this chapter' lists at top")
    print("  ✓ Image embeds replaced with <!-- IMAGE REMOVED --> comments")
    print("\nReady to regenerate DOCX files for publisher!")

if __name__ == '__main__':
    main()
