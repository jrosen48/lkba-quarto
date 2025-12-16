#!/usr/bin/env python3
"""
Script to handle the trail renumbering:
1. Delete Trail 23 (Whiteoak Sink)
2. Add new Trail 13 (Aspire Park) at end of Knoxville section
3. Renumber all trails 13-22 to become 14-23
4. Update internal chapter titles (## Trail X:)
5. Update map references (maps/trail-XX-map.jpeg)
"""

import os
import re
from pathlib import Path
import shutil

def update_trail_number_in_file(filepath, old_num, new_num):
    """Update trail number references within a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update chapter heading (## Trail X:)
    content = re.sub(
        rf'^## Trail {old_num}:',
        f'## Trail {new_num}:',
        content,
        flags=re.MULTILINE
    )

    # Update map reference (maps/trail-XX-map.jpeg)
    old_map = f'trail-{old_num:02d}-map.jpeg'
    new_map = f'trail-{new_num:02d}-map.jpeg'
    content = content.replace(old_map, new_map)

    # Update figure references (trail-XX-figure-XX.jpg)
    old_prefix = f'trail-{old_num:02d}-figure-'
    new_prefix = f'trail-{new_num:02d}-figure-'
    content = content.replace(old_prefix, new_prefix)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    print("=" * 70)
    print("TRAIL RENUMBERING SCRIPT")
    print("=" * 70)
    print("\nChanges to make:")
    print("  1. DELETE Trail 23 (Whiteoak Sink)")
    print("  2. ADD Trail 13 (Aspire Park) - placeholder")
    print("  3. RENUMBER Trails 13-22 → Trails 14-23")
    print("  4. UPDATE internal trail numbers in files")
    print("  5. RENAME map files accordingly")
    print("\n" + "=" * 70)

    # Step 1: Delete Trail 23 (Whiteoak Sink)
    print("\nSTEP 1: Deleting Trail 23 (Whiteoak Sink)")
    print("-" * 70)
    whiteoak_file = Path('Trail_23__Whiteoak_Sink.qmd')
    if whiteoak_file.exists():
        whiteoak_file.unlink()
        print(f"  ✓ Deleted {whiteoak_file}")
    else:
        print(f"  ⚠ File not found: {whiteoak_file}")

    # Delete corresponding map
    whiteoak_map = Path('maps/trail-23-map.jpeg')
    if whiteoak_map.exists():
        whiteoak_map.unlink()
        print(f"  ✓ Deleted {whiteoak_map}")

    # Step 2: Renumber trails in reverse order (to avoid conflicts)
    print("\nSTEP 2: Renumbering trail files (working backwards)")
    print("-" * 70)

    # Map: old_num -> new_num for trails that need renumbering
    renumber_map = {
        22: 23,  # Mouse Creek
        21: 22,  # Little River
        20: 21,  # Spruce Flats Falls
        19: 20,  # Honey Creek
        18: 19,  # Angel Falls
        17: 18,  # Twin Arches
        16: 17,  # Fall Branch Falls
        15: 16,  # Bandy Creek
        14: 15,  # Obed Point
        13: 14,  # Emory Falls
    }

    # Process in reverse order to avoid conflicts
    for old_num in sorted(renumber_map.keys(), reverse=True):
        new_num = renumber_map[old_num]

        # Find the file with old trail number
        old_pattern = f'Trail_{old_num}__*.qmd'
        matches = list(Path('.').glob(old_pattern))

        if not matches:
            print(f"  ⚠ No file found for Trail {old_num}")
            continue

        old_file = matches[0]
        # Create new filename with updated trail number
        new_filename = old_file.name.replace(f'Trail_{old_num}__', f'Trail_{new_num}__')
        new_file = Path(new_filename)

        # Update content first
        print(f"  Updating Trail {old_num} → Trail {new_num}")
        update_trail_number_in_file(old_file, old_num, new_num)

        # Rename file
        old_file.rename(new_file)
        print(f"    ✓ Renamed: {old_file.name} → {new_file.name}")

        # Rename corresponding map file
        old_map = Path(f'maps/trail-{old_num:02d}-map.jpeg')
        new_map = Path(f'maps/trail-{new_num:02d}-map.jpeg')
        if old_map.exists():
            old_map.rename(new_map)
            print(f"    ✓ Renamed map: {old_map.name} → {new_map.name}")

    # Step 3: Create placeholder for new Trail 13 (Aspire Park)
    print("\nSTEP 3: Creating placeholder for Trail 13 (Aspire Park)")
    print("-" * 70)

    aspire_content = """## Trail 13: Aspire Park

**Figures included in this chapter:**

- trail-13-map.jpeg

### Overview

[CONTENT NEEDED: Please add the Aspire Park trail description here]

<!-- IMAGE REMOVED FOR PUBLISHER: trail-13-map.jpeg -->

### Key Characteristics

| **Characteristic**        | **Details**              |
|---------------------------|--------------------------|
| Time Estimate             | [TBD]                    |
| Trail Distance (Miles)    | [TBD]                    |
| Elevation Change          | [TBD]                    |
| Pets                      | [TBD]                    |
| Parking Pass/Entrance Fee | [TBD]                    |
| Restroom(s)               | [TBD]                    |
| Best Ages                 | [TBD]                    |
| Strollers and Wheelchairs | [TBD]                    |

### Directions to the Trailhead

[CONTENT NEEDED: Add directions and GPS coordinates]

### Trail Description

[CONTENT NEEDED: Add mile-by-mile trail description]

### Nearby

[CONTENT NEEDED: Add nearby attractions or activities]
"""

    aspire_file = Path('Trail_13__Aspire_Park.qmd')
    with open(aspire_file, 'w', encoding='utf-8') as f:
        f.write(aspire_content)
    print(f"  ✓ Created {aspire_file}")
    print("  ⚠ This is a PLACEHOLDER - you need to add actual content!")

    print("\n" + "=" * 70)
    print("RENUMBERING COMPLETE!")
    print("=" * 70)
    print("\nNext steps:")
    print("  1. Add content to Trail_13__Aspire_Park.qmd")
    print("  2. Add trail-13-map.jpeg to maps/ folder")
    print("  3. Update _quarto.yml configuration")
    print("  4. Update create-chapters.sh script")
    print("  5. Regenerate publisher files")

if __name__ == '__main__':
    main()
