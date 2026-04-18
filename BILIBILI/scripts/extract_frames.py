#!/usr/bin/env python3
"""Auto-detect best cover frame from a video by analyzing visual appeal."""

import argparse
import os
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


def extract_multiple_frames(video_path, timestamps, output_dir):
    """Extract frames at multiple timestamps."""
    frames = []
    for i, ts in enumerate(timestamps):
        output_path = output_dir / f"frame_{i:02d}_at_{ts.replace(':', '-')}.jpg"
        cmd = [
            "ffmpeg", "-y", "-ss", ts,
            "-i", str(video_path),
            "-frames:v", "1", "-q:v", "2",
            str(output_path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0 and output_path.exists():
            frames.append(output_path)
            print(f"  Extracted frame at {ts}")
    return frames


def suggest_timestamps(duration, num_frames=6):
    """Suggest timestamps spread across the video, biased toward interesting moments."""
    # Skip first 5% (often intros) and last 5% (often outros)
    start = max(0.05 * duration, 2)
    end = min(0.95 * duration, duration - 2)
    
    timestamps = []
    for i in range(num_frames):
        frac = (i + 0.5) / num_frames
        t = start + frac * (end - start)
        mins = int(t) // 60
        secs = int(t) % 60
        timestamps.append(f"{mins:02d}:{secs:02d}")
    
    return timestamps


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract candidate cover frames from video.")
    parser.add_argument("video", help="Path to video file")
    parser.add_argument("--num", type=int, default=6, help="Number of frames to extract")
    args = parser.parse_args()

    video_path = Path(args.video)
    output_dir = video_path.parent

    print(f"Getting duration of {video_path.name}...")
    duration = get_video_duration(str(video_path))
    print(f"Duration: {duration:.1f}s")

    timestamps = suggest_timestamps(duration, args.num)
    print(f"\nExtracting {args.num} frames at: {', '.join(timestamps)}")
    
    frames = extract_multiple_frames(str(video_path), timestamps, output_dir)
    
    print(f"\nExtracted {len(frames)} frames. Review them and pick the best one for the cover.")
    print("Then run:")
    print(f"  python3 scripts/make_cover.py {video_path} --timestamp <chosen_timestamp>")