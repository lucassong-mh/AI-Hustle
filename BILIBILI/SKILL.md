# Skill: Daily Bilibili Video Repost

## Overview

Each day, find one YouTube video that is funny, relaxing, absurd, or visually appealing, download it, generate Chinese subtitles (when needed), trim outro/subscribe segments, and produce everything needed for a Bilibili upload. The goal is **low effort, high entertainment** — content that helps people decompress after work.

## Prerequisites

```bash
brew install ffmpeg yt-dlp
pip3 install --break-system-packages pillow
```

Verify:
```bash
ffmpeg -version && yt-dlp --version
```

## Folder Structure

```
BILIBILI/
  SKILL.md                          # This skill file
  scripts/                           # Helper scripts
    search_cc.py                    # Search YouTube CC videos
    download_video.py                # Download video + subtitles
    vtt_to_srt.py                   # Convert VTT to SRT
    burn_subs.py                    # Burn subtitles into video
    make_cover.py                   # Generate cover with watermark
    extract_frames.py               # Extract candidate cover frames
    trim_outro.py                   # Trim subscribe/outro segments
  videos/
    2026-MM-DD-slug/
      video.mp4                     # Downloaded original video
      video_trimmed.mp4             # Trimmed video (outro removed)
      subtitle.srt                 # Chinese subtitle file (SRT format, optional)
      cover.jpg                    # Cover image with text overlay (optional)
      meta.md                      # B站标题、简介、标签
    candidates/
      candidates.md                # Unused video candidates pool
    log.md                          # Daily log of all produced videos
  youtube-watcher-1.0.0/           # Third-party tool (gitignored)
```

## Trigger

User says "找今天的视频" / "发B站" / "daily video" / or any request to produce today's Bilibili video content.

## Content Guidelines (What Kind of Videos)

Target videos that make people **relax, laugh, or go "???"**:

| Category | Description | Examples |
|----------|-------------|---------|
| 搞笑/沙雕 | Absurd humor, fails, prank compilations | 踩空、滑倒、动物沙雕 |
| 抽象/离谱 | Surreal content that makes no sense | 日本整蛊、泰国广告、AI翻车 |
| 解压/ASMR | Satisfying, calming, oddly pleasing | 切肥皂、收纳、修复、压力球 |
| 美女/颜值 | Visually appealing, regardless of content | 舞蹈、变装、日常vlog |
| 擦边/暧昧 | Suggestive but not explicit — tease, not show | yoga try-on、cosplay、淋浴挑战 |
| 温馨/治愈 | Animals, kindness, small happy moments | 猫狗、宝宝、善意瞬间 |
| 音乐/节奏 | Catchy beats, mashups, creative performances | 洗脑改编、乐器合奏 |

**Hard rules:**
- Prefer CC BY or CC BY-SA licensed videos (verified via YouTube filter). Small creators with no explicit license are also acceptable — risk is low and attribution is given.
- Duration: **30 seconds to 10 minutes** (shorter is better)
- No political, extremist, or genuinely harmful content
- No explicit/pornographic content (B站会封号)
- "擦边" means suggestive, NOT explicit. When in doubt, dial it back.

## Workflow

### Step 1 — Search & Select

Use yt-dlp to search YouTube, then let the user pick.

**Search keywords** (rotate through these, mix it up):
- English: `funny fails`, `satisfying`, `oddly satisfying`, `compilation funny`, `asmr relaxing`, `try on haul`, `yoga stretch`, `cute animals`, `abstract humor`, `creative`, `challenge funny`
- Japanese: `面白い`, `癒し`, `整骨`, `ASMR`
- Korean: `웃긴`, `만족`, `스트레스해소`

**Search command:**
```bash
export http_proxy="http://127.0.0.1:7897"
export https_proxy="http://127.0.0.1:7897"
yt-dlp "ytsearch20:oddly satisfying" --print "%(id)s|%(title)s|%(duration_string)s|%(view_count)s|%(channel)s" --flat-playlist --no-warnings 2>/dev/null
```

Also try the CC filter URL:
```
https://www.youtube.com/results?search_query=oddly+satisfying&sp=EgIwAQ%253D%253D
```

**Selection criteria (pick 5 candidates for user to choose):**
1. View count > 10,000 (the higher the better, but not a hard floor)
2. Duration 30s-10min
3. Content fits one of the categories above
4. Not a duplicate of previously downloaded videos (check `videos/` folder and `log.md`)

**For each candidate, present:**
- Title (original)
- View count, duration
- URL
- One-line Chinese description of what it is
- Category tag (搞笑/解压/抽象/美女/擦边/治愈/音乐)

Let the user pick one. Save unused candidates to `videos/candidates/candidates.md`.

### Step 2 — Download Video

```bash
export http_proxy="http://127.0.0.1:7897"
export https_proxy="http://127.0.0.1:7897"
mkdir -p "BILIBILI/videos/{date}-{slug}"
yt-dlp -f "bestvideo[height<=1080]+bestaudio/best[height<=1080]" \
  --merge-output-format mp4 \
  -o "BILIBILI/videos/{date}-{slug}/video.mp4" \
  "https://www.youtube.com/watch?v={VIDEO_ID}"
```

### Step 3 — Get Original Subtitles

```bash
cd "BILIBILI/videos/{date}-{slug}"
yt-dlp --write-subs --write-auto-subs --sub-lang "en,zh-Hans" \
  --skip-download -o "original" "https://www.youtube.com/watch?v={VIDEO_ID}"
```

If English subtitles exist, use them as the source for translation. If only Chinese auto-subs exist, use those after cleanup. If neither exists, check if the video has spoken dialogue:
- **No dialogue (silent animation, ASMR, satisfying content)** → Skip subtitles, proceed without. Note in `meta.md`.
- **Has dialogue** → Subtitles are mandatory. If no subs available, consider picking another video.

### Step 4 — Produce Chinese Subtitles (SRT)

**Subtitle decision logic:**
- **Silent/visual-only videos** (no dialogue, pure visuals): No subtitles needed. Skip this step entirely.
- **Videos with foreign language dialogue**: Chinese subtitles are **mandatory**. Translate from English subs or create from scratch.

When producing subtitles:

1. **Read the original subtitle file** (`.vtt` or `.srt`), or if none exists, read the video description and transcript via `get_transcript.py`
2. **Translate to Chinese**:
   - Keep sentences natural and conversational
   - Preserve humor — adapt jokes, don't literal-translate them
   - For on-screen text/signs that need explaining, add `（注：xxx）`
   - For slang/idioms, use the closest Chinese equivalent
   - Each subtitle line: **≤18 Chinese characters** (for mobile readability)
   - If one English line is too long, split into multiple SRT entries
   - **CRITICAL: Timestamps must be strictly accurate.** Each subtitle entry's start and end time must precisely match when the words are spoken. Misaligned subtitles are worse than no subtitles. Use the original subtitles' timestamps as the source of truth. If adjusting, verify timing matches the actual speech.
3. **Generate SRT file** with proper timestamps
4. **Save as** `subtitle.srt` in the video folder

### Step 5 — Trim Outro/Subscribe Segments

Many YouTube videos end with a "Subscribe", "Like and Subscribe", channel logo, or YouTube-specific outro screen. These look out of place on Bilibili.

**Detection:**
- Watch the last 10-15 seconds of the video description for phrases like "subscribe", "like", "comment", channel cards, end screens
- Check if the video has an endscreen overlay (yt-dlp `--dump-json` shows `"annotations"` or similar)
- If the last 3-15 seconds are clearly a subscribe/outro segment, trim it

**Trim command:**
```bash
ffmpeg -i video.mp4 -t {trim_to_seconds} -c:v libx264 -c:a aac video_trimmed.mp4
```

Save as `video_trimmed.mp4`. The trimmed version is the one to upload to Bilibili. Keep the original `video.mp4` for reference.

If the video has no subscribe/outro segment, skip trimming and use the original video directly.

### Step 6 — Cover Image (Optional)

Cover images are **optional**. Bilibili can auto-select a frame from the video. Only create a cover when there's a compelling reason:

- The video has a particularly striking visual that needs text overlay for context
- You want to add a short punchy text phrase to make the thumbnail more clickable

**When creating a cover:**
- Extract a frame using `ffmpeg` or `extract_frames.py`
- Add **short, punchy text** (2-6 Chinese characters maximum) using `make_cover.py`
- Text should be a hook, not a description: "笑死", "离谱", "打工人看", "解压"
- The `AI字幕` badge is optional — only add if the video has Chinese subtitles

**When NOT to create a cover:**
- The video thumbnail is already clear and interesting
- No text would add value
- B站 auto-frame is good enough

**To preview frames and pick the best one:**
```bash
python3 BILIBILI/scripts/extract_frames.py BILIBILI/videos/{date}-{slug}/video.mp4 --num 8
# Then review the extracted frames and choose one
python3 BILIBILI/scripts/make_cover.py BILIBILI/videos/{date}-{slug}/video.mp4 --timestamp {chosen_time} --badge "AI字幕"
```

### Step 7 — Generate Bilibili Upload Metadata

Create `meta.md` in the video folder with everything needed for Bilibili upload:

```markdown
# 视频信息

- **原始链接**: {YouTube URL}
- **原始标题**: {original title}
- **频道**: {channel name}
- **时长**: {duration}
- **播放量**: {view count}
- **CC协议**: {license type}
- **描述**: {original description snippet}

## B站标题

以下3-5个候选标题，供挑选：

1. {title 1}
2. {title 2}
3. {title 3}
4. {title 4}
5. {title 5}

### 标题要求
- ≤40个中文字符
- 必须是hook而非描述：提问、反差、悬念、引诱点击
- B站风格：网友、竟然、离谱、笑死、打工人
- 好标题示例："程序员终于下班去滑板了，然后……"
- 坏标题示例："搞笑动画短片搬运第5期"

## B站简介

{2-3句有趣、口语化的描述}
{一句话总结/吐槽}

原视频：{original title} by {channel name}
来源：{YouTube URL}

## B站标签

每行一个标签，直接复制粘贴到B站（回车分隔）：

{tag1}
{tag2}
{tag3}
...
(10个以内)

## 封面

{有/无} | {如有：说明文字内容，如无：说明原因}

## 分区

- 主分区: {分区名}
- 子分区: {子分区名}

## 裁剪

{是否裁剪了结尾} | {如有：原始时长 → 裁剪后时长}
```

### Step 8 — Deliver

Present the user with a consolidated summary:
1. **3-5 candidate B站 titles** (let them pick)
2. **Cover image** (if generated) or note that B站 auto-frame is fine
3. **Subtitle status** (has subs / no subs needed / no subs available)
4. **Tags** (ready to copy-paste, one per line)
5. **Video description** (ready to copy-paste)
6. **Trim info** (whether outro was cut, original vs trimmed duration)
7. **Partition suggestion** (B站分区)

User uploads to Bilibili manually — I handle all the preparation, they do the final click.

## Daily Log

After each video is produced, append to `BILIBILI/videos/log.md`:

```markdown
### {date} — {slug}
- 视频: {title}
- 来源: {YouTube URL}
- 频道: {channel}
- CC协议: {license type}
- 分类: {category}
- B站标题: {chosen title}
- 裁剪: {是否裁剪结尾}
- 字幕: {有/无}
- 状态: 待上传 / 已上传
```

## Candidate Pool

Unused candidates from Step 1 are saved to `BILIBILI/videos/candidates/candidates.md`, format:

```markdown
### N. Video Title (Channel)

- **原文链接**: {YouTube URL}
- **类别**: {category}
- **时长**: {duration}
- **播放量**: {view count}
- **热度**: ⭐评分 (1-5)
- **适合B站原因**: 一句话说明
- **状态**: 未使用 / 已使用 (日期)
```

## Important Notes

1. **Proxy**: YouTube downloads always require:
   ```bash
   export http_proxy="http://127.0.0.1:7897"
   export https_proxy="http://127.0.0.1:7897"
   ```

2. **CC License verification**: Prefer CC BY/CC BY-SA videos. Small creators without explicit license are acceptable — always credit them in the B站简介.

3. **Attribution**: Always include original channel name and video URL in the B站简介.

4. **Subtitle quality**: When producing subtitles, **timestamps must be strictly accurate**. Misaligned subtitles are unacceptable. Use original timestamps as reference. If you can't get accurate timing, explain to the user and let them decide.

5. **Outro trimming**: Always check the end of videos for YouTube-specific subscribe/outro segments. Trim them when found. The trimmed video (`video_trimmed.mp4`) is what gets uploaded to Bilibili.

6. **File size**: Keep videos under 4GB (Bilibili upload limit). For most short videos this is not an issue.

7. **Cover images are optional**: Only create when they add clear value. B站 auto-frame is often fine.

8. **Tags format**: One tag per line, ready for the user to copy-paste into B站's tag input (B站 uses Enter to add each tag).