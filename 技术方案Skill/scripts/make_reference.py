"""Build a pandoc reference.docx with the official styling required by TASK-GUIDE.md.

Style spec:
  Normal:      仿宋_GB2312 16pt (三号), 行距固定值 28pt, 首行缩进 2 字符
  Heading 1:   黑体     16pt 加粗
  Heading 2:   楷体     16pt 加粗
  Heading 3:   仿宋_GB2312 16pt 加粗
  Table cell:  宋体     10.5pt
  Caption:     宋体      9pt
  Page:        A4, 上下边距 2.54cm, 左右 3.18cm（默认）
"""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


def set_cn_font(run_or_style_font, ascii_font, cn_font, size_pt, bold=False):
    """Apply a font that combines an ASCII face and a Chinese (east-asia) face."""
    run_or_style_font.name = ascii_font
    run_or_style_font.size = Pt(size_pt)
    run_or_style_font.bold = bold
    # NOTE: Font.element is the <w:style>/<w:r> element, NOT its <w:rPr>.
    # We must descend into rPr; otherwise the rFonts we create is misplaced
    # (a direct child of <w:style>) and Word ignores eastAsia/cs — that was
    # the bug that wiped 标题/正文 的中文字体 from every style.
    rPr = run_or_style_font.element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.insert(0, rFonts)
    rFonts.set(qn('w:ascii'), ascii_font)
    rFonts.set(qn('w:hAnsi'), ascii_font)
    rFonts.set(qn('w:eastAsia'), cn_font)
    rFonts.set(qn('w:cs'), ascii_font)
    # Drop theme font refs so our explicit faces win over the template theme
    # (the default Heading styles carry eastAsiaTheme="majorEastAsia").
    for attr in ('w:asciiTheme', 'w:hAnsiTheme', 'w:eastAsiaTheme', 'w:cstheme'):
        if rFonts.get(qn(attr)) is not None:
            del rFonts.attrib[qn(attr)]


def set_paragraph_indent_and_spacing(pf, first_line_chars=2, line_pt=28,
                                     space_before=0, space_after=0):
    """Apply first-line-indent (in characters) and fixed line spacing."""
    pf.line_spacing = Pt(line_pt)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    # Same caveat as set_cn_font: descend into pPr, don't operate on <w:style>.
    pPr = pf.element.get_or_add_pPr()
    ind = pPr.find(qn('w:ind'))
    if ind is None:
        ind = OxmlElement('w:ind')
        pPr.append(ind)
    if first_line_chars:
        ind.set(qn('w:firstLineChars'), str(first_line_chars * 100))
        ind.set(qn('w:firstLine'), str(first_line_chars * 320))
    else:
        for attr in ('w:firstLineChars', 'w:firstLine'):
            if ind.get(qn(attr)) is not None:
                del ind.attrib[qn(attr)]


def main(out_path, margins='generic'):
    doc = Document()

    # --- Body styles -------------------------------------------------------
    # IMPORTANT: pandoc usually tags body paragraphs as 'Body Text' /
    # 'First Paragraph', NOT 'Normal'. If we only style 'Normal', body text
    # keeps pandoc's default font/size. So style Normal AND pandoc's body
    # styles (create them if the blank template lacks them). apply_postprocess
    # also enforces this on runs as a final safety net.
    for body_name in ('Normal', 'Body Text', 'First Paragraph', 'Compact', 'Body'):
        try:
            st = doc.styles[body_name]
        except KeyError:
            try:
                from docx.enum.style import WD_STYLE_TYPE
                st = doc.styles.add_style(body_name, WD_STYLE_TYPE.PARAGRAPH)
                if body_name != 'Normal':
                    st.base_style = doc.styles['Normal']
            except Exception:
                continue
        set_cn_font(st.font, 'Times New Roman', '仿宋_GB2312', 16)
        set_paragraph_indent_and_spacing(st.paragraph_format,
                                         first_line_chars=2, line_pt=28)

    # --- Heading styles ----------------------------------------------------
    h_specs = [
        ('Heading 1', 'Times New Roman', '黑体',         16, True),
        ('Heading 2', 'Times New Roman', '楷体_GB2312',  16, True),
        ('Heading 3', 'Times New Roman', '仿宋_GB2312',  16, True),
        ('Heading 4', 'Times New Roman', '仿宋_GB2312',  14, True),
        ('Heading 5', 'Times New Roman', '仿宋_GB2312',  12, True),
        ('Heading 6', 'Times New Roman', '仿宋_GB2312',  12, True),
    ]
    for name, ascii_f, cn_f, size, bold in h_specs:
        try:
            st = doc.styles[name]
        except KeyError:
            continue
        set_cn_font(st.font, ascii_f, cn_f, size, bold=bold)
        st.font.color.rgb = RGBColor(0, 0, 0)
        # Headings: no first-line indent, slightly looser line spacing.
        set_paragraph_indent_and_spacing(st.paragraph_format,
                                         first_line_chars=0,
                                         line_pt=size + 12,
                                         space_before=6, space_after=6)

    # --- Title (cover) -----------------------------------------------------
    try:
        title = doc.styles['Title']
        set_cn_font(title.font, 'Times New Roman', '方正小标宋简体', 22, bold=True)
        set_paragraph_indent_and_spacing(title.paragraph_format,
                                         first_line_chars=0,
                                         line_pt=34, space_before=12, space_after=12)
    except KeyError:
        pass

    # --- Captions ----------------------------------------------------------
    try:
        cap = doc.styles['Caption']
        set_cn_font(cap.font, 'Times New Roman', '宋体', 9)
        set_paragraph_indent_and_spacing(cap.paragraph_format,
                                         first_line_chars=0,
                                         line_pt=14, space_before=2, space_after=2)
    except KeyError:
        pass

    # --- Image holder paragraph style (pandoc puts images in Normal anyway;
    #     we tighten via post-processing in apply_postprocess.py) -----------

    # --- Table styles ------------------------------------------------------
    # pandoc default table style is 'Table'; we override its font to 宋体 10.5pt
    for tbl_name in ('Table Grid', 'Table'):
        try:
            ts = doc.styles[tbl_name]
            set_cn_font(ts.font, 'Times New Roman', '宋体', 10.5)
            set_paragraph_indent_and_spacing(ts.paragraph_format,
                                             first_line_chars=0,
                                             line_pt=14, space_before=0, space_after=0)
        except KeyError:
            pass

    # --- Page setup --------------------------------------------------------
    # margins='generic' → 通用 A4（Word 默认风格，适合申报书/标书/方案等非公文材料）
    # margins='gb'      → GB/T 9704 公文版心：天头37/地脚35/订口28/切口26 mm
    #                     （版心 156×225mm，正式党政公文或评审要求公文格式时用）
    if margins == 'gb':
        top, bottom, left, right = 3.7, 3.5, 2.8, 2.6
    else:
        top, bottom, left, right = 2.54, 2.54, 3.18, 3.18
    for section in doc.sections:
        section.page_width = Cm(21)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(top)
        section.bottom_margin = Cm(bottom)
        section.left_margin = Cm(left)
        section.right_margin = Cm(right)

    doc.save(out_path)
    print(f'Reference docx written: {out_path}')


if __name__ == '__main__':
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else 'reference.docx'
    margins = sys.argv[2] if len(sys.argv) > 2 else 'generic'  # 'generic' | 'gb'
    main(out, margins=margins)
