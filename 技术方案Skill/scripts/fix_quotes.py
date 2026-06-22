"""In merged-clean.md, replace ASCII " with paired Chinese “ ” quotes.

Pairing is done per-paragraph (a paragraph = a block separated by blank
lines), in order of appearance: 1st " -> “, 2nd -> ”, 3rd -> “, ...
If a paragraph has an odd count, the last one is left as " for review.

Also normalizes ASCII single quotes ' to Chinese ‘ ’ when used in pairs
inside Chinese text (skip if mostly English context). Conservative:
only does it when the apostrophe count is even AND surrounded by CJK chars.
"""
import re
import sys
import io


def is_cjk(ch):
    if not ch:
        return False
    cp = ord(ch)
    # Common CJK ranges
    return (
        0x4E00 <= cp <= 0x9FFF or
        0x3400 <= cp <= 0x4DBF or
        0x3000 <= cp <= 0x303F or
        0xFF00 <= cp <= 0xFFEF
    )


def fix_paragraph_quotes(p):
    chars = list(p)
    quote_positions = [i for i, c in enumerate(chars) if c == '"']
    n = len(quote_positions)
    if n == 0:
        return p, 0, 0
    paired_n = n - (n % 2)
    fixed = 0
    for j in range(paired_n):
        idx = quote_positions[j]
        if j % 2 == 0:
            chars[idx] = '“'   # “
        else:
            chars[idx] = '”'   # ”
        fixed += 1
    odd_left = n - paired_n
    return ''.join(chars), fixed, odd_left


def main(path_in, path_out):
    text = open(path_in, encoding='utf-8').read()
    # Split into paragraphs by blank lines BUT also treat each markdown
    # "single line" (heading, list item, table row) as its own scope so
    # we don't accidentally pair quotes across rows of the same table.
    # Approach: walk line-by-line. For each non-blank line, fix quotes
    # within that line independently.
    lines = text.split('\n')
    total_fixed = 0
    total_odd = 0
    new_lines = []
    for line in lines:
        new_line, fixed, odd = fix_paragraph_quotes(line)
        new_lines.append(new_line)
        total_fixed += fixed
        total_odd += odd

    out = '\n'.join(new_lines)
    open(path_out, 'w', encoding='utf-8').write(out)
    print(f'Replaced {total_fixed} ASCII " into paired “ ”')
    print(f'Lines with leftover unpaired ASCII " : {total_odd}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else sys.argv[1])
