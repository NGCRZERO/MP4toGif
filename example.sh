#!/bin/bash
# MP4转GIF使用示例脚本

echo "============================================"
echo "MP4转GIF高质量转换工具 - 使用示例"
echo "============================================"
echo ""

# 检查是否提供了输入文件
if [ -z "$1" ]; then
    echo "使用方法："
    echo "  bash example.sh <你的视频文件.mp4>"
    echo ""
    echo "示例："
    echo "  bash example.sh myvideo.mp4"
    echo ""
    echo "说明：此脚本将演示三种质量级别的转换效果"
    exit 1
fi

INPUT_FILE="$1"

# 检查输入文件是否存在
if [ ! -f "$INPUT_FILE" ]; then
    echo "错误：找不到文件 '$INPUT_FILE'"
    exit 1
fi

FILENAME=$(basename "$INPUT_FILE" | sed 's/\.[^.]*$//')

echo "输入文件: $INPUT_FILE"
echo ""

# 示例1：默认高质量模式
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "示例1: 默认高质量模式 (推荐)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 mp4_to_gif.py "$INPUT_FILE" -o "${FILENAME}_high.gif"
echo ""

# 示例2：超高质量模式（保持原分辨率）
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "示例2: 超高质量模式"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 mp4_to_gif.py "$INPUT_FILE" -o "${FILENAME}_ultra.gif" -q ultra
echo ""

# 示例3：自定义帧率和宽度
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "示例3: 自定义参数 (25fps, 800px宽)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
python3 mp4_to_gif.py "$INPUT_FILE" -o "${FILENAME}_custom.gif" -fps 25 -w 800 -q high
echo ""

echo "============================================"
echo "✓ 转换完成！生成了以下文件："
echo "  - ${FILENAME}_high.gif (高质量)"
echo "  - ${FILENAME}_ultra.gif (超高质量)"
echo "  - ${FILENAME}_custom.gif (自定义)"
echo ""
echo "可以使用以下命令查看文件大小："
echo "  ls -lh ${FILENAME}*.gif"
echo "============================================"
