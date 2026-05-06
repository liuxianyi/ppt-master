# DOC 转 Markdown 工具

这个目录提供一个专门处理旧版 Word 文档的辅助工具：当输入是 `.doc` 时，先自动转成 `.docx`，再调用 PPT Master 自带的 [doc_to_md.py](file:///Users/apple/Desktop/work/ppt-master/skills/ppt-master/scripts/source_to_md/doc_to_md.py) 转成 Markdown。

## 适用场景

- 你手头是老式 Word 97-2003 文档 `.doc`
- 直接用 `markitdown` 处理 `.doc` 报 `UnsupportedFormatException`
- 你希望保留在 PPT Master 仓库内完成 `doc` -> `docx` -> `md`

## 目录结构

```text
tools/
  doc/
    README.md
    doc_tool.py
```

## 依赖

脚本本身只依赖 Python 3，但处理 `.doc` 时还需要以下任一外部工具：

- `LibreOffice` / `soffice`：推荐，兼容旧版 `.doc` 更稳
- `pandoc`：可作为后备方案

安装示例：

```bash
# 推荐
brew install --cask libreoffice

# 或后备方案
brew install pandoc
```

如果输入本来就是 `.docx`，则不需要上面的转换器，脚本会直接调用仓库自带的 `doc_to_md.py`。

## 快速开始

把 `.doc` 转成 Markdown：

```bash
python3 tools/doc/doc_tool.py "无人机应用技术专业人才培养方案修订情况的汇报.doc"
```

如果想指定输出 Markdown 路径：

```bash
python3 tools/doc/doc_tool.py \
  "无人机应用技术专业人才培养方案修订情况的汇报.doc" \
  -o projects/seconf/tmp.md
```

如果想保留中间生成的 `.docx`：

```bash
python3 tools/doc/doc_tool.py \
  "无人机应用技术专业人才培养方案修订情况的汇报.doc" \
  --keep-docx
```

如果输入已经是 `.docx`，也可以直接用这个工具：

```bash
python3 tools/doc/doc_tool.py "项目方案.docx"
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `input` | 必填，输入 `.doc` 或 `.docx` 文件 |
| `-o`, `--output` | 输出 Markdown 路径 |
| `--docx-output` | 自定义中间 `.docx` 输出路径，仅 `.doc` 输入时有效 |
| `--keep-docx` | 保留中间转换得到的 `.docx` 文件 |
| `--print-command` | 打印底层实际执行的命令，便于排查 |

## 工作流程

1. 检查输入文件扩展名
2. 如果是 `.doc`，优先用 `LibreOffice`，否则回退到 `pandoc` 转成 `.docx`
3. 调用仓库脚本 `skills/ppt-master/scripts/source_to_md/doc_to_md.py`
4. 输出 `.md`，并在默认情况下删除中间 `.docx`

## 与 markitdown 的区别

- 这个工具不依赖 `markitdown` 处理 `.doc`
- 重点是绕开旧版 `.doc` 的格式兼容问题
- 真正的 Markdown 转换仍交给 PPT Master 自带脚本完成，更贴近仓库主流程

## 注意事项

- 文件名含空格或中文时，请始终用双引号包住路径
- 某些极旧或损坏的 `.doc` 文件，即使使用 LibreOffice 也可能转换失败
- 如果 `.doc` 中包含复杂公式、批注、修订记录，Markdown 输出可能需要人工整理
