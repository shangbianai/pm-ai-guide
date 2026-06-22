"""Rewrite H3 headings in merged-clean.md so they use the "X.Y.N" form.

The source has two H3 styles that need disambiguating:
  (a) "### 4.4.1 装车排号优化算法"   -- already numbered, true H3
  (b) "### 一、问题定义"            -- chinese-numeral H3

Within each H2 section:
  - If (a)-style H3s exist, the (b)-style ones are *sub-sections* of the
    nearest preceding (a). Demote them to H4 (####) and strip the prefix.
  - Otherwise (no (a)-style in this H2), (b)-style H3s become real H3s:
    strip the chinese prefix and prepend "X.Y.N ".

H1 (#) and H2 (##) are left alone.
H4 (####) and below are left alone (except for the auto-demotions above).
"""
import re
import sys

CHINESE_NUMS = ('一', '二', '三', '四', '五', '六', '七', '八', '九',
                '十一', '十二', '十三', '十四', '十五', '十六', '十七',
                '十八', '十九', '二十', '十')   # 十 last for non-greedy
prefix_re = re.compile(
    r'^(?:'
    r'(?:' + '|'.join(CHINESE_NUMS) + r')[、，.\s]+'
    r'|[（(](?:' + '|'.join(CHINESE_NUMS) + r')[）)][、，.\s]*'
    r')'
)
already_numbered_re = re.compile(r'^\d+(?:\.\d+){1,3}\s')

h1_re = re.compile(r'^#\s+(.*)$')
h2_re = re.compile(r'^##\s+([\d.]+)\s+(.*)$')
h3_re = re.compile(r'^###\s+(.*)$')


def split_into_h2_blocks(lines):
    """Yield (h2_number or None, list_of_lines_including_h2_header)."""
    block = []
    current = None
    for line in lines:
        m = h2_re.match(line)
        if m:
            if block:
                yield current, block
            current = m.group(1)
            block = [line]
        else:
            block.append(line)
    if block:
        yield current, block


def process_block(h2_num, block_lines):
    """Renumber H3 within one H2 block. h2_num is e.g. "1.3" or None."""
    if h2_num is None:
        return block_lines  # nothing to do (e.g. before first H2)
    # Pre-scan: does this block contain any pre-numbered H3 like "X.Y.Z ..."?
    has_pre_numbered = any(
        h3_re.match(l) and already_numbered_re.match(h3_re.match(l).group(1))
        for l in block_lines
    )
    new_block = []
    h3_counter = 0
    for line in block_lines:
        m3 = h3_re.match(line)
        if not m3:
            new_block.append(line)
            continue
        title = m3.group(1).strip()
        if already_numbered_re.match(title):
            # Already "X.Y.Z foo" -- leave as-is (real H3).
            new_block.append(line)
            continue
        stripped = prefix_re.sub('', title)
        if has_pre_numbered:
            # Demote to H4
            new_block.append(f'#### {stripped}')
        else:
            h3_counter += 1
            new_block.append(f'### {h2_num}.{h3_counter} {stripped}')
    return new_block


def main(path_in, path_out):
    text = open(path_in, encoding='utf-8').read()
    lines = text.split('\n')
    out = []
    for h2_num, block in split_into_h2_blocks(lines):
        out.extend(process_block(h2_num, block))
    open(path_out, 'w', encoding='utf-8').write('\n'.join(out))
    print(f'Done. Wrote {path_out}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else sys.argv[1])
