#!/bin/env python3
"""Download a YouTube video with subtitles, prepare for Bilibili upload."""

import argparse
import os
import subprocess
import sys
from pathlib import Path

BILIBILI_DIR = Path(__file__).parent.parent / "videos"


def download_video(video_id, date_slug, proxy="http://127.0.0.1:7897"):
    """Download video and subtitles from YouTube."""
    output_dir = BILIBILI_DIR / date_slug
    output_dir.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    if proxy:
        env["http_proxy"] = proxy
        env["https_proxy"] = proxy

    url = f"https://www.youtube.com/watch?v={video_id}"

    # Download video
    print(f"Downloading video: {url}")
    cmd_video = [
        "yt-dlp",
        "-f", "bestvideo[height<=1080]+bestaudio/best[height<=1080]",
        "-o", str(output_dir / "video.mp4"),
        "--merge-output-format", "mp4",
        url,
    ]
    subprocess.run(cmd_video, env=env, check=True)

    # Download subtitles
    print("Downloading subtitles...")
    cmd_subs = [
        "yt-dlp",
        "--write-subs", "--write-auto-subs",
        "--sub-lang", "en,zh-Hans",
        "--skip-download",
        "-o", str(output_dir / "original"),
        url,
    ]
    result = subprocess.run(cmd_subs, env=env, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Subtitle download warning: {result.stderr}")

    # Check what we got
    subtitle_files = list(output_dir.glob("original*.vtt")) + list(output_dir.glob("original*.srt"))
    if subtitle_files:
        print(f"Found {len(subtitle_files)} subtitle file(s)")
        for f in subtitle_files:
            print(f"  - {f.name}")
    else:
        print("No subtitles found. Video may not have any available.")

    print(f"\nAll files saved to: {output_dir}")
    return output_dir


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download YouTube video for Bilibili upload.")
    parser.add_argument("video_id", help="YouTube video ID (e.g., dQw4w9WgXcQ)")
    parser.add_argument("--date-slug", required=True, help="Date and slug for folder name (e.g., 2026-04-17-funny-cat)")
    parser.add_argument("--proxy", default="http://127.0.0.1:7897", help="Proxy URL")
    args = parser.parse_args()

    download_video(args.video_id, args.date_slug, args.proxy)