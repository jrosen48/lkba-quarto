#!/usr/bin/env python3
"""
Remove all callouts from trail files for DOCX generation.
Also removes any image references that were inside callouts.
"""

import re
from pathlib import Path

def remove_callouts_from_file(filepath):
    """Remove all callout blocks from a trail file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find and remove all callout blocks
    # Pattern matches from ::: {.callout-note...} through all content to the closing :::
    callout_pattern = r':::\s*\{\.callout-note.*?\}\s*####.*?:::'

    # Count callouts before removal
    callouts_found = len(re.findall(callout_pattern, content, re.DOTALL))

    # Remove all callouts
    new_content = re.sub(callout_pattern, '', content, flags=re.DOTALL)

    # Clean up multiple blank lines (max 2 consecutive blank lines)
    new_content = re.sub(r'\n\n\n+', '\n\n', new_content)

    return new_content, callouts_found

def update_figures_list(content):
    """Remove illustration/photo references from 'Figures included' section."""
    # Pattern to find the figures section
    figures_pattern = r'(\*\*Figures included in this chapter:\*\*\n\n)((?:- .+\n)+)'

    def filter_figures(match):
        header = match.group(1)
        figures_list = match.group(2)

        # Split into individual figure lines
        figures = figures_list.strip().split('\n')

        # Keep only lines that don't contain illustration or callout-related images
        # We want to keep maps and trail figures, but remove illustrations
        filtered = []
        for fig in figures:
            # Remove items from illustrations/ directory
            if 'illustrations/' in fig.lower():
                continue
            # Remove individual illustration files we know about
            if any(x in fig.lower() for x in [
                'bluebird.png', 'pawpaw.jpg', 'phlox.png', 'elm.png', 'turtle.png',
                'lichenwithlabels.png', 'trillium.png', 'rattlesnake.png',
                'copperhead.png', 'br2linedsalamader.png', 'laurel.png',
                'rhodo.png', 'red cheeked.png', 'fir.jpg', 'hemlock.jpg',
                'bigleaf-magnolia.jpeg', 'bear.jpg', 'spruce.jpeg', 'app.jpg',
                'jo-bsf-cliff.jpg', 'ijams marble callout.jpeg'
            ]):
                continue
            filtered.append(fig)

        if filtered:
            return header + '\n'.join(filtered) + '\n'
        else:
            return header

    return re.sub(figures_pattern, filter_figures, content)

def main():
    print("=" * 80)
    print("REMOVING CALLOUTS FROM TRAIL FILES")
    print("=" * 80)
    print()

    # Find all trail files
    trail_files = sorted(Path('.').glob('Trail_*.qmd'))

    total_callouts = 0

    for trail_file in trail_files:
        print(f"Processing {trail_file.name}...")

        # Remove callouts
        new_content, callouts_found = remove_callouts_from_file(trail_file)

        # Update figures list
        new_content = update_figures_list(new_content)

        # Write back to file
        with open(trail_file, 'w', encoding='utf-8') as f:
            f.write(new_content)

        if callouts_found > 0:
            print(f"  ✓ Removed {callouts_found} callout(s)")
            total_callouts += callouts_found
        else:
            print(f"  ○ No callouts found")

    print()
    print(f"Total callouts removed: {total_callouts}")
    print()
    print("=" * 80)
    print("DONE!")
    print("=" * 80)

if __name__ == '__main__':
    main()
