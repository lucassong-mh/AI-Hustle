# AI-Hustle

This project manages automated content creation for Chinese social media platforms, producing daily AI news blog posts and derivative short-form content.

## Project Structure

```
AI-Hustle/
  CLAUDE.md                  # This file — project context for AI agents
  ZHIHU/                     # Zhihu (知乎) content
    专栏.md                    # Column metadata (name, description, cover, topic tags)
    blogs/
      SKILL.md                # Skill/workflow rules for Zhihu blog production
      2026-MM-DD-slug.md      # Published blog posts
      candidates/
        candidates.md          # Unused article candidates pool
    answers/                  # Zhihu answer content
      SKILL.md                # Skill for Zhihu answers
    requirements/             # Original requirement docs
  XHS/                       # Xiaohongshu (小红书) content
    posts/
      SKILL.md                # Skill/workflow rules for XHS post production
      2026-MM-DD-slug.md      # Published XHS posts (≤500 chars, derived from Zhihu blogs)
```

## Content Pipeline

1. **Source** — Find hot AI news from major outlets (The Verge, TechCrunch, Anthropic blog, etc.)
2. **Zhihu blog** — Full-length Chinese article with translation, commentary, and cover image
3. **XHS post** — ≤500 char excerpt derived from the Zhihu blog, written in Xiaohongshu style

## Key Rules

- All content is in Chinese. Keep widely-known English terms (GPT, LLM, RAG, Agent) as-is.
- Each Zhihu blog follows the format defined in `ZHIHU/blogs/SKILL.md`
- Each XHS post follows the format defined in `XHS/posts/SKILL.md`
- Blog file naming: `YYYY-MM-DD-中文slug.md`
- Candidate articles are stored in `ZHIHU/blogs/candidates/candidates.md`
- When reading a Zhihu blog to create an XHS post, read the full blog first, then condense per the XHS skill rules