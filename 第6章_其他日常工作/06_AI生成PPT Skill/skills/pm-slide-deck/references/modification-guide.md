# 幻灯片修改指南

初始生成后修改单张幻灯片的工作流。

## 编辑单张幻灯片

修改内容后重新生成指定幻灯片：

1. 识别要编辑的幻灯片（如 `03-slide-key-findings.png`）
2. 更新 `prompts/03-slide-key-findings.md` 中的提示词
3. 如内容变化较大，更新文件名中的 slug
4. 使用相同的会话 ID 重新生成图片
5. 重新生成 PPTX 和 PDF

## 新增幻灯片

在指定位置插入新幻灯片：

1. 指定插入位置（如在第 3 张之后）
2. 创建带有合适 slug 的新提示词（如 `04-slide-new-section.md`）
3. 生成新的幻灯片图片
4. **重新编号文件**：所有后续幻灯片的 NN 递增 1
   - `04-slide-conclusion.png` → `05-slide-conclusion.png`
   - slug 保持不变
5. 更新 `outline.md` 添加新的幻灯片条目
6. 重新生成 PPTX 和 PDF

## 删除幻灯片

删除幻灯片并重新编号：

1. 识别要删除的幻灯片（如 `03-slide-key-findings.png`）
2. 删除图片文件和提示词文件
3. **重新编号文件**：所有后续幻灯片的 NN 递减 1
   - `04-slide-conclusion.png` → `03-slide-conclusion.png`
   - slug 保持不变
4. 更新 `outline.md` 移除该幻灯片条目
5. 重新生成 PPTX 和 PDF

## 文件命名规范

文件使用有意义的 slug 以提高可读性：

```
NN-slide-[slug].png
NN-slide-[slug].md（在 prompts/ 目录下）
```

示例：
- `01-slide-cover.png`
- `02-slide-problem-statement.png`
- `03-slide-key-findings.png`
- `04-slide-back-cover.png`

## Slug 规则

| 规则 | 说明 |
|------|------|
| 格式 | 短横线命名法（小写字母，连字符分隔） |
| 来源 | 从幻灯片标题/内容中派生 |
| 唯一性 | 在整套幻灯片中必须唯一 |
| 更新 | 内容发生显著变化时更换 slug |

## 重新编号规则

| 场景 | 操作 |
|------|------|
| 新增幻灯片 | 后续所有幻灯片的 NN 递增 |
| 删除幻灯片 | 后续所有幻灯片的 NN 递减 |
| 调整顺序 | 更新 NN 以匹配新位置 |
| 编辑幻灯片 | NN 不变，必要时更新 slug |

**重要**：重新编号时 slug 保持不变，只有 NN 前缀会改变。

## 修改后检查清单

每次修改后：

- [ ] 图片文件已正确重命名/创建
- [ ] 提示词文件已正确重命名/创建
- [ ] 后续文件已重新编号（新增/删除时）
- [ ] `outline.md` 已更新以反映变更
- [ ] PPTX 已重新生成
- [ ] PDF 已重新生成
- [ ] outline 头部的幻灯片总数已更新
