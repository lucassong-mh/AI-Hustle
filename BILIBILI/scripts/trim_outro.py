#!/usr/bin/env python3
"""Trim outro/subscribe segments from the end of a video."""

import argparse
import subprocess
import sys
from pathlib import Path


def get_video_duration(video_path):
    """Get video duration in seconds using ffprobe."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(video_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return float(result.stdout.strip())


def trim_video(video_path, end_seconds, output_path=None):
    """Trim video to end at end_seconds from the beginning."""
    video_dir = Path(video_path).parent
    if output_path is None:
        output_path = video_dir / "video_trimmed.mp4"

    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-t", str(end_seconds),
        "-c:v", "libx264",
        "-c:a", "aac",
        str(output_path),
    ]

    print(f"Trimming video: {video_path}")
    print(f"  Original duration: {get_video_duration(video_path):.1f}s")
    print(f"  Trimming to: {end_seconds:.1f}s")
    print(f"  Output: {output_path}")

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)

    print("Done!")
    return output_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Trim outro from end of video.")
    parser.add_argument("video", help="Path to video file")
    parser.add_argument("--end", type=float, required=True, help="End time in seconds (e.g. 95.5)")
    parser.add_argument("--output", default=None, help="Output path (default: video_trimmed.mp4 in same dir)")
    args = parser.parse_args()

    trim_video(args.video, args.end, args.output)