import os
import argparse
from lxml import etree

def clean_svg_images(input_path, output_path):
    # 解析 SVG 文件
    parser = etree.XMLParser(remove_blank_text=True)
    try:
        tree = etree.parse(input_path, parser)
    except Exception as e:
        print(f"解析 SVG 失败: {e}")
        return
        
    root = tree.getroot()

    # 定义命名空间
    namespaces = {
        'svg': 'http://www.w3.org/2000/svg',
        'xlink': 'http://www.w3.org/1999/xlink'
    }

    # 查找所有的 image 标签
    images = root.xpath('//svg:image | //image', namespaces=namespaces)
    
    count = 0
    for img in images:
        # 获取原有的属性
        x = img.get('x', '0')
        y = img.get('y', '0')
        width = img.get('width')
        height = img.get('height')
        transform = img.get('transform')

        # 创建一个矩形替代图片
        rect = etree.Element('{http://www.w3.org/2000/svg}rect')
        rect.set('x', x)
        rect.set('y', y)
        if width: rect.set('width', width)
        if height: rect.set('height', height)
        if transform: rect.set('transform', transform)
        
        # 设置样式：浅灰色填充和深灰色细边框
        rect.set('fill', '#f0f0f0') 
        rect.set('stroke', '#cccccc')
        rect.set('stroke-width', '1')

        # 用矩形替换掉图片节点
        img.getparent().replace(img, rect)
        count += 1

    # 保存结果
    try:
        with open(output_path, 'wb') as f:
            f.write(etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding='utf-8'))
        print(f"处理成功！共替换了 {count} 张图片。")
        print(f"文件已保存至: {output_path}")
    except Exception as e:
        print(f"保存文件失败: {e}")

if __name__ == "__main__":
    # 配置命令行参数解析器
    parser = argparse.ArgumentParser(
        description="清理 SVG 文件中的内嵌 Base64 图片，并用带有原始宽高的灰色占位框替换它们。"
    )
    
    # 添加输入和输出参数
    parser.add_argument("-i", "--input", required=True, help="输入的 SVG 文件路径")
    parser.add_argument("-o", "--output", required=True, help="输出的 SVG 文件路径")
    
    # 解析命令行输入的参数
    args = parser.parse_args()
    
    # 检查输入文件是否存在
    if os.path.exists(args.input):
        clean_svg_images(args.input, args.output)
    else:
        print(f"错误：未找到输入文件 '{args.input}'，请检查路径是否正确。")