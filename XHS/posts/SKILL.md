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

#### Part 0: 标题 — ≤20 Chinese characters

Every XHS post must have a short, punchy title that summarizes the hook. Rules:

1. **Length**: ≤20 Chinese characters (strict hard limit)
2. **Style**: One sharp observation, contradiction, or punchline. Not a topic announcement.
3. Same tone rules as the body: no preachy language, no excessive questioning, 谦逊理工男 voice.
4. Stored as the first line of the file, before the `[Tag]` line.

Good examples:
- "Anthropic老板在百度干过一年，然后封杀了中国"
- "OpenAI说对手80亿收入是假的，但两种记账都合规"
- "6周8万star，但它97%还是TypeScript"

Bad examples:
- "今天聊聊Anthropic" (topic announcement)
- "AI行业到底怎么了？？？" (vague, too many question marks)
- "震惊！OpenAI内部备忘录曝光" (clickbait, 爹味)

#### Part 1: 图文字卡 — The text card (≤500 Chinese characters)

This is the main content that appears as a text-image card on XHS. Rules:

1. **Length**: ≤500 Chinese characters (strict hard limit)
2. **Structure**: 3-5 short paragraphs, each 1-3 sentences. Break between every 2-3 lines for readability on mobile. NEVER write a wall of text.
3. **Tone**: Conversational, punchy, opinionated. Like talking to a smart friend, not writing an essay. Use 呀/啊/吧 sparingly for natural flow but never sound cute. **No preachy tone** — you're a peer sharing thoughts, not a teacher telling people what to think. Avoid "应该认识到", "我们必须", "不可否认". Raise questions, share observations, offer angles — as one curious person to another. **No excessive questioning** — at most one "?" per post. Prefer declarative sentences. Think 谦逊理工男: calm, precise, understated. Let the irony or insight speak for itself.
4. **No section headers** — just line breaks. No `##`, no bold `**`, no emoji.
5. **No forced Chinese translations for domain terms** — same rule as Zhihu blog: skill stays skill, token stays token, benchmark stays benchmark, etc. XHS readers are tech-savvy enough.
5. **Optional cover image**: If there is a fitting image from the Zhihu blog (usually the cover), note it as a comment at the top of the file. The user can post it as the first image on XHS. This is optional — only include it when the image is visually striking and directly relevant.
6. **Must include**: At least one concrete number or data point from the original blog.
7. **Must include**: A clear opinion or hot take. XHS rewards takes, not reports.
8. **Logical flow**: Every paragraph must connect to the next. Read aloud — if it sounds like a list of unrelated facts, rewrite it. The reader should feel pulled through from first line to last.
9. **Engagement hooks** (learned from real XHS comments on the Anthropic post):
   - The most engaged comments come from **contradictions and ironies** — "创始人在百度干过一年然后封杀中国" got 54 likes, "盗了百度的广告技术吗" got 46 likes. Surface these contradictions prominently.
   - **Conversational zingers** work better than formal analysis — "百度核心功能没学到家，各种广告" beats "百度在AI领域的战略失误分析".
   - **"What about..." reversals** spark debate — when readers push back, that's the engagement. Write content that invites the reader to think "but wait..."
   - **Concrete scenes beat abstract statements** — "1600万次蒸馏攻击" beats "大规模未经授权使用".
10. **AI-flavor avoidance** (same rules as Zhihu blog):
    - No "值得一提的是", "毋庸置疑", "总的来说"
    - No "首先…其次…最后…"
    - No unnecessary hedging
    - No robotic closings
    - No emoji decorated section headers
    - No preachy or condescending tone — no "应该认识到", "我们必须", "不可否认". You're discussing with peers, not lecturing.

#### Part 2: 原文 — Brief takeaway + reference links

A short closing that provides either a sharp takeaway or useful reference links (or both). Rules:

1. **Length**: 1-3 lines. Maximum ~80 characters for the takeaway portion.
2. **Content options** (pick one or combine):
   - A thought-provoking, unexpected angle (mic drop style)
   - Key reference links (GitHub repo, original article, official source)
   - A one-liner + a link
3. **Tone**: Can be more philosophical, ironic, or deadpan than the text card.
4. **Must start with "原文："** on its own, followed by the content on the next line.
5. **Links**: Use plain URLs (not markdown links). XHS doesn't render markdown links well. Just paste the URL directly.

Example formats:

```
原文：
AI编程工具的下一轮洗牌，不比谁的模型聪明，比谁的运行时更轻。

原文：
GitHub: github.com/NousResearch/hermes-agent
6周8万star，自学习循环是关键差异。

原文：
OpenAI备忘录原文：theverge.com/xxxxx
300亿里80亿是会计手法，但两种记账方式都合规。
```

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
<!-- 封面图: https://...image-url... (optional, only when fitting) -->

标题≤20字

[Tag] 缩短后的标题

（图文字卡内容，≤500字，分3-5段）

原文：
（一两句引人深思的话 or 参考链接）

#人工智能 #AI #科技资讯
```

No markdown headers (`#`), no bold. The only HTML-style content is the optional `<!-- 封面图 -->` comment at the top, which the user can use to locate the image for posting as the first comment on XHS. Pure plain text for the body. The `[Tag]` in the title uses the same tag system as the Zhihu blog.

### Step 6 — Deliver

1. Confirm the file has been saved.
2. Show the user the final XHS post (so they can copy-paste into the app).
3. Check text card character count — must be ≤500.

## Quality Checklist

- [ ] Title ≤20 Chinese characters, punchy and specific
- [ ] Text card character count ≤500 (excluding title, [Tag] line, 原文 line, and hashtags)
- [ ] 原文 section is 1-3 lines, includes either a takeaway or reference links or both
- [ ] Links in 原文 are plain URLs, not markdown links
- [ ] Contains at least one concrete number or data point in text card
- [ ] Contains a clear opinion/hot take in text card
- [ ] 3-5 hashtags at the end
- [ ] Optional cover image noted in comment (only when visually striking and relevant)
- [ ] No markdown formatting in body — pure plain text
- [ ] Same date-slug as the corresponding Zhihu blog
- [ ] Tone is conversational and punchy, not essay-like
- [ ] No AI-flavor phrases or patterns
- [ ] Logical flow — each paragraph connects to the next, reader feels pulled through