import os
import re

folder = "."
chapter_re = re.compile(r"^#\s+(.*)")
callout_start_re = re.compile(r"^::: \{\.callout-[^\}]+\}")
callout_header_re = re.compile(r"^####\s+(.*)")

results = []

# List all .qmd files in the current folder
files = [f for f in os.listdir(folder) if f.endswith(".qmd")]
print("Found", len(files), "files.")

for filename in files:
    filepath = os.path.join(folder, filename)
    print("Processing file:", filename)
    chapter_title = None
    inside_callout = False
    callout_title = None

    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            # Look for chapter header if not yet set
            if chapter_title is None:
                m = chapter_re.match(line)
                if m:
                    chapter_title = m.group(1).strip()

            # Identify the start of a callout block
            if not inside_callout and callout_start_re.match(line):
                inside_callout = True
                callout_title = None
                continue

            if inside_callout:
                # End of the callout block
                if line.startswith(":::"):
                    inside_callout = False
                    if callout_title:
                        results.append({"chapter": chapter_title or filename, "callout": callout_title})
                    continue

                # Capture the callout header (first header line within the callout)
                if callout_title is None:
                    m = callout_header_re.match(line)
                    if m:
                        callout_title = m.group(1).strip()

    # Fallback: if no chapter header was found, use the filename
    if chapter_title is None:
        chapter_title = filename

# Output results as a Markdown table
print("\n| Chapter | Callout Title |")
print("|---------|---------------|")
for entry in results:
    print(f"| {entry['chapter']} | {entry['callout']} |")
