#!/usr/bin/env python3
"""
Update all trail chapter files to change "Distance from Knoxville"
to "Time from Knoxville" in the Key Characteristics tables.
"""

from pathlib import Path

def update_trail_file(trail_num: int) -> bool:
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

    # Simple string replacement
    if "Distance from Knoxville" not in content:
        print(f"⚠️  Trail {trail_num}: 'Distance from Knoxville' not found in {trail_file.name}")
        return False

    new_content = content.replace("Distance from Knoxville", "Time from Knoxville")

    # Write the updated content back
    with open(trail_file, 'w', encoding='utf-8') as f:
        f.write(new_content)

    print(f"✓ Trail {trail_num}: Updated {trail_file.name}")
    return True

def main():
    """Update all trail files."""
    print("Updating all trail chapters: 'Distance from Knoxville' → 'Time from Knoxville'\n")

    updated_count = 0
    failed_count = 0

    for trail_num in range(1, 31):
        if update_trail_file(trail_num):
            updated_count += 1
        else:
            failed_count += 1

    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  ✓ Successfully updated: {updated_count} files")
    print(f"  ⚠️  Failed or skipped: {failed_count} files")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
