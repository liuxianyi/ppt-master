# Tools

这个目录用于存放与 PPT Master 配套、但不属于主流程脚本的独立辅助工具。

## 当前工具

| 工具 | 说明 |
|------|------|
| [`doc/`](./doc/) | 旧版 Word 文档转换工具，支持将 `.doc` 自动转为 `.docx` 后再转成 Markdown。 |
| [`markitdown/`](./markitdown/) | 基于 `markitdown` 的本地文档转 Markdown 工具，支持 PDF、DOCX、PPTX、XLSX、HTML、图片等常见格式。 |
| [`youtube/`](./youtube/) | 基于 `yt-dlp` / `youtube-dl` 的 YouTube 下载辅助工具，支持优先下载 `mp4`、提取音频和保存元数据。 |

## 设计原则

- `tools/` 下的内容应保持独立，不影响 `skills/ppt-master/scripts/` 主工作流。
- 每个工具建议单独建立子目录，并提供自己的 `README.md`。
- 优先提供轻量包装脚本，避免为仓库引入新的强依赖。
- 如依赖第三方程序，应在文档中明确安装方式、适用场景与限制。
