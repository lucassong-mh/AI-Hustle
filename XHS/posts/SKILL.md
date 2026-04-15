# Skill: Daily Xiaohongshu (XHS) Post

## Overview

Every time a Zhihu blog is published, create a corresponding Xiaohongshu post. The XHS post consists of two parts: a **图文卡片** (text card, ≤500 chars) and a **原文** (brief takeaway, 1-2 sentences). The whole thing should be copy-paste ready as plain text.

## Trigger

A Zhihu blog has just been written, or user says "发小红书" / "同步小红书" / "写XHS".

## Workflow

### Step 1 — Read the Zhihu Blog

Read the full Zhihu blog file. Understand the core argument, the most surprising data point, and the commentary/看法 section.

### Step 2 — Extract the Hook

Identify the single most striking, surprising, or provocative element from the blog. This becomes the opening line — it must grab attention in under 3 seconds of scrolling.

Good hooks:
- A shocking number ("只有10%的美国人对AI感到兴奋")
- A paradox ("用AI最多的人，怕AI最深")
- A contradiction ("封杀中国最狠的AI公司，创始人从百度起家")
- A provocative question ("AI进步的叙事，到底是谁的叙事？")

Bad hooks:
- Topic announcements ("今天的文章是关于…")
- Vague statements ("AI领域最近很热闹")
- Flat summaries ("斯坦福发布了一份报告")

### Step 3 — Write the Post

XHS posts consist of **two parts**: 图文字卡 (text card) and 原文 (takeaway).

#### Part 1: 图文字卡 — The text card (≤500 Chinese characters)

This is the main content that appears as a text-image card on XHS. Rules:

1. **Length**: ≤500 Chinese characters (strict hard limit)
2. **Structure**: 3-5 short paragraphs, each 1-3 sentences. Break between every 2-3 lines for readability on mobile. NEVER write a wall of text.
3. **Tone**: Conversational, punchy, opinionated. Like talking to a smart friend, not writing an essay. Use 呀/啊/吧 sparingly for natural flow but never sound cute.
4. **No section headers** — just line breaks. No `##`, no bold `**`, no emoji.
5. **No images** — XHS text cards don't embed images. Focus purely on content quality.
6. **Must include**: At least one concrete number or data point from the original blog.
7. **Must include**: A clear opinion or hot take. XHS rewards takes, not reports.
8. **Logical flow**: Every paragraph must connect to the next. Read aloud — if it sounds like a list of unrelated facts, rewrite it. The reader should feel pulled through from first line to last.
9. **AI-flavor avoidance** (same rules as Zhihu blog):
   - No "值得一提的是", "毋庸置疑", "总的来说"
   - No "首先…其次…最后…"
   - No unnecessary hedging
   - No robotic closings
   - No emoji decorated section headers

#### Part 2: 原文 — The brief takeaway (1-2 sentences)

A short, sharp closing that sits below the text card as a separate element. Rules:

1. **Length**: 1-2 sentences only. Maximum ~50 characters.
2. **Content**: A thought-provoking, unexpected angle. NOT a summary of the text card. It should feel like the last line of a movie — something that lingers.
3. **Tone**: Can be more philosophical, ironic, or deadpan than the text card. This is your mic drop moment.
4. **Must start with "原文："** on its own, followed by the text on the next line.

### Step 4 — Hashtags

End the entire post with 3-5 hashtags on a single line, separated by spaces:

```
#人工智能 #AI #科技资讯
```

### Step 5 — File Output

Write the XHS post to:

```
XHS/posts/{YYYY-MM-DD}-{slug}.md
```

- Use the **same date and slug** as the corresponding Zhihu blog for easy cross-referencing.
- Example: If Zhihu blog is `2026-04-14-斯坦福报告AI鸿沟.md`, XHS post is `2026-04-14-斯坦福报告AI鸿沟.md`

**File format:**

```markdown
[Tag] 缩短后的标题

（图文字卡内容，≤500字，分3-5段）

原文：
（一两句引人深思的话）

#人工智能 #AI #科技资讯
```

No markdown headers (`#`), no bold, no images, no HTML. Pure plain text that can be directly copy-pasted into the XHS app. The `[Tag]` in the title uses the same tag system as the Zhihu blog.

### Step 6 — Deliver

1. Confirm the file has been saved.
2. Show the user the final XHS post (so they can copy-paste into the app).
3. Check text card character count — must be ≤500.

## Quality Checklist

- [ ] Text card character count ≤500 (excluding title, 原文 line, and hashtags)
- [ ] 原文 is 1-2 sentences, ≤50 chars, and says something non-obvious
- [ ] Contains at least one concrete number or data point in text card
- [ ] Contains a clear opinion/hot take in text card
- [ ] 3-5 hashtags at the end
- [ ] No images, no markdown formatting — pure plain text
- [ ] Same date-slug as the corresponding Zhihu blog
- [ ] Tone is conversational and punchy, not essay-like
- [ ] No AI-flavor phrases or patterns
- [ ] Logical flow — each paragraph connects to the next, reader feels pulled through