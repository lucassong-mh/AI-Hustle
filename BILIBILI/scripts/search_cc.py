#!/usr/bin/env python3
"""Search YouTube for CC-licensed videos and print top results."""

import subprocess
import sys
import json

def search_youtube(query, max_results=20):
    """Search YouTube with CC filter using yt-dlp."""
    cmd = [
        "yt-dlp",
        f"ytsearch{max_results}:{query}",
        "--filter", "creative_commons",
        "--print", "%(id)s\t%(title)s\t%(duration_string)s\t%(view_count)s\t%(channel)s\t%(license)s",
        "--flat-playlist",
        "--no-warnings",
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            print(f"Error: {result.stderr}", file=sys.stderr)
            return []
        
        videos = []
        for line in result.stdout.strip().split('\n'):
            if not line.strip():
                continue
            parts = line.split('\t')
            if len(parts) >= 4:
                videos.append({
                    'id': parts[0],
                    'title': parts[1],
                    'duration': parts[2],
                    'views': parts[3],
                    'channel': parts[4] if len(parts) > 4 else '',
                    'license': parts[5] if len(parts) > 5 else '',
                })
        return videos
    except subprocess.TimeoutExpired:
        print("Search timed out", file=sys.stderr)
        return []
    except FileNotFoundError:
        print("yt-dlp not found. Install with: brew install yt-dlp", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    import os
    os.environ.setdefault("http_proxy", "http://127.0.0.1:7897")
    os.environ.setdefault("https_proxy", "http://127.0.0.1:7897")
    
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "oddly satisfying"
    max_results = 20
    
    print(f"Searching: {query} (CC only)\n")
    videos = search_youtube(query, max_results)
    
    if not videos:
        print("No results found. Try a different search term.")
        sys.exit(0)
    
    for i, v in enumerate(videos, 1):
        views_str = f"{int(v['views']):,}" if v['views'] and v['views'] != 'NA' else "N/A"
        print(f"{i}. [{v['duration']}] {v['title']}")
        print(f"   Views: {views_str} | Channel: {v['channel']} | License: {v['license']}")
        print(f"   https://www.youtube.com/watch?v={v['id']}")
        print()