#!/usr/bin/env python3
"""
Update all trail chapter files to replace "Time Estimate - Hiking Fast"
with "Distance from Knoxville" in the Key Characteristics tables.
"""

import re
from pathlib import Path

# Mapping of trail numbers to driving times from Knoxville
DRIVING_TIMES = {
    1: "30 mins",
    2: "10-15 mins",
    3: "10-15 mins",
    4: "10-15 mins",
    5: "25-30 mins",
    6: "5-10 mins",
    7: "10-15 mins",
    8: "10-15 mins",
    9: "15 mins",
    10: "10 mins",
    11: "30 mins",
    12: "30 mins",
    13: "30 mins",  # Aspire Park
    14: "50 mins",
    15: "50 mins",
    16: "1 hr 30 mins",
    17: "1 hr 30 mins",
    18: "1 hr 45 mins",
    19: "1 hr 30 mins",
    20: "1 hr 30 mins",
    21: "50 mins",
    22: "1 hour",
    23: "1 hr 5 mins",
    24: "1 hr 5 mins",
    25: "55 mins",
    26: "45 mins",
    27: "45 mins",
    28: "1 hr 30 mins",
    29: "1 hr 45 mins",
    30: "1 hr 15 mins",
}

def update_trail_file(trail_num: int, driving_time: str) -> bool:
    """Update a single trail file's Key Characteristics table."""

    # Construct the filename
    trail_files = list(Path('.').glob(f'Trail_{trail_num}__*.qmd'))

    if not trail_files:
        print(f"⚠️  Trail {trail_num}: No file found")
        return False

    trail_file = trail_files[0]

    # Read the file
    with open(trail_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Try multiple patterns to match different "Time Estimate" variations
    patterns = [
        r'\|\s*Time Estimate - Hiking Fast\s*\|\s*[^|]*\|',  # "Time Estimate - Hiking Fast"
        r'\|\s*Time Estimate\s*\|\s*[^|]*\|',                # "Time Estimate"
    ]

    # Replacement with the new row
    replacement = f'| Distance from Knoxville | {driving_time:<24} |'

    pattern_found = False
    new_content = content

    # Try each pattern
    for pattern in patterns:
        if re.search(pattern, content):
            new_content = re.sub(pattern, replacement, content)
            pattern_found = True
            break

    # Check if any pattern was found
    if not pattern_found:
        print(f"⚠️  Trail {trail_num}: No time estimate pattern found in {trail_file.name}")
        return False

    # Write the updated content back
    with open(trail_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✓ Trail {trail_num}: Updated {trail_file.name}")
    return True

def main():
    """Update all trail files."""
    print("Updating all trail chapter Key Characteristics tables...\n")

    updated_count = 0
    failed_count = 0

    for trail_num in range(1, 31):
        if trail_num in DRIVING_TIMES:
            driving_time = DRIVING_TIMES[trail_num]
            if update_trail_file(trail_num, driving_time):
                updated_count += 1
            else:
                failed_count += 1
        else:
            print(f"⚠️  Trail {trail_num}: No driving time defined")
            failed_count += 1

    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  ✓ Successfully updated: {updated_count} files")
    print(f"  ⚠️  Failed or skipped: {failed_count} files")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
