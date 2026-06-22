"""Take the archived docx and produce a slim reference.docx for pandoc:
keep all style definitions, drop the body content (and embedded media).
"""
import sys
import zipfile
import shutil
import re
import os
from pathlib import Path

src = sys.argv[1]
dst = sys.argv[2]

work = Path(dst).with_suffix('.work')
if work.exists():
    shutil.rmtree(work)
work.mkdir(parents=True)

with zipfile.ZipFile(src) as z:
    z.extractall(work)

# Replace document.xml body with empty content (keep section properties).
doc_path = work / 'word' / 'document.xml'
xml = doc_path.read_text(encoding='utf-8')
# Find sectPr (page size/margins) to keep
sect_match = re.search(r'<w:sectPr[\s\S]*?</w:sectPr>', xml)
sect = sect_match.group(0) if sect_match else ''
# Locate body
body_open = xml.index('<w:body>')
body_close = xml.index('</w:body>') + len('</w:body>')
new_body = f'<w:body><w:p><w:r><w:t></w:t></w:r></w:p>{sect}</w:body>'
xml = xml[:body_open] + new_body + xml[body_close:]
doc_path.write_text(xml, encoding='utf-8')

# Drop embedded media to slim the file.
media_dir = work / 'word' / 'media'
if media_dir.exists():
    shutil.rmtree(media_dir)
# Drop drawings/charts/embeddings if present.
for sub in ('charts', 'embeddings', 'theme'):
    d = work / 'word' / sub
    if d.exists():
        shutil.rmtree(d)

# Clean rels to media we just deleted, to avoid pandoc/Word inheriting
# orphan image references.
rels_path = work / 'word' / '_rels' / 'document.xml.rels'
if rels_path.exists():
    rxml = rels_path.read_text(encoding='utf-8')
    # Match a full <Relationship .../> tag, then drop it if it targets
    # media/charts/embeddings. Done non-greedy so we don't span multiple tags.
    def _drop(m):
        tag = m.group(0)
        if re.search(r'Target="(media|charts|embeddings)/', tag):
            return ''
        return tag
    rxml = re.sub(r'<Relationship\b[^>]*/>', _drop, rxml)
    rels_path.write_text(rxml, encoding='utf-8')

# Normalize old GB2312 font names to modern Windows-installed names
# (仿宋_GB2312 → 仿宋, 楷体_GB2312 → 楷体), so the doc renders correctly
# on any standard Windows install. The archived doc declared the old names,
# which fall back to a weird default if the GB2312 variant is not installed.
styles_path = work / 'word' / 'styles.xml'
if styles_path.exists():
    sxml = styles_path.read_text(encoding='utf-8')
    sxml = sxml.replace('仿宋_GB2312', '仿宋').replace('楷体_GB2312', '楷体')
    styles_path.write_text(sxml, encoding='utf-8')
fontTable_path = work / 'word' / 'fontTable.xml'
if fontTable_path.exists():
    fxml = fontTable_path.read_text(encoding='utf-8')
    fxml = fxml.replace('仿宋_GB2312', '仿宋').replace('楷体_GB2312', '楷体')
    fontTable_path.write_text(fxml, encoding='utf-8')

# Re-zip.
out = Path(dst)
if out.exists():
    out.unlink()
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for f in work.rglob('*'):
        if f.is_file():
            z.write(f, f.relative_to(work).as_posix())
shutil.rmtree(work)
print(f'Slim reference saved: {dst} ({os.path.getsize(dst)} bytes)')
