#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
高质量MP4视频转GIF工具
使用ffmpeg的高级滤镜确保生成的GIF保持最佳画质
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def check_ffmpeg():
    """检查ffmpeg是否已安装"""
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      stdout=subprocess.PIPE, 
                      stderr=subprocess.PIPE, 
                      check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_video_info(input_file):
    """获取视频信息"""
    try:
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height,r_frame_rate',
            '-of', 'csv=p=0',
            input_file
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        width, height, fps_str = result.stdout.strip().split(',')
        
        # 计算fps
        if '/' in fps_str:
            num, den = fps_str.split('/')
            fps = int(num) / int(den)
        else:
            fps = float(fps_str)
        
        return int(width), int(height), fps
    except Exception as e:
        print(f"警告: 无法获取视频信息，将使用默认设置: {e}")
        return None, None, None


def convert_mp4_to_gif(input_file, output_file=None, fps=None, width=None, quality='high'):
    """
    将MP4视频转换为高质量GIF
    
    参数:
        input_file: 输入的MP4文件路径
        output_file: 输出的GIF文件路径（可选，默认为输入文件名+.gif）
        fps: 帧率（可选，默认保持原视频帧率或15fps）
        width: 宽度（可选，默认保持原视频宽度）
        quality: 质量级别 ('high', 'ultra', 'medium')
    """
    
    # 检查输入文件
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"输入文件不存在: {input_file}")
    
    # 设置输出文件名
    if output_file is None:
        output_file = Path(input_file).stem + '.gif'
    
    # 获取视频信息
    video_width, video_height, video_fps = get_video_info(input_file)
    
    # 设置参数
    if fps is None:
        fps = min(video_fps if video_fps else 15, 30)  # 最高30fps，过高会导致文件过大
    
    # 根据质量级别设置参数
    quality_settings = {
        'medium': {
            'stats_mode': 'diff',
            'dither': 'bayer:bayer_scale=3'
        },
        'high': {
            'stats_mode': 'full',
            'dither': 'sierra2_4a'
        },
        'ultra': {
            'stats_mode': 'full',
            'dither': 'floyd_steinberg'
        }
    }
    
    settings = quality_settings.get(quality, quality_settings['high'])
    
    print(f"开始转换: {input_file}")
    print(f"输出文件: {output_file}")
    print(f"质量级别: {quality}")
    print(f"帧率: {fps} fps")
    if width:
        print(f"宽度: {width}px (高度自动)")
    else:
        print(f"分辨率: 保持原视频 ({video_width}x{video_height})")
    
    # 第一步：生成调色板（palette）
    # 这是生成高质量GIF的关键！
    palette_file = '/tmp/palette.png'
    
    # 构建滤镜链
    if width:
        scale_filter = f"fps={fps},scale={width}:-1:flags=lanczos"
    else:
        scale_filter = f"fps={fps},scale=flags=lanczos"
    
    palette_cmd = [
        'ffmpeg',
        '-y',  # 覆盖输出文件
        '-i', input_file,
        '-vf', f"{scale_filter},palettegen=stats_mode={settings['stats_mode']}:max_colors=256",
        palette_file
    ]
    
    print("\n步骤 1/2: 生成调色板...")
    try:
        subprocess.run(palette_cmd, check=True, stderr=subprocess.PIPE)
        print("✓ 调色板生成完成")
    except subprocess.CalledProcessError as e:
        print(f"错误: 生成调色板失败")
        print(e.stderr.decode('utf-8', errors='ignore'))
        return False
    
    # 第二步：使用调色板生成GIF
    gif_cmd = [
        'ffmpeg',
        '-y',
        '-i', input_file,
        '-i', palette_file,
        '-lavfi', f"{scale_filter}[x];[x][1:v]paletteuse=dither={settings['dither']}",
        output_file
    ]
    
    print("\n步骤 2/2: 生成GIF...")
    try:
        subprocess.run(gif_cmd, check=True, stderr=subprocess.PIPE)
        print("✓ GIF生成完成")
    except subprocess.CalledProcessError as e:
        print(f"错误: 生成GIF失败")
        print(e.stderr.decode('utf-8', errors='ignore'))
        return False
    finally:
        # 清理临时文件
        if os.path.exists(palette_file):
            os.remove(palette_file)
    
    # 显示文件大小
    input_size = os.path.getsize(input_file) / (1024 * 1024)
    output_size = os.path.getsize(output_file) / (1024 * 1024)
    print(f"\n✓ 转换成功！")
    print(f"原视频大小: {input_size:.2f} MB")
    print(f"GIF大小: {output_size:.2f} MB")
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description='高质量MP4视频转GIF工具 - 保持最佳画质',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础转换（自动优化）
  python mp4_to_gif.py input.mp4
  
  # 指定输出文件名
  python mp4_to_gif.py input.mp4 -o output.gif
  
  # 设置帧率（推荐15-30）
  python mp4_to_gif.py input.mp4 -fps 20
  
  # 设置宽度（保持宽高比）
  python mp4_to_gif.py input.mp4 -w 800
  
  # 超高质量模式
  python mp4_to_gif.py input.mp4 -q ultra
  
  # 完整参数示例
  python mp4_to_gif.py input.mp4 -o output.gif -fps 25 -w 1920 -q ultra
        """
    )
    
    parser.add_argument('input', help='输入的MP4视频文件')
    parser.add_argument('-o', '--output', help='输出的GIF文件路径（可选）')
    parser.add_argument('-fps', '--fps', type=float, help='帧率（默认保持原视频帧率，最高30fps）')
    parser.add_argument('-w', '--width', type=int, help='输出宽度（像素），高度自动计算保持宽高比')
    parser.add_argument('-q', '--quality', 
                       choices=['medium', 'high', 'ultra'],
                       default='high',
                       help='质量级别: medium(中等), high(高), ultra(超高) - 默认: high')
    
    args = parser.parse_args()
    
    # 检查ffmpeg
    if not check_ffmpeg():
        print("错误: 未找到ffmpeg，请先安装ffmpeg")
        print("\nUbuntu/Debian: sudo apt-get install ffmpeg")
        print("macOS: brew install ffmpeg")
        print("Windows: 从 https://ffmpeg.org/download.html 下载")
        sys.exit(1)
    
    # 转换视频
    success = convert_mp4_to_gif(
        args.input,
        args.output,
        args.fps,
        args.width,
        args.quality
    )
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
