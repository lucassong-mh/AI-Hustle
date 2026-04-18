#!/usr/bin/env python3
"""Burn SRT subtitles into video using ffmpeg."""

import argparse
import subprocess
import sys
from pathlib import Path


def burn_subtitles(video_path, srt_path, output_path=None, font_name="Noto Sans CJK SC", font_size=20):
    """Burn SRT subtitles into video."""
    video_dir = Path(video_path).parent
    if output_path is None:
        output_path = video_dir / "video_with_subs.mp4"

    # ffmpeg subtitle filter requires escaped path on some systems
    srt_escaped = str(srt_path).replace("\\", "/").replace(":", "\\:")
    
    subtitle_style = (
        f"FontName={font_name},"
        f"FontSize={font_size},"
        f"PrimaryColour=&H00FFFFFF,"
        f"OutlineColour=&H00000000,"
        f"Outline=2,"
        f"MarginV=30"
    )

    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-vf", f"subtitles={srt_escaped}:force_style='{subtitle_style}'",
        "-c:v", "libx264", "-crf", "23",
        "-c:a", "copy",
        str(output_path),
    ]

    print("Burning subtitles into video...")
    print(f"Input: {video_path}")
    print(f"Subtitles: {srt_path}")
    print(f"Output: {output_path}")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)
    
    print(f"Done! Output saved to: {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Burn subtitles into video.")
    parser.add_argument("video", help="Path to video file")
    parser.add_argument("srt", help="Path to SRT subtitle file")
    parser.add_argument("--output", default=None, help="Output video path")
    parser.add_argument("--font-size", type=int, default=20, help="Subtitle font size")
    args = parser.parse_args()

    burn_subtitles(args.video, args.srt, args.output, font_size=args.font_size)