#!/usr/bin/env python3
"""
Compare callouts in the master CSV vs. what's currently in the book.
Identifies matches, mismatches, and where callouts need to be moved/added/removed.
"""

import csv
import re
import glob
from collections import defaultdict
from difflib import SequenceMatcher

# Mapping of chapter names in CSV to trail numbers
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
    'Alum Caves': 30,  # Alternative spelling
}

def similarity(a, b):
    """Calculate similarity ratio between two strings."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def extract_title_from_callout(callout_text):
    """Extract the title from callout text (#### Title)."""
    match = re.search(r'^#{2,4}\s+(.+?)$', callout_text, re.MULTILINE)
    return match.group(1).strip() if match else "[No title]"

def parse_trail_number(filename):
    """Extract trail number from filename."""
    match = re.search(r'Trail_(\d+)__', filename)
    return int(match.group(1)) if match else None

def get_trail_name(filename):
    """Extract trail name from filename."""
    match = re.search(r'Trail_\d+__(.+)\.qmd', filename)
    return match.group(1).replace('_', ' ') if match else filename

def load_master_csv(csv_path):
    """Load the master callouts CSV."""
    callouts = defaultdict(list)

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            chapter = row['Chapter'].strip()
            title = row['Title'].strip()
            text = row['Text'].strip()
            notes = row['Notes'].strip()

            trail_num = CHAPTER_TO_TRAIL.get(chapter)
            if trail_num is None:
                print(f"WARNING: Unknown chapter '{chapter}' in CSV")
                continue

            callouts[trail_num].append({
                'title': title,
                'text': text,
                'notes': notes,
                'chapter': chapter
            })

    return callouts

def extract_book_callouts(text, trail_num, trail_name):
    """Extract callouts from a book chapter."""
    callout_pattern = re.compile(
        r':::\s*\{\.callout[^\}]*\}\s*(.*?)^:::\s*$',
        re.MULTILINE | re.DOTALL
    )

    matches = callout_pattern.findall(text)
    callouts = []

    for match in matches:
        title = extract_title_from_callout(match)
        callouts.append({
            'title': title,
            'text': match.strip(),
            'trail_num': trail_num,
            'trail_name': trail_name
        })

    return callouts

def main():
    print("=" * 100)
    print("CALLOUT COMPARISON: MASTER CSV vs. CURRENT BOOK")
    print("=" * 100)
    print()

    # Load master CSV
    master_callouts = load_master_csv('callouts-master.csv')

    # Load current book callouts
    book_callouts = defaultdict(list)
    trail_files = sorted(glob.glob('Trail_*.qmd'))

    for trail_file in trail_files:
        trail_num = parse_trail_number(trail_file)
        if trail_num is None:
            continue

        trail_name = get_trail_name(trail_file)

        with open(trail_file, 'r', encoding='utf-8') as f:
            text = f.read()

        callouts = extract_book_callouts(text, trail_num, trail_name)
        book_callouts[trail_num] = callouts

    # Analysis structures
    perfect_matches = []
    content_differences = []
    wrong_trail = []
    in_csv_not_book = []
    in_book_not_csv = []

    # Compare master CSV to book
    for trail_num in sorted(set(list(master_callouts.keys()) + list(book_callouts.keys()))):
        csv_calls = master_callouts.get(trail_num, [])
        book_calls = book_callouts.get(trail_num, [])

        # Check each CSV callout
        for csv_call in csv_calls:
            found = False

            # First check if it's in the correct trail in the book
            for book_call in book_calls:
                title_match = similarity(csv_call['title'], book_call['title']) > 0.85

                if title_match:
                    found = True
                    # Check if content matches
                    content_sim = similarity(csv_call['text'], book_call['text'])

                    if content_sim > 0.95:
                        perfect_matches.append({
                            'trail': trail_num,
                            'title': csv_call['title'],
                            'chapter': csv_call['chapter']
                        })
                    else:
                        content_differences.append({
                            'trail': trail_num,
                            'title': csv_call['title'],
                            'chapter': csv_call['chapter'],
                            'similarity': content_sim,
                            'csv_text': csv_call['text'][:100] + "...",
                            'book_text': book_call['text'][:100] + "..."
                        })
                    break

            if not found:
                # Check if it's in a different trail
                found_elsewhere = False
                for other_trail, other_calls in book_callouts.items():
                    if other_trail == trail_num:
                        continue

                    for book_call in other_calls:
                        if similarity(csv_call['title'], book_call['title']) > 0.85:
                            wrong_trail.append({
                                'title': csv_call['title'],
                                'csv_trail': trail_num,
                                'csv_chapter': csv_call['chapter'],
                                'book_trail': other_trail,
                                'book_trail_name': book_call['trail_name']
                            })
                            found_elsewhere = True
                            break

                    if found_elsewhere:
                        break

                if not found_elsewhere:
                    in_csv_not_book.append({
                        'trail': trail_num,
                        'title': csv_call['title'],
                        'chapter': csv_call['chapter'],
                        'notes': csv_call['notes']
                    })

        # Check for callouts in book but not in CSV
        for book_call in book_calls:
            found = False

            for csv_call in csv_calls:
                if similarity(csv_call['title'], book_call['title']) > 0.85:
                    found = True
                    break

            if not found:
                # Check if it's in CSV but assigned to different trail
                found_elsewhere = False
                for other_trail, other_csv_calls in master_callouts.items():
                    if other_trail == trail_num:
                        continue

                    for csv_call in other_csv_calls:
                        if similarity(csv_call['title'], book_call['title']) > 0.85:
                            found_elsewhere = True
                            break

                    if found_elsewhere:
                        break

                if not found_elsewhere:
                    in_book_not_csv.append({
                        'trail': trail_num,
                        'trail_name': book_call['trail_name'],
                        'title': book_call['title']
                    })

    # Print results
    print(f"✓ PERFECT MATCHES ({len(perfect_matches)}):")
    print("-" * 100)
    for match in perfect_matches:
        print(f"  Trail {match['trail']:2d} ({match['chapter']}): {match['title']}")

    print()
    print(f"⚠ CONTENT DIFFERENCES ({len(content_differences)}):")
    print("-" * 100)
    for diff in content_differences:
        print(f"  Trail {diff['trail']:2d} ({diff['chapter']}): {diff['title']}")
        print(f"    Similarity: {diff['similarity']:.1%}")
        print(f"    CSV: {diff['csv_text']}")
        print(f"    Book: {diff['book_text']}")
        print()

    print(f"↔ WRONG TRAIL ({len(wrong_trail)}) - Callout exists but in different trail:")
    print("-" * 100)
    for item in wrong_trail:
        print(f"  {item['title']}")
        print(f"    CSV says: Trail {item['csv_trail']:2d} ({item['csv_chapter']})")
        print(f"    Book has: Trail {item['book_trail']:2d} ({item['book_trail_name']})")
        print()

    print(f"+ IN CSV, NOT IN BOOK ({len(in_csv_not_book)}) - Need to add:")
    print("-" * 100)
    for item in in_csv_not_book:
        print(f"  Trail {item['trail']:2d} ({item['chapter']}): {item['title']} [{item['notes']}]")

    print()
    print(f"- IN BOOK, NOT IN CSV ({len(in_book_not_csv)}) - Need to remove or add to CSV:")
    print("-" * 100)
    for item in in_book_not_csv:
        print(f"  Trail {item['trail']:2d} ({item['trail_name']}): {item['title']}")

    print()
    print("=" * 100)
    print("SUMMARY:")
    print("-" * 100)
    print(f"  Perfect matches:     {len(perfect_matches)}")
    print(f"  Content differences: {len(content_differences)}")
    print(f"  Wrong trail:         {len(wrong_trail)}")
    print(f"  In CSV, not book:    {len(in_csv_not_book)}")
    print(f"  In book, not CSV:    {len(in_book_not_csv)}")
    print("=" * 100)

    # Save detailed report
    with open('callout-comparison-report.txt', 'w', encoding='utf-8') as f:
        f.write("CALLOUT COMPARISON REPORT\n")
        f.write("=" * 100 + "\n\n")

        f.write(f"Perfect matches: {len(perfect_matches)}\n")
        f.write(f"Content differences: {len(content_differences)}\n")
        f.write(f"Wrong trail: {len(wrong_trail)}\n")
        f.write(f"In CSV, not book: {len(in_csv_not_book)}\n")
        f.write(f"In book, not CSV: {len(in_book_not_csv)}\n")
        f.write("\nSee terminal output for details.\n")

    print("\nDetailed report saved to: callout-comparison-report.txt")

if __name__ == '__main__':
    main()
