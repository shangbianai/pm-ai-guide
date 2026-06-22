"""Insert a cover page at the very front of a docx — BEFORE the TOC.

Why a script: pandoc's `--toc` puts the table of contents at the absolute top
of the document (wrapped in a w:sdt). There's no clean way to make pandoc emit
a cover *before* that. So we post-process: build cover paragraphs and insert
them ahead of the first body element (the TOC sdt), then a page break. Result
order: 封面 → 目录 → 正文.

Usage:
    python add_cover.py in.docx out.docx "主标题" "副行1" "副行2" ...

- 主标题: 微软雅黑 28pt 加粗 居中（微软雅黑全平台都有，避免方正小标宋简体缺字时
  回退成行书等怪异字体；字号比正文标题大一档，封面更醒目）
- 副行 (承担单位 / 日期 等): 仿宋_GB2312 16pt(三号) 居中
"""
import sys
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def _par(text, cn_font, size_pt, bold=False, align='center', space_before=0):
    p = OxmlElement('w:p')
    pPr = OxmlElement('w:pPr')
    jc = OxmlElement('w:jc'); jc.set(qn('w:val'), align); pPr.append(jc)
    if space_before:
        sp = OxmlElement('w:spacing'); sp.set(qn('w:before'), str(space_before)); pPr.append(sp)
    p.append(pPr)
    r = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    rf = OxmlElement('w:rFonts')
    rf.set(qn('w:ascii'), 'Times New Roman'); rf.set(qn('w:hAnsi'), 'Times New Roman')
    rf.set(qn('w:eastAsia'), cn_font); rf.set(qn('w:cs'), 'Times New Roman')
    rPr.append(rf)
    sz = OxmlElement('w:sz'); sz.set(qn('w:val'), str(int(size_pt * 2))); rPr.append(sz)
    if bold:
        rPr.append(OxmlElement('w:b'))
    r.append(rPr)
    t = OxmlElement('w:t'); t.set(qn('xml:space'), 'preserve'); t.text = text
    r.append(t); p.append(r)
    return p


def _page_break_par():
    p = OxmlElement('w:p')
    r = OxmlElement('w:r')
    br = OxmlElement('w:br'); br.set(qn('w:type'), 'page')
    r.append(br); p.append(r)
    return p


def main(path_in, path_out, title, sublines):
    doc = Document(path_in)
    body = doc.element.body
    first = body[0]  # the TOC sdt (or first content); cover goes before it

    elems = []
    # push the title down a bit from the top
    for _ in range(6):
        elems.append(_par('', '仿宋_GB2312', 16))
    elems.append(_par(title, '微软雅黑', 28, bold=True))
    elems.append(_par('', '仿宋_GB2312', 16))
    for line in sublines:
        elems.append(_par(line, '仿宋_GB2312', 16, space_before=120))
    elems.append(_page_break_par())

    for el in elems:           # insert in order, each right before `first`
        first.addprevious(el)

    # Page break AFTER the TOC so 正文 starts on a fresh page (otherwise 目录
    # 末尾和正文首段挤在同一页). `first` is pandoc's TOC sdt; only break when
    # it really is the TOC, else we'd split body content.
    if first.tag == qn('w:sdt'):
        first.addnext(_page_break_par())

    doc.save(path_out)
    print(f'Cover inserted before TOC. Saved {path_out}')


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('usage: python add_cover.py in.docx out.docx "标题" ["副行1" "副行2" ...]')
        sys.exit(1)
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:])
