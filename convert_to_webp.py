#!/usr/bin/env python3
"""
Convert all .jpg / .jpeg files in a folder to .webp
Usage: python convert_to_webp.py [folder_path] [--quality 85] [--delete-originals]
"""

import argparse
import os
import sys
from pathlib import Path
from PIL import Image


def convert_jpg_to_webp(
    folder: Path,
    output: Path,
    quality: int = 85,
    delete_originals: bool = False
) -> None:
    jpg_files = list(folder.glob("*.jpg")) + list(folder.glob("*.jpeg"))
    jpg_files += list(folder.glob("*.JPG")) + list(folder.glob("*.JPEG"))

    if not jpg_files:
        print(f"folder is: {folder}")
        print("⚠️  No .jpg files found in the specified folder.")
        sys.exit(0)
        
    output.mkdir(parents=True, exist_ok=True)
    print(f"🔍 Found {len(jpg_files)} file(s) in '{folder}'\n")
    converted, failed = 0, 0

    for jpg_path in jpg_files:
        webp_path = output / jpg_path.with_suffix(".webp").name
        try:
            with Image.open(jpg_path) as img:
                img.convert("RGB").save(webp_path, "WEBP", quality=quality, method=6)
            size_before = jpg_path.stat().st_size / 1024
            size_after  = webp_path.stat().st_size / 1024
            saving = 100 - (size_after / size_before * 100)
            print(f" {jpg_path.name} → {webp_path.name}  "
                  f"({size_before:.1f} KB → {size_after:.1f} KB, -{saving:.0f}%)")
            if delete_originals:
                jpg_path.unlink()
            converted += 1
        except Exception as e:
            print(f"X {jpg_path.name} — Error: {e}")
            failed += 1

    print(f"\n DONE! {converted} converted, {failed} failed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Batch convert JPG → WebP")
    parser.add_argument("folder", nargs="?", default="./images", help="Target folder (default: current dir)")
    parser.add_argument("--output", default=None, help="Output folder for .webp files (default: <source_folder>/webp)")
    parser.add_argument("--quality", type=int, default=85, help="WebP quality 1–100 (default: 85)")
    parser.add_argument("--delete-originals", action="store_true", help="Delete original .jpg files after conversion")
    args = parser.parse_args()

    folder = Path(args.folder).resolve()
    if not folder.is_dir():
        print(f"Folder not found: {folder}")
        sys.exit(1)
    if not 1 <= args.quality <= 100:
        print("Quality must be between 1 and 100.")
        sys.exit(1)
        
    output = Path(args.output).resolve() if args.output else folder / "webp"

    convert_jpg_to_webp(folder, output, quality=args.quality, delete_originals=args.delete_originals)
