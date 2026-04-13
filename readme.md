# image-video-optimizer

A lightweight Python utility to batch convert JPG images to WebP format and compress video files, optimizing assets for web delivery and storage.

## Features

- Convert `.jpg` / `.jpeg` images to `.webp` with configurable quality
- Compress video files using FFmpeg (H.264/H.265)
- Batch processing for entire directories
- Preserves original files by default
- CLI interface for easy integration into workflows

## Requirements

- Python 3.8+
- [Pillow](https://python-pillow.org/) — image conversion
- [FFmpeg](https://ffmpeg.org/) — video compression (must be installed and in PATH)

Install Python dependencies:

```bash
pip install -r requirements.txt
```

### requirements.txt

## Installation

```bash
git clone https://github.com/gregoriosiravo/image-video-optimizer.git
cd image-video-optimizer
pip install -r requirements.txt
```

Make sure FFmpeg is installed:

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html and add to PATH
```

## Usage

### Convert images to WebP

minimal usage:

```bash
python convert_to_webp.py
# reads from ./images, saves to ./images/webp with default quality 85 and keeps originals
```

custom input/output and quality:

```bash
python convert_to_webp.py ./photos --output ./output --quality 90 --delete-originals
# reads from ./photos, saves to ./output with quality 90 and deletes original JPGs
```

### Compress videos

minimal usage:

```bash
python compress_videos.py
# reads from ./videos
# saves to ./videos/compressed
# CRF 28, keeps originals
```

custom input/output and CRF:

```bash
python compress_videos.py ./my_videos --output ./my_videos/compressed --crf 23 --delete-originals

```

## Options

| Flag                 | Description                              | Default    |
| -------------------- | ---------------------------------------- | ---------- |
| `--input`            | Input file or directory                  | `.`        |
| `--output`           | Output directory                         | `./output` |
| `--crf`              | Video CRF value (lower = better quality) | `28`       |
| `--delete-originals` | Delete source files after compression    | `False`    |

## Output

Processed files are saved to the `--output` directory with the same filename and updated extension (`.webp` for images). Original files are never overwritten unless explicitly configured.

## License

MIT
