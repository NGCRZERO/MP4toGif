# MP4toGIF - 高质量视频转GIF工具 🎬→🎞️

一个专业的MP4视频转GIF工具，使用ffmpeg高级滤镜技术，**确保生成的GIF保持原视频的高清画质**！

## ✨ 特性

- 🎯 **超高画质**: 使用ffmpeg的palettegen和paletteuse滤镜，生成256色调色板，保证最佳视觉效果
- 🎨 **三种质量模式**: medium（中等）、high（高质量）、ultra（超高质量）
- 📐 **智能分辨率**: 自动保持原视频分辨率或自定义宽度（自动保持宽高比）
- 🎞️ **帧率优化**: 自动匹配原视频帧率（最高30fps）或自定义帧率
- 🚀 **简单易用**: 命令行工具，一键转换
- 💎 **专业算法**: 使用floyd_steinberg、sierra2_4a等高级抖动算法

## 🔧 安装依赖

### 1. 安装ffmpeg

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
从 [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html) 下载并安装

### 2. 验证安装
```bash
ffmpeg -version
```

## 🚀 使用方法

### 基础用法

```bash
# 最简单的转换（自动优化所有参数）
python mp4_to_gif.py input.mp4
```

### 高级用法

```bash
# 指定输出文件名
python mp4_to_gif.py input.mp4 -o output.gif

# 设置帧率（推荐15-30fps，太高会导致文件过大）
python mp4_to_gif.py input.mp4 -fps 20

# 设置宽度（高度自动计算，保持宽高比）
python mp4_to_gif.py input.mp4 -w 800

# 使用超高质量模式
python mp4_to_gif.py input.mp4 -q ultra

# 完整参数示例：超高质量、1920px宽、25fps
python mp4_to_gif.py input.mp4 -o myanimation.gif -fps 25 -w 1920 -q ultra
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `input` | 输入的MP4视频文件（必需） | - |
| `-o, --output` | 输出GIF文件路径 | 输入文件名.gif |
| `-fps, --fps` | 帧率 | 原视频帧率（最高30） |
| `-w, --width` | 输出宽度（像素） | 原视频宽度 |
| `-q, --quality` | 质量级别：medium/high/ultra | high |

## 📊 质量级别对比

| 级别 | stats_mode | dither算法 | 适用场景 |
|------|------------|-----------|---------|
| **medium** | diff | bayer | 快速转换，文件较小 |
| **high** | full | sierra2_4a | 平衡质量和大小（推荐） |
| **ultra** | full | floyd_steinberg | 最佳质量，文件较大 |

## 🎯 技术原理

本工具采用ffmpeg的两步转换法，这是目前业界最佳的GIF生成方案：

1. **第一步 - 生成调色板**: 分析整个视频，生成256色的最优调色板
   - 使用`palettegen`滤镜
   - `stats_mode=full`确保分析整个视频
   - 生成最适合视频内容的颜色集

2. **第二步 - 应用调色板**: 使用调色板转换视频
   - 使用`paletteuse`滤镜
   - 应用高级抖动算法（如floyd_steinberg）
   - 使用lanczos缩放算法保持清晰度

这种方法比直接转换的质量提升**显著**，能够最大程度保持原视频的画质！

## 💡 使用建议

1. **保持原分辨率**: 如果原视频已经是合适的尺寸，不要指定`-w`参数
2. **选择合适帧率**: 15-25fps足够流畅，30fps会显著增加文件大小
3. **质量优先**: 推荐使用`-q high`或`-q ultra`
4. **文件大小控制**: 如果GIF过大，可以降低帧率或减小分辨率

## 📝 示例

```bash
# 示例1: 将手机录制的竖屏视频转换为GIF
python mp4_to_gif.py phone_video.mp4 -fps 20 -w 480 -q high

# 示例2: 将1080p视频转换为高质量GIF（保持原分辨率）
python mp4_to_gif.py video_1080p.mp4 -fps 25 -q ultra

# 示例3: 快速转换，文件大小优先
python mp4_to_gif.py big_video.mp4 -fps 15 -w 640 -q medium

# 示例4: 制作表情包（小尺寸、高帧率）
python mp4_to_gif.py reaction.mp4 -fps 30 -w 320 -q high
```

## ⚠️ 注意事项

- GIF格式最多支持256色，无法完全还原真彩色视频，但本工具已经做到了GIF格式的极限画质
- 长视频转GIF会产生较大的文件，建议先剪辑视频或降低帧率/分辨率
- 确保有足够的磁盘空间
- 转换时间取决于视频长度和质量设置

## 🔍 常见问题

**Q: 为什么GIF文件很大？**  
A: GIF是无损压缩格式，高分辨率、高帧率会导致文件很大。建议：降低fps到15-20，或减小分辨率。

**Q: 画质能和原视频一模一样吗？**  
A: GIF格式限制为256色，无法完全还原真彩色，但本工具使用最先进的算法，已达到GIF格式的画质上限！

**Q: 转换速度慢怎么办？**  
A: 使用`-q medium`模式会更快，或者减小分辨率和帧率。

**Q: 支持其他视频格式吗？**  
A: 支持！ffmpeg支持的所有格式（AVI、MOV、MKV等）都可以转换。

## 📄 许可

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

---

**让你的视频保持高清，转GIF无损画质！** 💪