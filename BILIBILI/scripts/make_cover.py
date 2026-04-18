#!/usr/bin/env python3
"""Generate cover image with watermark from a video frame."""

import argparse
import os
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def extract_frame(video_path, timestamp, output_path):
    """Extract a single frame from video at given timestamp."""
    cmd = [
        "ffmpeg", "-y",
        "-ss", timestamp,
        "-i", video_path,
        "-frames:v", "1",
        "-q:v", "2",
        output_path,
    ]
    subprocess.run(cmd, capture_output=True, check=True)


def add_watermark(image_path, output_path, badge_text="AI字幕"):
    """Add watermark badge to cover image."""
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    # Try to load a CJK font
    font_paths = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    ]
    
    font = None
    for fp in font_paths:
        if os.path.exists(fp):
            try:
                font = ImageFont.truetype(fp, 28)
                break
            except Exception:
                continue
    
    if font is None:
        font = ImageFont.load_default()

    bbox = font.getbbox(badge_text)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    padding_x, padding_y = 10, 6
    x = img.width - text_w - padding_x * 2 - 10
    y = img.height - text_h - padding_y * 2 - 10

    # Semi-transparent background
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rounded_rectangle(
        [x - padding_x, y - padding_y, x + text_w + padding_x, y + text_h + padding_y],
        radius=8,
        fill=(0, 0, 0, 160),
    )
    
    img = img.convert("RGBA")
    img = Image.alpha_composite(img, overlay)
    img = img.convert("RGB")
    
    draw = ImageDraw.Draw(img)
    draw.text((x, y), badge_text, font=font, fill=(255, 255, 255))

    img.save(output_path, quality=92)


def main():
    parser = argparse.ArgumentParser(description="Generate cover image with watermark.")
    parser.add_argument("video", help="Path to video file")
    parser.add_argument("--timestamp", default="00:00:03", help="Timestamp for frame extraction (default: 3s)")
    parser.add_argument("--output", default=None, help="Output path for cover image")
    parser.add_argument("--badge", default="AI字幕", help="Badge text (default: AI字幕)")
    args = parser.parse_args()

    video_dir = Path(args.video).parent
    raw_path = video_dir / "cover_raw.jpg"
    out_path = Path(args.output) if args.output else video_dir / "cover.jpg"

    print(f"Extracting frame at {args.timestamp}...")
    extract_frame(args.video, args.timestamp, str(raw_path))

    print("Adding watermark...")
    add_watermark(str(raw_path), str(out_path), args.badge)

    print(f"Cover saved to: {out_path}")


if __name__ == "__main__":
    main()