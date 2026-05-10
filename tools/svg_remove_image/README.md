# PPT 友好 SVG 简化工具

这个工具用于把 SVG 简化为更适合 PowerPoint “转换为对象/形状”的基础元素集合，重点保留：

- `rect`
- `line`
- `path`
- 少量简单 `text`

同时尽量去掉或规避：

- `image`
- `clipPath`
- `mask`
- `filter`
- `use`
- 复杂 `transform`
- 多层嵌套文本

## 脚本位置

`tools/svg_remove_image/main.py`

## 处理方式

脚本会重新解析 SVG，并按以下规则输出新的简化版本：

- 删除 `<image>`、`<clipPath>`、`<mask>`、`<filter>`、`<defs>`、`<use>` 等复杂或不稳定元素
- 保留 `rect`、`line`、`path`、`text`
- 将 `circle`、`ellipse`、`polyline`、`polygon` 转成 `path`
- 将带圆角的 `rect` 转成 `path`
- 扁平化简单文本内容，尽量去掉多层 `tspan`
- 只保留简单 `translate(...)` 位移，复杂 `transform` 会被移除
- 尽量保留 `fill`、`stroke`、`font-size`、`font-family` 等基础样式

这意味着：

- 输出文件不再追求与原 SVG 完全一致
- 目标是提升 PowerPoint 转对象时的稳定性
- 复杂视觉效果可能会被删除或降级

## 使用方式

在项目根目录执行：

```bash
python3 tools/svg_remove_image/main.py <输入SVG文件>
```

如果希望指定输出路径：

```bash
python3 tools/svg_remove_image/main.py <输入SVG文件> -o <输出SVG文件>
```

## 参数说明

- `input`：必填，输入的 SVG 文件路径
- `-o, --output`：选填，输出 SVG 文件路径

## 输出规则

- 如果传入 `-o`，脚本会写入指定路径
- 如果未传入 `-o`，默认输出到输入文件同目录
- 默认输出文件名格式为：`原文件名_no_image.svg`

例如输入文件为：

```text
demo/example.svg
```

默认输出文件为：

```text
demo/example_no_image.svg
```

## 示例

示例 1：使用默认输出文件名

```bash
python3 tools/svg_remove_image/main.py demo/example.svg
```

示例 2：指定输出文件

```bash
python3 tools/svg_remove_image/main.py demo/example.svg -o demo/example.cleaned.svg
```

## 返回结果

脚本执行成功后，会输出：

- 删除的图片节点数量
- 删除的复杂定义数量
- 转换为 `path` 的元素数量
- 被移除的复杂 `transform` 数量
- 输出文件保存路径

如果输入文件不存在，或传入的不是 `.svg` 文件，脚本会直接报错并退出。

## 注意事项

- 这个脚本会重写 SVG 结构，不再是“最小文本改动”
- 它优先保证 PowerPoint 转对象兼容性，不保证视觉 100% 还原
- 复杂滤镜、遮罩、裁剪、符号引用会被移除
- 如果原 SVG 严重依赖复杂变换，导出结果可能仍然出现位置偏差
- 对 `path` 元素，脚本只保留简单的 `translate(...)` 位移，其他变换会被丢弃
