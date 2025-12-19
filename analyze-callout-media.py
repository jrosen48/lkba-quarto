#!/usr/bin/env python3
"""
Analyze what images/illustrations are needed for callouts.
Shows which ones exist and which ones are missing.
"""

import csv
import os
import glob
from collections import defaultdict

# Map chapter names to trail numbers
CHAPTER_TO_TRAIL = {
    'Seven Islands': 1, 'Ijams Riverside': 2, 'Lakeshore Park': 3,
    'High Ground Park': 4, 'UT Arboretum': 5, 'Knox-Blount Greenway': 6,
    'Sequoyah Park': 7, 'Ijams Crag': 8, 'William Hastie': 9,
    "Sharp's Ridge": 10, 'Norris Dam': 11, 'House Mountain': 12,
    'Aspire Park': 13, 'Emory Falls': 14, 'Obed Point': 15,
    'Bandy Creek': 16, 'Fall Branch Falls': 17, 'Twin Arches': 18,
    'Angel Falls': 19, 'Honey Creek': 20, 'Spruce Flats Falls': 21,
    'Little River': 22, 'Mouse Creek': 23, 'Middle Prong': 24,
    'Abrams Creek': 25, 'Look Rock': 26, 'Chestnut Top': 27,
    'Abrams Falls': 28, 'Andrews Bald': 29, 'Alum Cave': 30,
}

def normalize_for_filename(text):
    """Convert title to potential filename."""
    # Remove special characters, convert to lowercase
    import re
    text = text.lower()
    text = re.sub(r"[''']", '', text)  # Remove apostrophes
    text = re.sub(r'[^\w\s-]', '', text)  # Remove other special chars
    text = re.sub(r'\s+', '-', text)  # Replace spaces with hyphens
    return text

def find_matching_files(title, directories):
    """Find potential matching files for a callout title."""
    normalized = normalize_for_filename(title)
    matches = []

    for directory in directories:
        if not os.path.exists(directory):
            continue

        # Check for exact match
        for ext in ['.png', '.jpg', '.jpeg', '.pdf']:
            filepath = os.path.join(directory, normalized + ext)
            if os.path.exists(filepath):
                matches.append(filepath)

        # Check for partial matches
        for filepath in glob.glob(os.path.join(directory, '*')):
            filename = os.path.basename(filepath).lower()
            if normalized in filename or filename.replace('-', ' ') in title.lower():
                if filepath not in matches:
                    matches.append(filepath)

    return matches

def main():
    print("=" * 100)
    print("CALLOUT MEDIA ANALYSIS")
    print("=" * 100)
    print()

    # Load callouts from CSV
    callouts_by_media = {
        'illustration': [],
        'photo': [],
        'none': []
    }

    with open('callouts-master.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            chapter = row['Chapter'].strip()
            title = row['Title'].strip()
            notes = row['Notes'].strip().lower()

            trail_num = CHAPTER_TO_TRAIL.get(chapter)

            if 'illustration' in notes:
                media_type = 'illustration'
            elif 'photo' in notes:
                media_type = 'photo'
            else:
                media_type = 'none'

            callouts_by_media[media_type].append({
                'trail': trail_num,
                'chapter': chapter,
                'title': title,
                'notes': notes
            })

    # Analyze illustrations
    print(f"ILLUSTRATIONS NEEDED ({len(callouts_by_media['illustration'])} callouts):")
    print("-" * 100)

    missing_illustrations = []
    existing_illustrations = []

    for callout in sorted(callouts_by_media['illustration'], key=lambda x: x['trail']):
        matches = find_matching_files(callout['title'], ['illustrations/', 'img/'])

        if matches:
            existing_illustrations.append(callout)
            print(f"✓ Trail {callout['trail']:2d} - {callout['title']}")
            for match in matches:
                print(f"    Found: {match}")
        else:
            missing_illustrations.append(callout)
            print(f"✗ Trail {callout['trail']:2d} - {callout['title']}")
            print(f"    Missing: illustrations/{normalize_for_filename(callout['title'])}.png")

    print()
    print(f"PHOTOS NEEDED ({len(callouts_by_media['photo'])} callouts):")
    print("-" * 100)

    missing_photos = []
    existing_photos = []

    for callout in sorted(callouts_by_media['photo'], key=lambda x: x['trail']):
        matches = find_matching_files(callout['title'], ['img/', 'maps/'])

        if matches:
            existing_photos.append(callout)
            print(f"✓ Trail {callout['trail']:2d} - {callout['title']}")
            for match in matches:
                print(f"    Found: {match}")
        else:
            missing_photos.append(callout)
            print(f"✗ Trail {callout['trail']:2d} - {callout['title']}")
            print(f"    Missing: img/{normalize_for_filename(callout['title'])}.jpg")

    print()
    print(f"NO MEDIA NEEDED ({len(callouts_by_media['none'])} callouts):")
    print("-" * 100)
    for callout in sorted(callouts_by_media['none'], key=lambda x: x['trail']):
        print(f"○ Trail {callout['trail']:2d} - {callout['title']} (no media needed)")

    # Summary
    print()
    print("=" * 100)
    print("SUMMARY:")
    print("-" * 100)
    print(f"Illustrations:")
    print(f"  Needed: {len(callouts_by_media['illustration'])}")
    print(f"  Existing: {len(existing_illustrations)}")
    print(f"  Missing: {len(missing_illustrations)}")
    print()
    print(f"Photos:")
    print(f"  Needed: {len(callouts_by_media['photo'])}")
    print(f"  Existing: {len(existing_photos)}")
    print(f"  Missing: {len(missing_photos)}")
    print()
    print(f"No media needed: {len(callouts_by_media['none'])}")
    print("=" * 100)

    # Write missing list to file
    if missing_illustrations or missing_photos:
        with open('missing-callout-media.txt', 'w', encoding='utf-8') as f:
            f.write("MISSING CALLOUT MEDIA\n")
            f.write("=" * 80 + "\n\n")

            if missing_illustrations:
                f.write(f"MISSING ILLUSTRATIONS ({len(missing_illustrations)}):\n")
                f.write("-" * 80 + "\n")
                for callout in missing_illustrations:
                    f.write(f"Trail {callout['trail']:2d}: {callout['title']}\n")
                    f.write(f"  Suggested filename: illustrations/{normalize_for_filename(callout['title'])}.png\n")
                f.write("\n")

            if missing_photos:
                f.write(f"MISSING PHOTOS ({len(missing_photos)}):\n")
                f.write("-" * 80 + "\n")
                for callout in missing_photos:
                    f.write(f"Trail {callout['trail']:2d}: {callout['title']}\n")
                    f.write(f"  Suggested filename: img/{normalize_for_filename(callout['title'])}.jpg\n")

        print()
        print(f"Missing media list saved to: missing-callout-media.txt")

if __name__ == '__main__':
    main()
