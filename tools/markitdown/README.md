# MarkItDown 工具

这个目录提供一个基于 `markitdown` 的轻量包装脚本，用于把本地文档直接转换为 Markdown，适合作为独立预处理步骤，先把材料整理成 `.md`，再继续摘要、分析或生成 PPT。

## 适用场景

- 你手头有 `pdf`、`docx`、`pptx`、`xlsx`、`html`、图片等本地文件，想先转成 Markdown
- 你希望优先复用仓库内置的 `markitdown` 源码，而不是手工安装一套新环境
- 你需要一个比直接敲 `markitdown ...` 更稳定的仓库内统一入口

## 目录结构

```text
tools/
  markitdown/
    README.md
    markitdown_tool.py
```

## 依赖

脚本本身只依赖 Python 3。

运行时会按下面顺序寻找 `markitdown`：

1. 系统里已安装的 `markitdown` CLI
2. 当前仓库中的本地源码目录 `markitdown/packages/markitdown/src`
3. 如果你显式传入 `--install-missing`，则从 PyPI 安装 `markitdown[all]`

如果你希望手动安装：

```bash
python3 -m pip install "markitdown[all]"
```

## 快速开始

把 PDF 转成 Markdown：

```bash
python3 tools/markitdown/markitdown_tool.py "/absolute/path/to/report.pdf"
```

默认会在同目录下生成同名 `.md` 文件，例如：

```text
/absolute/path/to/report.pdf -> /absolute/path/to/report.md
```

## 常用命令

指定输出路径：

```bash
python3 tools/markitdown/markitdown_tool.py \
  "/absolute/path/to/spec.docx" \
  -o "/absolute/path/to/output/spec.md"
```

转换 PPTX：

```bash
python3 tools/markitdown/markitdown_tool.py \
  "/absolute/path/to/slides.pptx"
```

转换 XLSX：

```bash
python3 tools/markitdown/markitdown_tool.py \
  "/absolute/path/to/table.xlsx"
```

缺少运行时则自动安装：

```bash
python3 tools/markitdown/markitdown_tool.py \
  "/absolute/path/to/file.pdf" \
  --install-missing
```

启用插件：

```bash
python3 tools/markitdown/markitdown_tool.py \
  "/absolute/path/to/file.pdf" \
  --use-plugins
```

打印底层实际执行命令：

```bash
python3 tools/markitdown/markitdown_tool.py \
  "/absolute/path/to/file.pdf" \
  --print-command
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `input` | 必填，输入文件路径 |
| `-o`, `--output` | 输出 Markdown 路径，默认与源文件同目录同名 `.md` |
| `-x`, `--extension` | 传给 `markitdown` 的扩展名提示 |
| `-m`, `--mime-type` | 传给 `markitdown` 的 MIME 类型提示 |
| `-c`, `--charset` | 传给 `markitdown` 的字符集提示 |
| `--use-plugins` | 启用 `markitdown` 插件 |
| `--install-missing` | 如果未找到运行时，则尝试从 PyPI 安装 |
| `--print-command` | 打印解析后的底层命令，便于排查 |

## 工作方式

1. 检查输入文件是否存在
2. 推导输出 `.md` 路径
3. 优先查找系统已安装的 `markitdown`
4. 如果未安装，则回退到仓库内置源码方式运行
5. 执行转换并校验输出文件已生成且非空

## 与 skill 的关系

这个工具是可执行入口；`.trae/skills/markitdown-converter/SKILL.md` 是面向 agent 的调用说明。两者配合后：

- skill 负责告诉 agent 何时使用 `markitdown`
- tool 负责真正执行本地文件到 Markdown 的转换

## 注意事项

- 这个工具面向本地文件，不处理远程 URL
- 扫描版 PDF 或图片型文档，基础 `markitdown` 可能提取不到完整正文
- 旧版 `.doc` 文件不一定稳定支持，建议先转为 `.docx`
- Markdown 输出更偏向文本提取和结构保留，不保证还原原始排版
