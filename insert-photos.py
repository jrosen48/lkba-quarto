#!/usr/bin/env python3
"""
Insert specific photo references into callouts.
"""

import re
import shutil

# Map callout titles to photo filenames
PHOTO_MAP = {
    'Appalachian Trail': 'app.jpg',
    'Black Bear': 'bear.jpg',
    'Red Spruce': 'spruce.jpeg',
}

def insert_photo_in_callout(content, title, photo_file):
    """Insert photo reference into a specific callout."""
    # Pattern to find the callout with this title
    # We want to insert the image AFTER the text, BEFORE the Media comment

    pattern = rf'(:::\s*\{{\.callout-note[^\}}]*\}}\s*####\s*{re.escape(title)}\s*.*?)(<!-- Media:)'

    def replace_func(match):
        before_media = match.group(1)
        media_comment = match.group(2)

        # Check if image already exists
        if f'img/{photo_file}' in before_media:
            return match.group(0)  # Already there, don't duplicate

        # Insert the photo reference before the Media comment
        return f"{before_media}\n<!-- IMAGE: img/{photo_file} -->\n\n{media_comment}"

    # Apply replacement
    new_content = re.sub(pattern, replace_func, content, flags=re.DOTALL)

    return new_content

def main():
    print("=" * 80)
    print("INSERTING PHOTOS INTO CALLOUTS")
    print("=" * 80)
    print()

    # Trail 3: Appalachian Trail
    print("Trail 3 (Lakeshore Park): Appalachian Trail")
    with open('Trail_3__Lakeshore_Park.qmd', 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = insert_photo_in_callout(content, 'Appalachian Trail', 'app.jpg')

    if content != new_content:
        shutil.copy2('Trail_3__Lakeshore_Park.qmd', 'trail_backups_illustrations/Trail_3__Lakeshore_Park.qmd')
        with open('Trail_3__Lakeshore_Park.qmd', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("  ✓ Inserted img/app.jpg")
    else:
        print("  ○ Already present")

    # Trail 28: Black Bear
    print("\nTrail 28 (Abrams Falls): Black Bear")
    with open('Trail_28__Abrams_Falls.qmd', 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = insert_photo_in_callout(content, 'Black Bear', 'bear.jpg')

    if content != new_content:
        shutil.copy2('Trail_28__Abrams_Falls.qmd', 'trail_backups_illustrations/Trail_28__Abrams_Falls.qmd')
        with open('Trail_28__Abrams_Falls.qmd', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("  ✓ Inserted img/bear.jpg")
    else:
        print("  ○ Already present")

    # Trail 30: Red Spruce
    print("\nTrail 30 (Alum Cave): Red Spruce")
    with open('Trail_30__Alum_Cave_Bluffs.qmd', 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = insert_photo_in_callout(content, 'Red Spruce', 'spruce.jpeg')

    if content != new_content:
        shutil.copy2('Trail_30__Alum_Cave_Bluffs.qmd', 'trail_backups_illustrations/Trail_30__Alum_Cave_Bluffs.qmd')
        with open('Trail_30__Alum_Cave_Bluffs.qmd', 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("  ✓ Inserted img/spruce.jpeg")
    else:
        print("  ○ Already present")

    print()
    print("=" * 80)
    print("DONE!")
    print("=" * 80)

if __name__ == '__main__':
    main()
