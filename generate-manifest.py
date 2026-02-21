#!/usr/bin/env python3
"""
Generate PUBLISHER-MANIFEST.md from _quarto.yml configuration.
This ensures the manifest stays in sync with the book structure.
"""

import yaml
import os
from pathlib import Path

def generate_manifest():
    # Read _quarto.yml
    with open('_quarto.yml', 'r') as f:
        config = yaml.safe_load(f)

    book = config['book']
    title = book['title']
    subtitle = book.get('subtitle', '')
    author = book['author']
    date = book['date']

    # Start building the manifest
    lines = [
        "# Book Manifest: Little Kids, Big Adventures",
        "",
        f"**Title:** {title}",
        f"**Subtitle:** {subtitle}",
        f"**Authors:** {author}",
        f"**Publication Date:** {date}",
        "**Publisher:** UT Press",
        "",
        "---",
        ""
    ]

    chapter_num = 1
    total_trails = 0
    section_intros = 0
    front_matter_count = 0
    back_matter_count = 0
    intro_content_count = 0

    # Process chapters
    for part in book['chapters']:
        if isinstance(part, dict) and 'part' in part:
            part_name = part['part']

            # Determine if this is a file-based section intro or text part name
            if part_name.endswith('.qmd'):
                # This is a geographic section with its own file
                section_file = part_name
                section_name = section_file.replace('Sec - ', '').replace('.qmd', '').replace('_', ' ').upper()
                lines.append(f"## PART: {section_name}")
                lines.append("")
                lines.append(f"{chapter_num}. **Section Introduction** (`{section_file}`)")
                chapter_num += 1
                section_intros += 1
                lines.append("")
            else:
                # This is a text-based part divider
                part_upper = part_name.upper()
                lines.append(f"## {part_upper}")
                lines.append("")

                # Track section types for summary
                if 'front' in part_name.lower():
                    current_section = 'front'
                elif 'end' in part_name.lower():
                    current_section = 'end'
                elif any(word in part_name.lower() for word in ['getting ready', 'how to use']):
                    current_section = 'intro'
                else:
                    current_section = 'other'

            # Process chapters within this part
            for chapter in part['chapters']:
                if chapter == 'index.qmd':
                    lines.append(f"~~{chapter_num}. Index (`{chapter}`) - REMOVED FOR PUBLISHER~~")
                    lines.append("")
                    continue

                # Get chapter title from filename
                filename = os.path.basename(chapter)
                title_part = filename.replace('.qmd', '')

                # Clean up special prefixes
                if filename.startswith('Trail_'):
                    # Pattern: Trail_N__Name.qmd
                    parts = title_part.split('__')
                    if len(parts) == 2:
                        trail_num = parts[0].replace('Trail_', '')
                        trail_name = parts[1].replace('_', ' ')
                        display_title = f"Trail {trail_num}: {trail_name}"
                    else:
                        display_title = title_part.replace('_', ' ')
                    total_trails += 1
                elif title_part.startswith('AAA -'):
                    clean_title = title_part.replace('AAA - ', '').replace('_', ' ').replace('  ', ' ')
                    display_title = clean_title
                    intro_content_count += 1
                elif title_part.startswith('ZZZ -'):
                    clean_title = title_part.replace('ZZZ - ', '').replace('_', ' ').replace('__', ' ').replace('  ', ' ')
                    display_title = clean_title
                    back_matter_count += 1
                elif title_part.startswith('zzz-') or title_part.startswith('zzz -'):
                    clean_title = title_part.replace('zzz-', '').replace('zzz - ', '').replace('_', ' ').replace('  ', ' ').title()
                    display_title = clean_title
                    if 'front' in locals() and current_section == 'front':
                        front_matter_count += 1
                    else:
                        back_matter_count += 1
                elif title_part.startswith('Sec -'):
                    display_title = f"**Section Introduction: {title_part.replace('Sec - ', '').replace('_', ' ')}**"
                    section_intros += 1
                else:
                    display_title = title_part.replace('_', ' ').replace('-', ' ').replace('  ', ' ').title()

                lines.append(f"{chapter_num}. {display_title} (`{filename}`)")
                chapter_num += 1

            lines.append("")

    # Add summary
    total_chapters = chapter_num - 1
    lines.extend([
        "---",
        "",
        "## Summary",
        "",
        f"- **Total Chapters:** {total_chapters}",
        f"- **Trail Descriptions:** {total_trails} trails across 3 geographic regions",
        f"- **Section Introductions:** {section_intros} regional overviews",
        "",
        "## Notes for Publisher",
        "",
        "- The three geographic section introductions include regional maps and contextual information",
        "- Each of the 30 trail chapters follows a consistent template with maps, GPS coordinates, and trail descriptions",
        "- All chapters will be delivered as individual DOCX files numbered sequentially (see `docx_chapters/` directory)",
        "- Images will be delivered separately in `publisher_images/` directory with placement marked in text as `<!-- IMAGE: filename.jpg -->`",
        ""
    ])

    # Write manifest
    with open('PUBLISHER-MANIFEST.md', 'w') as f:
        f.write('\n'.join(lines))

    print(f"✓ Generated PUBLISHER-MANIFEST.md with {total_chapters} chapters")
    print(f"  - {total_trails} trail descriptions")
    print(f"  - {section_intros} section introductions")

if __name__ == '__main__':
    generate_manifest()
