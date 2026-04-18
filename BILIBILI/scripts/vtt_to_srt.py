#!/usr/bin/env python3
"""Convert YouTube VTT subtitles to clean SRT format."""

import re
import sys
from pathlib import Path


def vtt_to_srt(vtt_content):
    """Convert WebVTT content to SRT format."""
    lines = vtt_content.split('\n')
    srt_entries = []
    current_text = []
    start_time = ""
    end_time = ""
    in_cue = False
    index = 1

    for line in lines:
        line = line.strip()
        
        # Skip headers and metadata
        if line in ('WEBVTT', '') or line.startswith('NOTE') or line.startswith('STYLE'):
            continue
        
        # Match timestamp line
        ts_match = re.match(r'(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}\.\d{3})', line)
        if not ts_match:
            ts_match = re.match(r'(\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}\.\d{3})', line)
        
        if ts_match:
            # Save previous cue if any
            if current_text and start_time:
                text = ' '.join(current_text)
                # Remove duplicate lines
                text = re.sub(r'<[^>]+>', '', text)
                if text.strip():
                    srt_entries.append(f"{index}\n{start_time} --> {end_time}\n{text.strip()}\n")
                    index += 1
            current_text = []
            start_time = convert_timestamp(ts_match.group(1))
            end_time = convert_timestamp(ts_match.group(2))
            in_cue = True
            continue
        
        if in_cue and line and not line.isdigit():
            # Avoid consecutive duplicates
            if not current_text or line != current_text[-1]:
                current_text.append(line)

    # Don't forget the last cue
    if current_text and start_time:
        text = ' '.join(current_text)
        text = re.sub(r'<[^>]+>', '', text)
        if text.strip():
            srt_entries.append(f"{index}\n{start_time} --> {end_time}\n{text.strip()}\n")

    return '\n'.join(srt_entries)


def convert_timestamp(vtt_ts):
    """Convert VTT timestamp (HH:MM:SS.mmm or MM:SS.mmm) to SRT format (HH:MM:SS,mmm)."""
    # Handle both HH:MM:SS.mmm and MM:SS.mmm formats
    parts = vtt_ts.split(':')
    if len(parts) == 2:
        # MM:SS.mmm -> 00:MM:SS,mmm
        seconds_ms = parts[1].replace('.', ',')
        return f"00:{parts[0]}:{seconds_ms}"
    else:
        # HH:MM:SS.mmm -> HH:MM:SS,mmm
        return vtt_ts.replace('.', ',')


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 vtt_to_srt.py <input.vtt> [output.srt]")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else input_path.with_suffix('.srt')

    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    content = input_path.read_text(encoding='utf-8')
    srt_content = vtt_to_srt(content)
    output_path.write_text(srt_content, encoding='utf-8')
    print(f"SRT saved to: {output_path}")
    print(f"Total entries: {srt_content.count(chr(10) + str(1))}")


if __name__ == "__main__":
    main()