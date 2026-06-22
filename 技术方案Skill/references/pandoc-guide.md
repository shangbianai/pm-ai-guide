# Pandoc 中文排版指南

## 安装 Pandoc

- Windows: `winget install pandoc` 或从 https://pandoc.org/installing.html 下载
- macOS: `brew install pandoc`
- Linux: `apt install pandoc` 或 `dnf install pandoc`

验证安装：`pandoc --version`

## 基本转换命令

```bash
pandoc input.md \
  --reference-doc=reference.docx \
  --from=markdown+pipe_tables \
  --to=docx \
  --output=output.docx
```

## 带目录的转换

```bash
pandoc input.md \
  --reference-doc=reference.docx \
  --from=markdown+pipe_tables \
  --to=docx \
  --toc --toc-depth=3 \
  --output=output.docx
```

## 常见问题与解决方案

### 1. 图片被文字截断/遮挡

**原因**：reference.docx 的 Normal 样式设置了固定行高（如 28pt），图片高度超过行高被裁剪。

**解决**：在 reference.docx 中不要给 Normal 样式设置 Exactly 行高，改为 At Least。或者在后处理脚本中，找到所有包含图片的段落，将其行高改为 `auto`（行距倍数 1.0）。

`apply_postprocess.py` 已自动处理。

### 2. 图片不居中

**原因**：Pandoc 将图片插入到 Normal 样式的段落中，Normal 样式有首行缩进。

**解决**：后处理脚本中找到所有包含 `w:drawing` 的段落，清除首行缩进并设置居中对齐。

`apply_postprocess.py` 已自动处理。

### 3. 标题字体不是中文

**原因**：reference.docx 的 Heading 样式未设置 east-asia 字体。

**解决**：在 `make_reference.py` 中，为每个 Heading 样式显式设置 `w:eastAsia` 字体属性。

### 4. 表格样式不对

**原因**：Pandoc 默认使用 "Table" 样式，该样式可能不符合中文排版规范。

**解决**：后处理脚本处理所有表格：
- 设置三线表边框
- 表头行加黑体
- 表体行加宋体
- 清除表格内首行缩进

`apply_postprocess.py` 已自动处理。

### 5. 中文引号变成英文

**原因**：Pandoc 的 `--from=markdown` 默认不处理中文引号转换。

**解决**：在 Pandoc 转换之前用 `fix_quotes.py` 预处理 markdown 文件，将 ASCII " 替换为配对的中文引号 " "。

### 6. 中文文件名图片引用失败

**原因**：某些系统上 Pandoc 无法正确解析含中文的图片路径。

**解决**：图片文件名全部使用英文（如 `img_4-1_architecture.png`），中文信息放在路径的目录名中。

### 7. 标题编号混乱（如 1.3.1 和 一 并存）

**原因**：不同作者使用了不同的编号体系。

**解决**：用 `renumber_h3.py` 在 markdown 阶段统一编号格式。规则：
- 如果某 H2 节下已有带数字编号的 H3（如 "4.4.1 xxx"），则其他中文编号的 H3 降级为 H4
- 否则给中文编号的 H3 补上数字编号

### 8. 转换后页数大幅减少

**原因**：可能是：
- reference.docx 的字号/行距设置比原文档更紧凑
- Pandoc 未能正确继承某些样式

**解决**：
- 对比 reference.docx 和原文档的 Normal 样式参数
- 确认 `make_reference.py` 生成的字号、行距、页边距与期望一致
- 如果要从已有文档继承样式，使用 `strip_reference.py` 提取

## reference.docx 生成策略

两种方式：

### 方式一：从零生成（推荐）

```bash
python scripts/make_reference.py reference.docx
```

这会生成一个干净的 reference.docx，样式按formatting-spec.md 标准设置。

### 方式二：从已有文档提取

```bash
python scripts/strip_reference.py 已有的文档.docx reference.docx
```

这会提取已有文档的样式定义，但清除正文内容。适用于需要完全匹配某个已有文档格式的场景。

## 依赖

后处理脚本依赖 `python-docx`：

```bash
pip install python-docx
```

Pandoc 本身不依赖 Python。
