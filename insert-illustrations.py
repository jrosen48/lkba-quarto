#!/usr/bin/env python3
"""
Insert illustration references into callout blocks.
Matches illustrations to callouts and inserts <!-- IMAGE: ... --> comments.
"""

import re
import glob
import os
import shutil

# Map callout titles to illustration filenames
ILLUSTRATION_MAP = {
    'Paw Paw': 'pawpaw.jpg',  # No PNG available, use JPG
    'Eastern Bluebird': 'bluebird.PNG',
    'Blue Phlox': 'phlox.PNG',
    'Elm Tree': 'elm.png',
    'Eastern Box Turtle': 'turtle.png',
    'Lichen': 'lichenwithlabels.png',  # Use the labeled version
    'Trillium': 'trillium.PNG',
    'Timber Rattlesnake': 'rattlesnake.PNG',
    'Eastern Copperhead': 'copperhead.PNG',
    'Blue Ridge Two-Lined Salamander': 'BR2linedsalamader.png',
    'Mountain Laurel': 'laurel.PNG',
    'Rosebay Rhododendron': 'rhodo.PNG',
    'Jordans Red Cheek': 'red cheeked.PNG',
}

def insert_illustration_in_callout(content, title, illustration_file):
    """Insert illustration reference into a specific callout."""
    # Pattern to find the callout with this title
    # We want to insert the image AFTER the text, BEFORE the Media comment

    # Find the callout block with this title
    pattern = rf'(:::\s*\{{\.callout-note[^\}}]*\}}\s*####\s*{re.escape(title)}\s*.*?)(<!-- Media:)'

    def replace_func(match):
        before_media = match.group(1)
        media_comment = match.group(2)

        # Insert the illustration reference before the Media comment
        return f"{before_media}\n<!-- IMAGE: illustrations/{illustration_file} -->\n\n{media_comment}"

    # Apply replacement
    new_content = re.sub(pattern, replace_func, content, flags=re.DOTALL)

    return new_content

def process_file(filepath, illustrations_to_insert):
    """Process a trail file and insert illustrations."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    inserted = []

    # Insert each illustration that should be in this file
    for title, illustration_file in illustrations_to_insert:
        # Check if illustration already exists in this callout
        if f'illustrations/{illustration_file}' in content:
            continue  # Already inserted

        # Check if this callout title exists in the file
        if f'#### {title}' not in content:
            continue  # Callout not in this file

        content = insert_illustration_in_callout(content, title, illustration_file)

        # Check if insertion was successful
        if content != original:
            inserted.append(title)
            original = content

    return content, inserted

def main():
    print("=" * 80)
    print("INSERTING ILLUSTRATIONS INTO CALLOUTS")
    print("=" * 80)
    print()

    # Verify all illustration files exist
    print("Verifying illustration files...")
    missing = []
    for title, filename in ILLUSTRATION_MAP.items():
        filepath = os.path.join('illustrations', filename)
        if not os.path.exists(filepath):
            missing.append(f"{title} → {filename}")
        else:
            print(f"✓ {filename}")

    if missing:
        print("\nMissing illustration files:")
        for item in missing:
            print(f"  ✗ {item}")
        return

    print()
    print("-" * 80)
    print("Processing trail files...")
    print("-" * 80)

    # Backup directory
    backup_dir = 'trail_backups_illustrations'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    trail_files = sorted(glob.glob('Trail_*.qmd'))
    total_inserted = 0

    for trail_file in trail_files:
        # Backup
        shutil.copy2(trail_file, os.path.join(backup_dir, os.path.basename(trail_file)))

        # Process
        with open(trail_file, 'r', encoding='utf-8') as f:
            original = f.read()

        new_content, inserted = process_file(trail_file, ILLUSTRATION_MAP.items())

        if inserted:
            with open(trail_file, 'w', encoding='utf-8') as f:
                f.write(new_content)

            trail_num = int(re.search(r'Trail_(\d+)__', trail_file).group(1))
            print(f"✓ Trail {trail_num:2d}: Inserted {len(inserted)} illustration(s)")
            for title in inserted:
                print(f"    - {title}")
            total_inserted += len(inserted)

    print()
    print("=" * 80)
    print("SUMMARY:")
    print(f"  Total illustrations inserted: {total_inserted}")
    print(f"  Backups saved to: {backup_dir}/")
    print("=" * 80)
    print()

    # Show which illustrations weren't inserted (not in any trail)
    all_inserted_titles = set()
    for trail_file in trail_files:
        with open(trail_file, 'r') as f:
            content = f.read()
        for title in ILLUSTRATION_MAP.keys():
            if f'illustrations/{ILLUSTRATION_MAP[title]}' in content:
                all_inserted_titles.add(title)

    not_inserted = set(ILLUSTRATION_MAP.keys()) - all_inserted_titles
    if not_inserted:
        print("Illustrations not inserted (callout may not exist):")
        for title in sorted(not_inserted):
            print(f"  - {title}")

if __name__ == '__main__':
    main()
