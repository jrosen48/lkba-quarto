import os
import re
import csv
import sys
import glob

def get_chapter_name(qmd_text, fallback_name):
    """
    Attempts to extract a chapter title from:
      1. YAML front matter 'title:'
      2. The first top-level heading '# Some Heading'
    Falls back to fallback_name if none found.
    """
    # 1) Try YAML front matter:
    #    ---
    #    title: Something
    #    ---
    yaml_title_pattern = re.compile(
        r'^---\s*\ntitle:\s*(.+?)\n.*?^---\s*$',
        re.DOTALL | re.MULTILINE
    )
    match = yaml_title_pattern.search(qmd_text)
    if match:
        return match.group(1).strip().strip('"').strip("'")

    # 2) If no YAML title, try the first top-level heading (# Something)
    heading_pattern = re.compile(r'^(#)\s+(.+)$', re.MULTILINE)
    match = heading_pattern.search(qmd_text)
    if match:
        return match.group(2).strip()

    # 3) Fallback
    return fallback_name

def get_callouts(qmd_text):
    """
    Returns a list of strings, each corresponding to the text inside
    a Quarto callout like:
        ::: {.callout-??? ...}
        (content)
        :::
    """
    # You can broaden this pattern if you use 4 colons or advanced attributes.
    callout_pattern = re.compile(
        r'^:::\s*\{\.callout[^\}]*\}\s*(.*?)^:::\s*$',
        re.MULTILINE | re.DOTALL
    )
    matches = callout_pattern.findall(qmd_text)
    return [m.strip() for m in matches]

def parse_trail_number(qmd_filename):
    """
    If the filename contains something like 'Trail_29_foo.qmd',
    return 29 (as int). Otherwise, return 0 (or another fallback).
    """
    # We look for 'Trail_<digits>' at the start OR anywhere:
    # e.g. "Trail_10_Something.qmd".
    match = re.search(r'\bTrail_(\d+)\b', qmd_filename, re.IGNORECASE)
    if match:
        return int(match.group(1))
    else:
        return 0  # fallback for non-trail files

def main(qmd_directory, output_csv):
    """
    1. Finds all .qmd in qmd_directory (not recursive by default).
    2. For each .qmd:
       - Parse a 'trail number' from the filename
       - Extract a 'chapter name' from YAML or # heading
       - Extract all callouts
    3. Collect them, sort by 'trail number', and write CSV (ChapterName, Callout).
    """
    qmd_files = glob.glob(os.path.join(qmd_directory, '*.qmd'))

    results = []  # will hold tuples: (trail_num, chapter_name, callout_text)

    for qmd_path in qmd_files:
        # e.g. "Trail_29_Example.qmd" or "Intro.qmd"
        basename = os.path.basename(qmd_path)
        trail_num = parse_trail_number(basename)

        with open(qmd_path, 'r', encoding='utf-8') as f:
            text = f.read()

        # Derive chapter name from the file contents or fallback to basename
        fallback_name = os.path.splitext(basename)[0]  # "Trail_29_Example"
        chapter_name = get_chapter_name(text, fallback_name)

        # Extract the callouts from the QMD
        callouts = get_callouts(text)

        # Add them to our collection
        for c in callouts:
            results.append((trail_num, chapter_name, c))

    # Sort all callouts by the numeric 'trail_num' ascending
    results.sort(key=lambda row: row[0])  # (trail_num, chapter_name, callout)

    # Write CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["ChapterName", "Callout"])  # CSV header
        for (trail_num, chap_name, callout_text) in results:
            writer.writerow([chap_name, callout_text])

    print(f"Found {len(results)} total callouts across {len(qmd_files)} .qmd files.")
    print(f"Sorted by 'trail_num' and wrote output to {output_csv}.")

if __name__ == "__main__":
    # Usage: python script.py [qmd_directory] [output.csv]
    if len(sys.argv) < 3:
        print("Usage: python script.py <qmd_directory> <output.csv>")
        sys.exit(1)

    qmd_dir = sys.argv[1]
    out_csv = sys.argv[2]

    main(qmd_dir, out_csv)
