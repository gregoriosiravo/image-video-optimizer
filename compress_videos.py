#!/usr/bin/env python3
"""
Batch compress videos to H.264 web-optimized MP4 (YouTube/Vimeo HQ 1080p30).
Usage: python compress_videos.py [folder] [--output OUTPUT] [--crf 28] [--delete-originals]
"""

import argparse
import subprocess
import sys
from pathlib import Path

VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".avi", ".m4v", ".wmv", ".flv", ".webm", ".mts", ".m2ts"}


def get_ffmpeg_cmd(input_path: Path, output_path: Path, crf: int) -> list:
    return [
        "ffmpeg", "-y",
        "-i", str(input_path),
        # Video
        "-c:v", "libx264",
        "-crf", str(crf),
        "-preset", "slow",          
        "-profile:v", "high",    
        "-level:v", "4.0",
        "-pix_fmt", "yuv420p",       
        "-vf", "scale=-2:min(ih\\,1080),fps=30", 
        "-movflags", "+faststart",
        # Audio
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "48000",              
        "-ac", "2",         
        str(output_path),
    ]


def get_duration(input_path: Path) -> float | None:
    """Returns video duration in seconds via ffprobe."""
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(input_path)],
            capture_output=True, text=True
        )
        val = result.stdout.strip()
        return float(val) if val else None
    except Exception:
        return None


def compress_videos(
    folder: Path,
    output: Path,
    crf: int = 28,
    delete_originals: bool = False
) -> None:
    video_files = [f for f in folder.iterdir() if f.suffix.lower() in VIDEO_EXTENSIONS]

    if not video_files:
        print("⚠️  No video files found in the specified folder.")
        sys.exit(0)

    output.mkdir(parents=True, exist_ok=True)

    print(f" Found {len(video_files)} video(s) in '{folder}'")
    print(f" Output folder: '{output}'")
    print(f" Codec: H.264 | CRF: {crf} | Preset: slow | 1080p30 | AAC 192k\n")
    converted, failed = 0, 0

    for video_path in video_files:
        output_path = output / (video_path.stem + ".mp4")
        if output_path.exists():
            print(f"  ⏭️  {video_path.name} — already compressed, skipping.")
            continue
        print(f" {video_path.name} …")
        cmd = get_ffmpeg_cmd(video_path, output_path, crf)

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                print(f" {video_path.name} — FFmpeg error:")
                # Print last 5 lines of stderr for diagnostics
                for line in result.stderr.strip().splitlines()[-5:]:
                    print(f"     {line}")
                failed += 1
                continue

            size_before = video_path.stat().st_size / (1024 * 1024)
            size_after  = output_path.stat().st_size / (1024 * 1024)
            saving = 100 - (size_after / size_before * 100)
            duration = get_duration(output_path)
            duration_str = f"{duration:.1f}s" if duration else "n/a"

            print(f"  ✅ {video_path.name} → {output_path.name}  "
                  f"({size_before:.1f} MB → {size_after:.1f} MB, -{saving:.0f}%)"
                  f"  [{duration_str}]")

            if delete_originals:
                video_path.unlink()
            converted += 1

        except FileNotFoundError:
            print(" FFmpeg not found. Install it: https://ffmpeg.org/download.html")
            sys.exit(1)
        except Exception as e:
            print(f" {video_path.name} — Unexpected error: {e}")
            failed += 1

    print(f"\n🎉 Done! {converted} compressed, {failed} failed.")
    print(f"📂 Output: {output.resolve()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch compress videos → H.264 Web/YouTube/Vimeo HQ")
    parser.add_argument("folder", nargs="?", default="./videos", help="Source folder with videos")
    parser.add_argument("--output", default=None, help="Output folder (default: <source>/compressed)")
    parser.add_argument("--crf", type=int, default=28, choices=range(0, 52), metavar="[0-51]",
                        help="H.264 CRF quality: 18=HQ, 23=default, 28-30=web balanced (default: 28)")
    parser.add_argument("--delete-originals", action="store_true", help="Delete source files after compression")
    args = parser.parse_args()

    folder = Path(args.folder).resolve()
    if not folder.is_dir():
        print(f" Folder not found: {folder}")
        sys.exit(1)
    

    output = Path(args.output).resolve() if args.output else folder / "compressed"
    compress_videos(folder, output, crf=args.crf, delete_originals=args.delete_originals)
