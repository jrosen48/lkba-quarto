import re

def combine_longtables_single_layout(input_tex, output_tex):
    with open(input_tex, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Regex to find each \begin{longtable}...\end{longtable} block.
    pattern = re.compile(
        r'\\begin{longtable}(\[[^\]]*\])?\{([^}]*)\}(.*?)\\end{longtable}',
        flags=re.DOTALL
    )
    
    all_blocks = pattern.findall(content)
    # all_blocks is a list of tuples: [(maybe_bracket, col_spec, table_body), ...]

    merged_rows = []  # We'll store the "cleaned" lines from every table block.

    for (maybe_bracket, col_spec, table_body) in all_blocks:
        # Remove repeated headings, footers, or lines you don't need:
        # e.g. \toprule, \bottomrule, \endhead, \endlastfoot, etc.
        # This is optional—if you want to keep some of those, remove from here.
        table_body = re.sub(r'\\toprule\s*\\noalign\{\}', '', table_body)
        table_body = re.sub(r'\\bottomrule\s*\\noalign\{\}', '', table_body)
        table_body = re.sub(r'\\midrule\s*\\noalign\{\}', '', table_body)
        table_body = re.sub(r'\\endhead', '', table_body)
        table_body = re.sub(r'\\endlastfoot', '', table_body)
        
        # Remove minipage wrappers
        table_body = re.sub(r'\\begin\{minipage\}\[b\]\{[^\}]*\}', '', table_body)
        table_body = re.sub(r'\\end\{minipage\}', '', table_body)

        # We will now filter out lines that look like leftover column definitions or blank lines.
        cleaned_lines = []
        for line in table_body.split('\n'):
            line = line.strip()
            
            # 1) Skip if empty
            if not line:
                continue
            
            # 2) Skip if it looks like a column definition line
            #    e.g. something starting with >{\raggedright\arraybackslash}p{...}, or ll@{} etc.
            if re.match(r'^>?\{\raggedright\\arraybackslash\}p\([^}]*\}', line):
                # e.g.  >{\raggedright\arraybackslash}p{(\linewidth - 2\tabcolsep) * \real{0.5745}}
                continue
            if re.match(r'^[lcr]+\@?\{\}?\}?$', line):
                # e.g.  ll@{}}
                continue
            
            # 3) Sometimes the leftover line might be partial, e.g.  @{}}
            #    We'll skip lines that are basically just braces or leftover at-clauses.
            if re.match(r'^[\@\}\{]+$', line):
                continue
            
            # 4) If you want to remove explicit \raggedright lines or leftover commands that appear alone:
            if line == r'\raggedright':
                continue
            
            # If the line passed all filters, keep it
            cleaned_lines.append(line)
        
        # Merge the lines back into one chunk
        if cleaned_lines:
            merged_rows.append("\n".join(cleaned_lines))
    
    # Decide on ONE final column spec for everything:
    # For instance, 2 columns each 50% wide:
    final_column_spec = r"@{}p{0.5\linewidth}p{0.5\linewidth}@{}"
    
    # Or if you prefer something else, e.g. 30%/70%:
    # final_column_spec = r"@{}p{0.3\linewidth}p{0.7\linewidth}@{}"

    with open(output_tex, "w", encoding="utf-8") as out:
        out.write(r"\begin{longtable}{" + final_column_spec + "}\n")
        
        # Write each block of lines
        for i, block in enumerate(merged_rows):
            out.write(block + "\n\n")
            # If you want a horizontal rule or empty line between blocks, add it:
            # out.write(r"\midrule" + "\n\n")
        
        out.write(r"\end{longtable}" + "\n")

    print(f"Combined {len(all_blocks)} tables into one with column spec '{final_column_spec}'. Written to {output_tex}.")


if __name__ == "__main__":
    input_file = "Little-Kids,-Big-Adventures--A-Guide-to-Family-Hikes-Around-Knoxville.tex"
    output_file = "combined_longtables_single.tex"
    combine_longtables_single_layout(input_file, output_file)
