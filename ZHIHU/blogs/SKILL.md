# Skill: Daily Zhihu AI News Blog

## Overview

Each day, produce one Zhihu-ready blog post based on a hot AI news article. The entire output is in Chinese only—no English original text. The result is saved as a Markdown file under `ZHIHU/blogs/`.

## Folder Structure

```
ZHIHU/
  blogs/
    SKILL.md              # This skill file
    2026-04-14-xxx.md     # Blog posts
    candidates/
      candidates.md       # Candidate articles not yet used
  requirements/           # Original requirement notes
  answers/                # Other content
```

## Trigger

User says anything like "写今天的知乎博客" / "daily blog" / "发知乎" / or simply provides a news URL.

## Workflow

### Step 1 — Source Selection

1. **If the user provides a URL**, use it directly. Skip to Step 2.
2. **If no URL is provided**, check `ZHIHU/blogs/candidates/candidates.md` first for unused entries. If the user says "从候选库选" / "用候补的", present available options.
3. **If no candidate is chosen**, search the following sources for today's hottest AI news, prioritizing in this order:

| Priority | Source | URL Pattern |
|----------|--------|-------------|
| 1 | OpenAI Blog | `https://openai.com/blog` |
| 2 | Google AI Blog | `https://blog.google/technology/ai/` |
| 3 | Anthropic News | `https://www.anthropic.com/news` |
| 4 | The Verge AI | `https://www.theverge.com/ai-artificial-intelligence` |
| 5 | TechCrunch AI | `https://techcrunch.com/category/artificial-intelligence/` |
| 6 | Hugging Face Blog | `https://huggingface.co/blog` |
| 7 | MIT Tech Review | `https://www.technologyreview.com/topic/artificial-intelligence/` |
| 8 | VentureBeat AI | `https://venturebeat.com/category/ai/` |
| 9 | Wired AI | `https://www.wired.com/tag/artificial-intelligence/` |
| 10 | arXiv cs.AI | `https://arxiv.org/list/cs.ai/new` |

   - Use `webfetch` to fetch 2–3 candidate pages.
   - Present the top 2–3 articles (title + one-line summary) to the user and let them pick one.
   - If the user doesn't pick, default to the highest-ranked article.
   - **Save 2–3 unused articles to `ZHIHU/blogs/candidates/candidates.md`** for future use.

### Step 2 — Content Extraction

- Use `webfetch` to retrieve the full article. If needed, fetch supplementary sources for richer context.
- Extract: title, author/date, body text, and **all image URLs** (preserve original image links).
- If the article is paywalled or incomplete, try alternative sources or notify the user.
- **Network note**: If `webfetch` fails to access a URL (403, timeout, connection refused, etc.), the user has a VPN proxy configured. Try setting environment variables before retrying:
  ```
  export http_proxy="http://127.0.0.1:7897"
  export https_proxy="http://127.0.0.1:7897"
  ```
  These match the proxy settings in `~/.zshrc`. After setting them, retry the `webfetch`.

### Step 3 — Translation

Translate the entire article into Chinese following these principles:

0. **Creative freedom** — You are NOT a translation machine. You are a tech columnist writing for Zhihu. Feel free to:
   - Restructure, merge, and reorder content for better flow and impact
   - Add context, background, and connections the original article doesn't mention (but mark them as your own commentary in the 评论 section)
   - Omit boring or irrelevant parts of the original
   - Use a mix of sources — when the original article is thin, supplement with information from other sources you fetch
   - Write a narrative, not a faithful translation. The goal is 抓人眼球 (eye-catching), not 忠实还原 (faithful reproduction)
   - You do NOT need to cite the original source verbatim. References go in the subtle section between main text and commentary. In the body, just write naturally as if you are the author.
   - When combining multiple sources, synthesize them into a single coherent story rather than presenting "Source A says X, Source B says Y"

1. **Accuracy first** — no distorting facts, numbers, names, or technical claims.
2. **Natural flow** — read like a Chinese tech columnist wrote it, not like machine translation. Vary sentence length. Use Chinese idioms / 四字词语 where fitting.
3. **AI-flavor avoidance**:
   - No 过渡句 filler like "值得一提的是", "毋庸置疑", "总的来说".
   - No 列举式过渡 like "首先…其次…最后…".
   - No unnecessary hedging ("在某种程度上", "可能也许大概").
   - Avoid over-polite or robotic closings.
   - **No emoji in section headers** (no 💡, 📊, 🔥 etc. — readers can smell AI from a mile away).
   - **No preachy or condescending tone** — you are a peer discussing, not a teacher lecturing. Avoid "应该认识到", "我们必须", "不可否认的是", "很显然". Don't tell the reader what to think. Share observations, raise questions, offer perspectives — but always as one curious person talking to another.
   - **No excessive questioning** — one rhetorical question per article at most. Too many "?" reads as sensationalist, not thoughtful. Prefer declarative sentences that make the reader think, rather than questions that tell them what to think about.
   - **地道的理工男语气** — calm, precise, understated. Not loud, not sensational. State things plainly, let the irony or insight speak for itself. Think "闲聊中发现了一个有意思的角度", not "大家注意了！这件事的真相竟然是！".
4. **Terminology**:
   - Keep widely-known English terms (GPT, LLM, RAG, Agent, etc.) as-is.
   - **Do NOT translate domain-specific terms into forced Chinese equivalents.** Keep the original English term if it is the common way practitioners refer to it. Examples:
     - skill → skill (NOT "技能")
     - benchmark → benchmark (NOT "基准测试" unless explaining to a lay audience)
     - token → token (NOT "令牌")
     - agent → Agent (NOT "智能体" unless the context demands it)
     - effort level → effort level (NOT "努力级别")
     - CVE → CVE (NOT "通用漏洞披露")
     - OAuth → OAuth (NOT "开放授权")
     - run rate → run rate (NOT "运行速率")
     - fine-tune → fine-tune (NOT "微调")
   - For truly niche terms that most Chinese readers won't know, provide Chinese translation with English in parentheses on first use, then stick to English thereafter.
   - **Avoid obscure acronyms** in titles/tags. If a tag references a concept like AGI, use the Chinese equivalent (通用智能) or a more accessible phrase.
5. **Images**: Insert each image **at its natural position** in the text (right after the paragraph it relates to), NOT grouped at the end. Use original URLs; do not rehost.

6. **Cover image**: Every blog post MUST have a cover image immediately after the title line. This is distinct from in-text images.

### Step 4 — Cover Image

Every blog post must have a cover image placed immediately after the `# [Tag] Title` line, before any body text.

**Source priority:**
1. **Original article's hero image** — the best option. Always try to extract it from the source article first. The Verge, TechCrunch etc. usually have high-quality featured images.
2. **Product/brand official image** — if the article is about a specific product (e.g., a robot, an AI model launch, a GitHub project), find the official image from the product's website or social preview (OG image). Examples:
   - OpenClaw → `https://openclaw.ai/og-image.png`
   - Anthropic blog → `https://cdn.sanity.io/images/4zrzovbb/website/...` (from their blog page)
   - Unitree → `https://www.unitree.com/images/...` (from their product page)
   - GitHub repo → org avatar or repo social preview
3. **Relevant stock image** — only if options 1 and 2 fail. The image must be **thematically relevant** to the article — not just "tech" or "robot", but specifically matching the topic:
   - Corporate rivalry → split screen, competition imagery
   - Open source / code → code on screen, terminal
   - Security → lock, shield, network visualization
   - Social impact → crowd, data visualization, charts
4. **NEVER reuse the same generic Unsplash image across multiple posts.** Each post should have a distinct, relevant cover. If you catch yourself using `photo-1635070041078-e363dbe005cb` or `photo-1677442136019-21780ecad95` again, stop and find something specific.
5. **Verify every image URL** — always `curl -s -o /dev/null -w "%{http_code}" "<url>"` to confirm HTTP 200 before using it. Never use a 404 image.
6. If no relevant image is available after searching, leave a placeholder note for the user.

**Format in the markdown file:**

```markdown
# [Tag] 翻译后的标题

![封面](图片URL)

（正文开始）
```

### Step 5 — Commentary

After the translated body + references, add a commentary section separated by `---`.

**Format:**

```markdown
---

（评论内容，直接开始写，无标题、无emoji、无小标题）
```

Requirements for this section:

- **Length**: 150–300 characters (简短有力).
- **Style**: Sharp, opinionated, thought-provoking. Like a seasoned tech columnist, not a ChatGPT summary.
- **Content options** (pick one or combine):
  - Why this matters / what's the real implication behind the hype
  - A contrarian take that challenges the prevailing narrative
  - A connection to broader trends the average reader might miss
  - A practical "so what" for developers / entrepreneurs / ordinary people
- **Must NOT**:
  - Simply restate the article's conclusion
  - Be uniformly positive or generic praise
  - Use AI clichés ("让我们拭目以待", "这将改变一切")
  - Use emoji
  - Use a section header like "我的看法" or "编者按" — the divider alone is enough. The shift in tone marks the boundary.

### Step 6 — Title

Format:

```markdown
# [Tag] 原标题的中文翻译
```

The bracketed tag rotates. Pick one that fits the article's vibe. The tag should be punchy, varied, and avoid repetition across consecutive posts.

**Tag pool (pick or create new):**

| Tag | When to use |
|-----|-------------|
| 今天你AI了吗 | Default / daily routine |
| AI搞事情了 | Breaking news, major release |
| 这也能AI？ | Surprising / unexpected AI application |
| AI又卷了 | Competitive escalation, benchmark wars |
| 谁在焦虑 | Hype correction, public sentiment, reality check |
| 你的下一份工作 | Workforce / automation impact |
| 开源万岁 | Open-source related |
| 人类观察中 | Philosophical / societal angle |
| 别慌，还没AGI | Reality check on AGI hype |
| 谁在焦虑 | Public sentiment, anxiety, inequality |
| 技术债务 | When technical debt, bugs, or security flaws are the story |
| 碳基观察 | Human perspective on AI events (from 专栏 name) |
| 拔剑四顾 | Competitive landscape, rivalries, showdowns |
| 越封越火 | When bans/backlash backfire and make something stronger (OpenClaw after Anthropic ban, etc.) |
| 账本翻开 | Revenue, funding, business model, financial disputes |
| 底牌亮了 | Leaks, reveals, internal memos, source code exposed |
| 权力的游戏 | Corporate power plays, government vs tech, geopolitical angle |
| 谁的规则 | When the question is about who makes the rules |
| 江湖规矩 | Ethics, norms, industry standards, "unwritten rules" |
| 冷思考 | When everyone's hyping, it's time to think clearly |
| 一地鸡毛 | Messy aftermath, unintended consequences, things gone wrong |

**Tag rules**:
- Must be ≤7 characters.
- Must be in plain Chinese — no obscure acronyms, no recycled English.
- Feel free to create new tags on the fly as long as they are punchy and accessible.
- **Rotate tags** — do not reuse the same tag in consecutive posts. If you used [开源万岁] yesterday, use something else today even if the topic is also open-source related.
- The tag should add emotional color or a perspective, not just categorize. "碳基观察" is better than "AI新闻"; "账本翻开" is better than "商业新闻".
- **The tag must make sense at first glance** — the reader should immediately get what angle you're taking. "越封越火" is clear (bans backfire). "底牌亮了" is clear (a reveal). Avoid tags so abstract that the reader has to guess, like "暗流涌动" or "时代之问".

### Step 7 — References Placement

References (original article URL, supplementary sources) go **between the main text and the commentary**, in a subtle, unobtrusive format. Use `<small>` or italicized blockquote — something that doesn't compete with the content:

```markdown
---

*原文：[原文标题](原文URL) · 作者 / 日期 | 补充来源：[来源标题](URL) · 机构*

---

（评论内容）
```

Do NOT put references at the very top of the article. The article should open with content, not citations.

### Step 8 — File Output

Write the final Markdown file to:

```
ZHIHU/blogs/{YYYY-MM-DD}-{slug}.md
```

- `slug`: 2–4 Chinese characters or English lowercase words summarizing the title, e.g., `2026-04-14-斯坦福报告AI鸿沟.md`

**Full file structure must be:**

```markdown
# [Tag] 翻译后的标题

![封面](封面图片URL)

（翻译正文，含图片在自然位置）

---

*原文：[原文标题](原文URL) · 作者 / 日期 | 补充来源：...*

---

（评论内容，无标题无emoji，直接写）
```

### Step 9 — Deliver

1. Confirm the file has been saved.
2. Show the user the final title and a one-line preview of the commentary.

## Candidate Pool (候选库)

未被选中的热门文章保存在 `ZHIHU/blogs/candidates/candidates.md`，格式如下：

```markdown
### N. 文章标题

- **原文链接**: URL
- **补充来源**: 额外抓取到的关键信息摘要
- **热度**: ⭐评分 (1-5)
- **适合知乎原因**: 一句话说明
- **状态**: 未使用 / 已使用 (日期)
```

### When to use the Candidate Pool

- When the user says "从候选库选" / "用候补的" / provides no URL and no fresh news is compelling.
- Agent should read `ZHIHU/blogs/candidates/candidates.md`, present available options, and let the user choose.
- After an article is used, mark its status as `已使用 ({date})`.
- Each day's search may add 2–3 new candidates to the pool. Append, don't overwrite.

## Quality Checklist (self-verify before delivering)

- [ ] Translation reads like a human wrote it — not stiff, not "AI-flavored"
- [ ] Cover image present immediately after title line, thematically relevant (not just generic "tech" image)
- [ ] All image URLs verified as HTTP 200
- [ ] No emoji in section headers or commentary heading
- [ ] Creative freedom applied — restructured, synthesized, not just a line-by-line translation
- [ ] All images appear at their natural positions in the text (not grouped at the end)
- [ ] References placed between main text and commentary, in subtle/reduced format
- [ ] Technical terms handled per Terminology rules
- [ ] Commentary has no header — just a divider, then direct writing
- [ ] Commentary is 150–300 chars, says something non-obvious
- [ ] Title tag uses plain Chinese, no obscure acronyms
- [ ] Title follows the `[Tag] 翻译标题` format
- [ ] File saved to correct path with correct naming
- [ ] Unused candidate articles saved to `ZHIHU/blogs/candidates/candidates.md`