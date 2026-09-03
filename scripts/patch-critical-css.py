from pathlib import Path
import re

SAVED = '/Users/a1-6/Downloads/熵尾音 咬青 _ UTAU Voicebank.html'
CUR = '/Users/a1-6/Documents/DeepSeek工作区/网页开发/kuro-voicebank-restore/index.html'

saved_html = Path(SAVED).read_text()
cur_html = Path(CUR).read_text()

START_TAG = '<style id="critical-css">'

i = saved_html.index(START_TAG)
# Use depth counter to find the matching close
depth = 0
j = i
while j < len(saved_html):
    c = saved_html[j]
    if c == '<':
        # look ahead for </style> opening
        if saved_html[j:j+8] == '</style>':
            depth -= 1
            if depth == 0:
                break
            j += 8
            continue
        if saved_html[j:j+6] == '<style':
            depth += 1
            j += 6
            continue
    j += 1

saved_block = saved_html[i:j+len('</style>')]
print('saved block len:', len(saved_block))

# Find and replace the same range in current
i2 = cur_html.index(START_TAG)
depth = 0
j2 = i2
while j2 < len(cur_html):
    c = cur_html[j2]
    if c == '<':
        if cur_html[j2:j2+8] == '</style>':
            depth -= 1
            if depth == 0:
                break
            j2 += 8
            continue
        if cur_html[j2:j2+6] == '<style':
            depth += 1
            j2 += 6
            continue
    j2 += 1
cur_end = j2 + len('</style>')

new_html = cur_html[:i2] + saved_block + cur_html[cur_end:]
Path(CUR).write_text(new_html)
print('patched. new size:', len(new_html))

# Verify
m = re.search(r'<style id="critical-css">.*?</style>', new_html, re.S)
print('cur critical CSS now len:', len(m.group(0)))
print('byte-identical to saved:', m.group(0) == saved_block)