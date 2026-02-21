#!/usr/bin/env python3
"""
Export all callouts from trail chapters to CSV.
"""

import re
import csv
from pathlib import Path

def extract_callouts_from_file(filepath):
    """Extract all callouts from a trail file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract trail number and name from the first heading
    # Handle both "Trail 19:" and "Trail 19 :" (with space before colon)
    trail_match = re.search(r'^##\s+Trail\s+(\d+)\s*:\s+(.+?)$', content, re.MULTILINE)
    if not trail_match:
        return []

    trail_number = trail_match.group(1)
    trail_name = trail_match.group(2).strip()

    # Find all callout blocks
    callout_pattern = r':::\s*\{\.callout-note[^}]*\}\s*####\s*(.+?)\s*\n\s*(.*?)\s*:::'

    callouts = []
    for match in re.finditer(callout_pattern, content, re.DOTALL):
        title = match.group(1).strip()
        full_block = match.group(2).strip()

        # Extract image filename
        image_match = re.search(r'<!--\s*IMAGE:\s*(?:img/|illustrations/)?(.+?)\s*-->', full_block)
        image_file = image_match.group(1) if image_match else ''

        # Extract media type
        media_match = re.search(r'<!--\s*Media:\s*(\w+)\s*-->', full_block)
        media_type = media_match.group(1) if media_match else ''

        # Remove IMAGE and Media comments from the text
        text_block = re.sub(r'<!--\s*IMAGE:.*?-->', '', full_block, flags=re.DOTALL)
        text_block = re.sub(r'<!--\s*Media:.*?-->', '', text_block, flags=re.DOTALL)
        text_block = re.sub(r'<!--\s*NOTE TO PUBLISHER:.*?-->', '', text_block, flags=re.DOTALL)

        # Clean up extra whitespace
        text_block = re.sub(r'\n\s*\n\s*\n+', '\n\n', text_block)
        text_block = text_block.strip()

        callouts.append({
            'trail_number': trail_number,
            'trail_name': trail_name,
            'title': title,
            'text': text_block,
            'media_type': media_type,
            'image_file': image_file
        })

    return callouts

def main():
    print("=" * 80)
    print("EXTRACTING ALL CALLOUTS TO CSV")
    print("=" * 80)
    print()

    # Find all trail files
    trail_files = sorted(Path('.').glob('Trail_*.qmd'))

    all_callouts = []

    for trail_file in trail_files:
        print(f"Processing {trail_file.name}...")
        callouts = extract_callouts_from_file(trail_file)
        all_callouts.extend(callouts)
        if callouts:
            print(f"  Found {len(callouts)} callout(s)")

    print()
    print(f"Total callouts found: {len(all_callouts)}")
    print()

    # Write to CSV
    output_file = 'all-callouts-export.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['trail_number', 'trail_name', 'title', 'text', 'media_type', 'image_file'])
        writer.writeheader()
        writer.writerows(all_callouts)

    print(f"✓ Exported to {output_file}")
    print()
    print("=" * 80)
    print("DONE!")
    print("=" * 80)

if __name__ == '__main__':
    main()
