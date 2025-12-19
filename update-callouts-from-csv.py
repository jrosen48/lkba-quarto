#!/usr/bin/env python3
"""
Update all callouts in trail files from the master CSV.
This script will:
1. Remove all existing callouts from trail files
2. Insert callouts from CSV in their correct trail files
3. Format callouts with proper Quarto syntax
4. Add media type comments
"""

import csv
import re
import glob
import os
import shutil
from collections import defaultdict

# Mapping of chapter names to trail numbers
CHAPTER_TO_TRAIL = {
    'Seven Islands': 1,
    'Ijams Riverside': 2,
    'Lakeshore Park': 3,
    'High Ground Park': 4,
    'UT Arboretum': 5,
    'Knox-Blount Greenway': 6,
    'Sequoyah Park': 7,
    'Ijams Crag': 8,
    'William Hastie': 9,
    "Sharp's Ridge": 10,
    'Norris Dam': 11,
    'House Mountain': 12,
    'Aspire Park': 13,
    'Emory Falls': 14,
    'Obed Point': 15,
    'Bandy Creek': 16,
    'Fall Branch Falls': 17,
    'Twin Arches': 18,
    'Angel Falls': 19,
    'Honey Creek': 20,
    'Spruce Flats Falls': 21,
    'Little River': 22,
    'Mouse Creek': 23,
    'Middle Prong': 24,
    'Abrams Creek': 25,
    'Look Rock': 26,
    'Chestnut Top': 27,
    'Abrams Falls': 28,
    'Andrews Bald': 29,
    'Alum Cave': 30,
}

def parse_trail_number(filename):
    """Extract trail number from filename."""
    match = re.search(r'Trail_(\d+)__', filename)
    return int(match.group(1)) if match else None

def load_callouts_from_csv(csv_path):
    """Load callouts from master CSV, organized by trail number."""
    callouts_by_trail = defaultdict(list)

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            chapter = row['Chapter'].strip()
            title = row['Title'].strip()
            text = row['Text'].strip()
            notes = row['Notes'].strip()

            trail_num = CHAPTER_TO_TRAIL.get(chapter)
            if trail_num is None:
                print(f"WARNING: Unknown chapter '{chapter}' in CSV - skipping")
                continue

            callouts_by_trail[trail_num].append({
                'title': title,
                'text': text,
                'notes': notes
            })

    return callouts_by_trail

def remove_existing_callouts(content):
    """Remove all existing callout blocks from content."""
    # Pattern to match callout blocks
    callout_pattern = re.compile(
        r':::\s*\{\.callout[^\}]*\}.*?^:::\s*$',
        re.MULTILINE | re.DOTALL
    )

    # Remove callouts
    content = callout_pattern.sub('', content)

    # Clean up multiple blank lines (more than 2 consecutive)
    content = re.sub(r'\n{3,}', '\n\n', content)

    return content

def format_media_type(notes):
    """Convert notes to standardized media type comment."""
    notes_lower = notes.lower()

    if 'illustration' in notes_lower:
        return 'illustration'
    elif 'photo' in notes_lower:
        return 'photo'
    elif 'no drawing' in notes_lower or 'no photo' in notes_lower or notes_lower == 'none':
        return 'none'
    else:
        # Default to none if unclear
        return 'none'

def create_callout_block(callout):
    """Format a callout with proper Quarto syntax."""
    media_type = format_media_type(callout['notes'])

    # Build the callout block with Media comment INSIDE (before closing :::)
    lines = []
    lines.append('::: {.callout-note appearance="simple" icon="true"}')
    lines.append(f"#### {callout['title']}")
    lines.append('')
    lines.append(callout['text'])
    lines.append('')
    lines.append(f'<!-- Media: {media_type} -->')
    lines.append(':::')
    lines.append('')

    return '\n'.join(lines)

def find_insertion_point(content):
    """
    Find the best insertion point for callouts.
    Inserts before '### Nearby' if it exists, otherwise before the last section.
    """
    # Try to find "### Nearby"
    nearby_match = re.search(r'^### Nearby\s*$', content, re.MULTILINE)
    if nearby_match:
        return nearby_match.start()

    # If no Nearby section, insert before the end (after last content)
    # Find the last ### heading
    headings = list(re.finditer(r'^### ', content, re.MULTILINE))
    if headings:
        # Insert before the last heading
        return headings[-1].start()

    # If no headings found, insert at end
    return len(content)

def update_trail_file(trail_file, callouts):
    """Update a single trail file with callouts from CSV."""
    with open(trail_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove existing callouts
    content = remove_existing_callouts(content)

    if not callouts:
        # No callouts for this trail, just write back the cleaned content
        with open(trail_file, 'w', encoding='utf-8') as f:
            f.write(content)
        return

    # Find insertion point
    insertion_point = find_insertion_point(content)

    # Build callout blocks
    callout_blocks = []
    for callout in callouts:
        callout_blocks.append(create_callout_block(callout))

    # Join all callouts
    callouts_text = '\n'.join(callout_blocks)

    # Insert callouts
    new_content = content[:insertion_point] + '\n' + callouts_text + '\n' + content[insertion_point:]

    # Clean up any excessive blank lines
    new_content = re.sub(r'\n{4,}', '\n\n\n', new_content)

    # Write updated content
    with open(trail_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

def main():
    print("=" * 80)
    print("UPDATING CALLOUTS FROM MASTER CSV")
    print("=" * 80)
    print()

    # Load callouts from CSV
    print("Loading callouts from callouts-master.csv...")
    callouts_by_trail = load_callouts_from_csv('callouts-master.csv')

    total_callouts = sum(len(calls) for calls in callouts_by_trail.values())
    print(f"Loaded {total_callouts} callouts for {len(callouts_by_trail)} trails")
    print()

    # Create backup directory
    backup_dir = 'trail_backups'
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
        print(f"Created backup directory: {backup_dir}/")

    # Get all trail files
    trail_files = sorted(glob.glob('Trail_*.qmd'))
    print(f"Found {len(trail_files)} trail files")
    print()

    # Process each trail file
    print("Processing files...")
    print("-" * 80)

    for trail_file in trail_files:
        trail_num = parse_trail_number(trail_file)
        if trail_num is None:
            continue

        # Backup original file
        backup_path = os.path.join(backup_dir, os.path.basename(trail_file))
        shutil.copy2(trail_file, backup_path)

        # Get callouts for this trail
        callouts = callouts_by_trail.get(trail_num, [])

        # Update the file
        update_trail_file(trail_file, callouts)

        if callouts:
            print(f"✓ Trail {trail_num:2d}: Updated with {len(callouts)} callout(s)")
        else:
            print(f"○ Trail {trail_num:2d}: No callouts (cleaned existing)")

    print("-" * 80)
    print()
    print("✓ All trail files updated successfully!")
    print(f"✓ Backups saved to: {backup_dir}/")
    print()
    print("=" * 80)

if __name__ == '__main__':
    main()
