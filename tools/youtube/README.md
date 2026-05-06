# YouTube 工具

这个目录提供一个基于 `yt-dlp` / `youtube-dl` 的轻量辅助工具，用来下载 YouTube 视频、音频或元数据，方便你在 PPT Master 工作流之外先收集素材，再决定是否将内容整理进演示文稿。

## 适用场景

- 下载演讲、发布会、课程、采访等 YouTube 视频作为研究素材。
- 只提取音频，便于转写、摘要或内容整理。
- 保存缩略图与元数据，用于封面参考、资料归档或后续人工分析。
- 在不修改 PPT Master 主流程的前提下，为项目补充外部视频资料。

## 目录结构

```text
tools/
  youtube/
    README.md
    youtube_tool.py
```

## 依赖

本工具本身只依赖 Python 3，但真正执行下载时需要系统里已经安装 `yt-dlp` 或 `youtube-dl`。

推荐优先安装 `yt-dlp`，它对新版 YouTube 页面和 `Shorts` 的兼容性更好。常见安装方式如下：

```bash
# macOS
brew install yt-dlp

# 或使用 pip
python3 -m pip install --upgrade yt-dlp
```

如果你仍然需要兼容旧命令，也可以安装 `youtube-dl`：

```bash
brew install youtube-dl
python3 -m pip install --upgrade youtube-dl
```

相关项目主页：

- <https://github.com/ytdl-org/youtube-dl>
- <https://github.com/yt-dlp/yt-dlp>

## 快速开始

进入仓库根目录后运行。脚本默认优先下载 `mp4`：

```bash
python3 tools/youtube/youtube_tool.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

也支持直接传入 `Shorts` 链接，脚本会自动转换为普通视频链接：

```bash
python3 tools/youtube/youtube_tool.py "https://www.youtube.com/shorts/VIDEO_ID"
```

默认会将文件下载到当前工作目录下的 `downloads/` 文件夹，并使用如下命名模板：

```text
%(upload_date)s_%(title)s_%(id)s.%(ext)s
```

## 常用命令

下载 `mp4` 视频：

```bash
python3 tools/youtube/youtube_tool.py \
  "https://www.youtube.com/watch?v=VIDEO_ID" \
  -o tools/youtube/downloads
```

下载 `Shorts` 为 `mp4`：

```bash
python3 tools/youtube/youtube_tool.py \
  "https://www.youtube.com/shorts/3kMeu2LsCRI" \
  -o tools/youtube/downloads
```

只下载音频并转为 MP3：

```bash
python3 tools/youtube/youtube_tool.py \
  "https://www.youtube.com/watch?v=VIDEO_ID" \
  --audio-only \
  -o tools/youtube/audio
```

同时保存元数据和缩略图：

```bash
python3 tools/youtube/youtube_tool.py \
  "https://www.youtube.com/watch?v=VIDEO_ID" \
  --write-info-json \
  --write-thumbnail \
  -o tools/youtube/assets
```

打印最终执行的 `youtube-dl` 命令：

```bash
python3 tools/youtube/youtube_tool.py \
  "https://www.youtube.com/watch?v=VIDEO_ID" \
  --print-command
```

查看可用清晰度与格式：

```bash
python3 tools/youtube/youtube_tool.py \
  "https://www.youtube.com/watch?v=VIDEO_ID" \
  --list-formats
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `url` | 必填，YouTube 视频或播放列表链接 |
| `-o`, `--output-dir` | 输出目录，默认 `downloads` |
| 默认行为 | 优先下载 `mp4`，文件扩展名通常为 `.mp4` |
| `--audio-only` | 仅下载音频，并调用 `youtube-dl -x --audio-format mp3` |
| `--list-formats` | 列出源视频可用格式，不执行下载 |
| `--write-info-json` | 保存视频元数据 JSON |
| `--write-thumbnail` | 保存视频缩略图 |
| `--print-command` | 打印解析后的底层命令，便于调试 |

## 与 PPT Master 的关系

这个工具是独立辅助工具，不属于 `skills/ppt-master/scripts/` 主工作流，也不会被默认调用。推荐使用方式：

1. 先用本工具把视频、音频或缩略图下载到本地。
2. 再手动整理为摘要、截图、转写文本或参考图片。
3. 最后把整理好的资料放入 `projects/<project_name>/sources/` 或 `images/`，交给 PPT Master 继续处理。

## 注意事项

- 请确保你对目标内容拥有合法下载和使用权限，并遵守所在地区法律、平台服务条款与版权要求。
- 某些视频可能因地区限制、登录限制、年龄限制或反爬策略无法直接下载。
- 脚本会优先调用 `yt-dlp`，找不到时再回退到 `youtube-dl`。
- `youtube-dl` 对新版 `Shorts` 支持较弱，建议优先安装 `yt-dlp`。
- 本工具当前未额外处理 cookies、代理或账号登录等高级场景。
- 如果系统中未安装下载器，脚本会直接报错并给出安装提示。

## 后续可扩展方向

- 增加字幕下载参数，如自动字幕或人工字幕导出。
- 增加播放列表批量下载控制。
- 增加下载后自动抽帧、生成封面候选图、提取音频摘要等二次处理能力。
