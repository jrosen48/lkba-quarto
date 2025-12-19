#!/usr/bin/env python3
"""
Analyze callout distribution across the book.
Shows which trails have callouts, which don't, and extracts callout titles.
"""

import os
import re
import glob
from collections import defaultdict

def parse_trail_number(filename):
    """Extract trail number from filename like 'Trail_1__Seven_Islands.qmd'"""
    match = re.search(r'Trail_(\d+)__', filename)
    if match:
        return int(match.group(1))
    return None

def get_trail_name(filename):
    """Extract trail name from filename like 'Trail_1__Seven_Islands.qmd'"""
    match = re.search(r'Trail_\d+__(.+)\.qmd', filename)
    if match:
        return match.group(1).replace('_', ' ')
    return filename

def extract_callouts(text):
    """
    Extract callout blocks from the text.
    Returns a list of dicts with 'title' and 'content'.
    """
    callouts = []

    # Pattern to match callout blocks
    callout_pattern = re.compile(
        r':::\s*\{\.callout[^\}]*\}\s*(.*?)^:::\s*$',
        re.MULTILINE | re.DOTALL
    )

    matches = callout_pattern.findall(text)

    for match in matches:
        # Try to extract title (#### Title or ### Title)
        title_match = re.search(r'^#{2,4}\s+(.+?)$', match, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else "[No title]"

        # Get first line of content (after title) for preview
        content_lines = match.strip().split('\n')
        # Skip the title line if present
        content_preview = ""
        for line in content_lines:
            if not line.strip().startswith('#') and line.strip():
                content_preview = line.strip()[:60]
                if len(line.strip()) > 60:
                    content_preview += "..."
                break

        callouts.append({
            'title': title,
            'preview': content_preview
        })

    return callouts

def main():
    """Analyze callout distribution across all trail files."""

    # Get all trail files
    trail_files = sorted(glob.glob('Trail_*.qmd'))

    # Dictionary to store callout info by trail number
    trail_callouts = {}
    trails_without_callouts = []

    print("=" * 80)
    print("CALLOUT DISTRIBUTION ANALYSIS")
    print("=" * 80)
    print()

    for trail_file in trail_files:
        trail_num = parse_trail_number(trail_file)
        if trail_num is None:
            continue

        trail_name = get_trail_name(trail_file)

        with open(trail_file, 'r', encoding='utf-8') as f:
            text = f.read()

        callouts = extract_callouts(text)

        if callouts:
            trail_callouts[trail_num] = {
                'name': trail_name,
                'file': trail_file,
                'callouts': callouts
            }
        else:
            trails_without_callouts.append((trail_num, trail_name))

    # Print trails WITH callouts
    print(f"TRAILS WITH CALLOUTS ({len(trail_callouts)} trails):")
    print("-" * 80)

    for trail_num in sorted(trail_callouts.keys()):
        info = trail_callouts[trail_num]
        print(f"\nTrail {trail_num}: {info['name']}")
        print(f"  File: {info['file']}")
        print(f"  Callouts: {len(info['callouts'])}")

        for i, callout in enumerate(info['callouts'], 1):
            print(f"    {i}. {callout['title']}")
            if callout['preview']:
                print(f"       Preview: {callout['preview']}")

    # Print trails WITHOUT callouts
    print()
    print("=" * 80)
    print(f"TRAILS WITHOUT CALLOUTS ({len(trails_without_callouts)} trails):")
    print("-" * 80)

    for trail_num, trail_name in sorted(trails_without_callouts):
        print(f"  Trail {trail_num:2d}: {trail_name}")

    # Summary statistics
    print()
    print("=" * 80)
    print("SUMMARY:")
    print("-" * 80)
    print(f"  Total trail chapters: {len(trail_files)}")
    print(f"  Trails with callouts: {len(trail_callouts)}")
    print(f"  Trails without callouts: {len(trails_without_callouts)}")

    total_callouts = sum(len(info['callouts']) for info in trail_callouts.values())
    print(f"  Total callouts: {total_callouts}")

    if trail_callouts:
        avg_callouts = total_callouts / len(trail_callouts)
        print(f"  Average callouts per trail (with callouts): {avg_callouts:.1f}")

    # Coverage percentage
    coverage = (len(trail_callouts) / len(trail_files)) * 100
    print(f"  Coverage: {coverage:.1f}% of trails have callouts")
    print("=" * 80)

if __name__ == '__main__':
    main()
