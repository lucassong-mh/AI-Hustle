# Skill: 小红书时尚内容生产

## Overview

从国内外时尚源抓取热门时尚内容（时装周、明星穿搭、潮流趋势、品牌新品等），整理成可直接发布的小红书帖子。输出两种格式：**图文帖**和**视频帖**。我们是信息汇总者，不是创造者——用户只做最终review和发布。

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
XHS/FASHION/
  SKILL.md                        # This skill file
  candidates/
    candidates.md                  # 候选内容池
  posts/
    2026-MM-DD-slug/
      meta.md                     # 帖子文案（标题、正文、单品清单、标签）
      images/                     # 下载的图片（图文帖）
        01.jpg
        02.jpg
        ...
      video.mp4                   # 下载的视频（视频帖，如适用）
```

## Trigger

User says "找时尚内容" / "找今天的穿搭" / "发小红书时尚" / "时尚帖" / "fashion post" / or provides a fashion URL.

## Content Types

| 类型 | 说明 | 优先级 |
|------|------|--------|
| 明星/名人穿搭 | 机场、街拍、红毯、日常穿搭拆解 | 高 |
| 时装周/大秀 | 品牌发布会、秀场造型、后台花絮 | 高 |
| 潮流趋势 | 当季流行趋势、搭配公式、风格解析 | 中 |
| 品牌新品 | 新品发布、联名系列、限量款 | 中 |
| 街头风格 | 街拍、素人穿搭、风格混搭 | 中 |

男女皆可，不限风格（街头、奢侈、极简、复古、高街等）。

## Source Priority

### 国际源

| 优先级 | 来源 | URL | 类型 |
|--------|------|-----|------|
| 1 | Vogue Runway | `https://www.vogue.com/fashion-shows` | 时装周 |
| 2 | Vogue | `https://www.vogue.com` | 综合 |
| 3 | GQ | `https://www.gq.com` | 男装/综合 |
| 4 | Harper's Bazaar | `https://www.harpersbazaar.com` | 女装 |
| 5 | Hypebeast | `https://hypebeast.com` | 街头/潮流 |
| 6 | Highsnobiety | `https://www.highsnobiety.com` | 潮流/奢侈 |
| 7 | WWD | `https://wwd.com` | 行业新闻 |
| 8 | BOF | `https://www.businessoffashion.com` | 行业分析 |
| 9 | Elle | `https://www.elle.com` | 女装/趋势 |
| 10 | W Magazine | `https://www.wmagazine.com` | 高级时装 |

### 国内源

| 优先级 | 来源 | URL | 类型 |
|--------|------|-----|------|
| 11 | VOGUE中国 | `https://www.vogue.com.cn` | 综合 |
| 12 | GQ中国 | `https://www.gq.com.cn` | 男装/综合 |
| 13 | ELLE中国 | `https://www.ellechina.com` | 女装/趋势 |
| 14 | NOWRE | `https://nowre.com` | 街头/球鞋 |
| 15 | HYPEBEAST中文 | `https://hypebeast.cn` | 街头/潮流 |

### 视频源（YouTube时装周/品牌频道）

| 来源 | Channel URL | 用途 |
|------|-------------|------|
| Vogue YouTube | `https://www.youtube.com/@Vogue` | 大秀视频、后台 |
|品牌官方频道 | 各品牌YouTube | 发布会、Campaign |

**注意：不以小红书作为内容源**（我们要发的地方，不能抄同平台内容）。

## Workflow

### Step 1 — Source Selection

1. **If the user provides a URL**, use it directly. Skip to Step 2.
2. **If no URL is provided**, check `XHS/FASHION/candidates/candidates.md` first for unused entries. If the user says "从候选库选", present available options.
3. **If no candidate is chosen**, search sources for today's hottest fashion content:
   - Use `webfetch` to fetch 2-3 candidate pages from the source priority list.
   - Focus on content that is: newsworthy (时装周、大秀), trending (明星同款出圈), or practical (穿搭公式、单品推荐).
   - Present the top 3-5 articles/events to the user with: title, source, one-line Chinese summary, thumbnail description.
   - Let the user pick one.
   - **Save unused candidates to `XHS/FASHION/candidates/candidates.md`** for future use.
4. **Network note**: If `webfetch` fails to access a URL (403, timeout, etc.), the user has a VPN proxy configured. Try setting environment variables before retrying:
   ```
   export http_proxy="http://127.0.0.1:7897"
   export https_proxy="http://127.0.0.1:7897"
   ```

### Step 2 — Content Extraction

Use `webfetch` to retrieve the full article/page. Extract:
- **Title**: Original headline
- **Images**: All high-quality image URLs (优先选大图、横版封面图、全身造型图)
- **Video**: If the source contains video (runway show, campaign video, etc.), note the video URL for yt-dlp download
- **Key items/outfits**: Identify every visible fashion item (clothing, shoes, bags, accessories, jewelry)
- **Brand/names**: Brand name for each item
- **Price**: Approximate price range in CNY (search brand official site or major retailers if needed; if unavailable, give rough estimate based on brand tier)
- **Context**: Event, season, theme, stylist credit, etc.

**Selection criteria for images:**
- Cover/hero image first
- Full outfit shots (全身照)
- Detail shots of key items (特写照)
- Behind-the-scenes if available
- Aim for 5-9 images for a 图文帖, flexible based on content quality
- Skip: pure text graphics, ads, irrelevant filler images

### Step 3 — Determine Output Format

Based on the content type, decide the format:

| Source content type | Output format | When |
|---------------------|---------------|------|
| 时装周大秀完整视频 | 视频帖 | 有完整runway video可用 |
| 品牌Campaign视频 | 视频帖 | 有高质量品牌视频 |
| 明星穿搭图文 | 图文帖 | 静态图片为主 |
| 潮流趋势/单品推荐 | 图文帖 | 静态图片+文字解析 |
| 街拍/lookbook | 图文帖 | 多张look图片 |

If the source has both great images AND video, produce **both formats** and let the user choose.

### Step 4 — Download Media

#### 图文帖：下载图片

```bash
mkdir -p "XHS/FASHION/posts/{date}-{slug}/images"
curl -s -o "XHS/FASHION/posts/{date}-{slug}/images/01.jpg" "{image_url_1}"
curl -s -o "XHS/FASHION/posts/{date}-{slug}/images/02.jpg" "{image_url_2}"
# ... repeat for all selected images
```

Rename images in sequence (01.jpg, 02.jpg, ...) in the order they should appear on XHS:
1. 封面图（最抢眼的全景/造型照）
2. 全身look照
3. 单品细节照
4. 补充照

Verify all images downloaded correctly:
```bash
ls -la "XHS/FASHION/posts/{date}-{slug}/images/"
file "XHS/FASHION/posts/{date}-{slug}/images/"*
```

#### 视频帖：下载视频

```bash
export http_proxy="http://127.0.0.1:7897"
export https_proxy="http://127.0.0.1:7897"
mkdir -p "XHS/FASHION/posts/{date}-{slug}"
yt-dlp -f "bestvideo[height<=1080]+bestaudio/best[height<=1080]" \
  --merge-output-format mp4 \
  -o "XHS/FASHION/posts/{date}-{slug}/video.mp4" \
  "{video_url}"
```

If video is from a web page (not YouTube), try:
```bash
yt-dlp -o "XHS/FASHION/posts/{date}-{slug}/video.mp4" "{page_url}"
```

For runway show videos on YouTube, also download a few key frames as potential cover images:
```bash
ffmpeg -i "XHS/FASHION/posts/{date}-{slug}/video.mp4" \
  -vf "select=eq(n\,0)+eq(n\,30)+eq(n\,60)+eq(n\,90)" \
  -vsync vfr \
  "XHS/FASHION/posts/{date}-{slug}/images/frame_%02d.jpg"
```

If video download fails, inform the user and fall back to 图文帖 format using whatever images are available.

### Step 5 — Product Research (单品调研)

For each identifiable item in the content, research:

1. **Brand name** (中英文)
2. **Item name** (如具体款名)
3. **Approximate price range** in CNY
4. **Product link** (品牌官网或主流电商，optional，能找到就加)

Price estimate tiers:
- 奢侈品牌 (LV, Dior, Chanel, etc.) → ¥10,000+
- 轻奢品牌 (Celine, Loewe, Bottega Veneta, etc.) → ¥3,000-¥30,000+
- 大众品牌 (Zara, H&M, Uniqlo, etc.) → ¥100-¥2,000
- 潮牌 (Supreme, Stüssy, Noah, etc.) → ¥500-¥5,000
- 球鞋 → 具体查，差异很大

If the exact item cannot be identified, provide the brand and a similar/representative item with price range.

### Step 6 — Write Post Copy (写文案)

The post copy must follow 小红书发布格式。所有内容合并为一段**可直接复制粘贴**的纯文本，无需额外格式化。

#### Title — ≤20 Chinese characters

Punchy, specific, hook-driven. Must make people stop scrolling.

Good examples:
- "Stella McCartney×H&M联名¥99起"
- "Bella同款水晶裤只要¥169"
- "今年秋冬最值得入手的5件单品"
- "Dior大秀这次又搞了什么"

Bad examples:
- "今天的穿搭分享" (无聊)
- "时尚资讯速递" (太泛)
- "震惊！这个品牌竟然……" (小红书已经看腻了)

#### Body Text — ≤1000 Chinese characters（含图片叙述、商品叙述、背景、标签，一气呵成）

这是**直接复制到小红书正文的完整文案**，包含所有内容。结构如下：

1. **图片叙述**：告诉读者每张图是什么（因为图片上无法叠加文字标注）
2. **背景/故事**：内容的背景和亮点
3. **单品清单**：每件商品的品牌、名称、价格
4. **标签**：5-8个话题标签

Rules:
1. **Hook first**: 开头用最抓眼球的元素（名人名字、具体单品、价格反差）
2. **Conversational tone**: 像跟懂时尚的朋友聊天，不是写论文
3. **Specific over vague**: "Chanel经典菱格纹小牛皮"比"一款名牌包"好；"全套不到¥2000"比"很划算"好
4. **Price as hook**: 当某件看起来很贵但其实不贵（或反之），直接点出来
5. **图片叙述格式**：用「图1/图2/...」标注每张图的内容，让读者对照看
6. **单品清单融入正文**：用emoji做分类前缀，品牌名+单品名+价格区间
7. **No AI flavor**: No "值得一提的是", "总的来说", "毋庸置疑". No preachy tone.
8. **Keep English terms**: Don't force-translate widely-known terms (Vintage, OOTD, Lookbook, Chic, etc.)
9. **标签在末尾**: #标签1 #标签2 ... 5-8个

**正文模板：**

```
图1: xxx
图2: xxx
图3: xxx
...

（背景故事+亮点+个人看法，200-400字）

单品清单：
🧥 xxx ｜ Chanel ｜约¥35,000-¥45,000
👖 xxx ｜ Levi's ｜约¥700-¥900
...

#标签1 #标签2 #标签3 ...
```

**单品清单格式规则：**
- Use emoji as item category prefix for visual scanning
- Brand name in English (or original language)
- Price in CNY, use 约with a range (约¥X-¥Y)
- If exact item can't be found, note (参考款) and give similar item
- If price truly unknown, write (待查)
- Order: top/bottom/shoes/bags/accessories

**Tag rules:**
- Always include one broad tag (#时尚穿搭, #穿搭灵感, #潮流趋势)
- Always include brand-specific tag (#Chanel, #StellaMcCartney)
- Include style tags (#极简风, #街头风, #老钱风, #高街)
- Include content-type tags (#时装周, #明星穿搭, #单品推荐)
- Include audience tags (#男生穿搭, #女生穿搭) when applicable

### Step 7 — Tag System (分类标签)

Each post gets a `[Tag]` in the title, similar to the Zhihu blog tag system but fashion-focused.

**Tag pool:**

| Tag | When to use |
|-----|-------------|
| 潮流速递 | 热门穿搭单品/趋势（默认） |
| 秀场直击 | 时装周、大秀、发布会 |
| 明星衣橱 | 明星/名人穿搭拆解 |
| 同款追踪 | 某件单品火了，找同款/替代 |
| 品牌上新 | 品牌新品、联名、限量 |
| 潮流公式 | 搭配公式、穿搭模板 |
| 街头捕手 | 街拍、素人穿搭 |
| 价格 conscious | 平价替代、高性价比 |
| 球鞋风暴 | 球鞋相关 |
| 珠宝腕表 | 配饰/珠宝/腕表 |
| 老钱风 | Quiet luxury, 老钱风 |
| 高街玩家 | 街头潮流/高街 |

Tag rules:
- ≤7 characters
- Must be Chinese
- Rotate tags — don't reuse the same tag consecutively

### Step 8 — File Output

Create the post folder:

```bash
mkdir -p "XHS/FASHION/posts/{date}-{slug}/images"
```

**File format for `meta.md` (图文帖):**

```markdown
# [Tag] 帖子标题（≤20字）

## 类型
图文

## 图片文件
images/01.jpg — 图片描述
images/02.jpg — 图片描述
images/03.jpg — 图片描述
...

## 以下内容直接复制到小红书

图1: xxx
图2: xxx
图3: xxx
...

（背景+亮点+看法，200-400字）

单品清单：
🧥 xxx ｜ Brand ｜约¥X-¥Y
👖 xxx ｜ Brand ｜约¥X-¥Y
👟 xxx ｜ Brand ｜约¥X-¥Y
👜 xxx ｜ Brand ｜约¥X-¥Y

#标签1 #标签2 #标签3 ...

## 来源（不发到小红书，仅作记录）
原文：[Title](URL) · 来源/日期
```

**File format for `meta.md` (视频帖):**

```markdown
# [Tag] 帖子标题（≤20字）

## 类型
视频

## 视频文件
video.mp4

## 封面图
images/frame_01.jpg

## 以下内容直接复制到小红书

（文案内容，≤1000字，包含背景+单品+标签）

#标签1 #标签2 #标签3 ...

## 来源（不发到小红书，仅作记录）
原文：[Title](URL) · 来源/日期
视频来源：[Channel](URL)

## 抖音发布（可选）

抖音标题：（≤30字，可与小红书不同）
抖音标签：（抖音热门标签格式）
```

### Step 9 — Deliver

Present the user with a consolidated summary:
1. **Post type**: 图文 or 视频
2. **Title**: Final title with tag
3. **Image/video count**: How many images, or video duration
4. **Product list**: Brief summary of items identified
5. **Source**: Where the content came from
6. **File location**: Path to the post folder

**Character count verification**: Before delivering, always verify:
- Title ≤20 characters: `echo "标题内容" | wc -m`
- Body text ≤1000 characters: `cat << 'EOF' | wc -m` (counting the full "直接复制到小红书" section content)

User reviews and posts manually — I handle all the preparation, they do the final click.

### Image Notes

**I cannot edit images** (add text overlays, annotations, watermarks). For single-item highlights on images, the user can:
- Use XHS's built-in text/layout tools
- Use separate annotation apps
- Rely on the detailed product list in the body text instead

All product details, prices, and links go in the **正文** and **单品清单** sections — this is the primary information carrier, not the image itself.

## Candidate Pool (候选库)

Unused candidates saved to `XHS/FASHION/candidates/candidates.md`, format:

```markdown
### N. 内容标题

- **来源**: URL
- **类型**: 明星穿搭/时装周/潮流趋势/品牌上新/街拍
- **热度**: ⭐评分 (1-5)
- **关键单品**: 品牌名 x2-3
- **适合XHS原因**: 一句话
- **状态**: 未使用 / 已使用 (日期)
```

## Quality Checklist

- [ ] Title ≤20 Chinese characters, punchy and specific (use `echo "标题" | wc -m` to verify)
- [ ] Body text ≤1000 Chinese characters total (use `cat << 'EOF' | wc -m` to verify, counting the full "直接复制到小红书" content)
- [ ] Body text is ready to copy-paste directly to XHS — no separate sections needed
- [ ] Product list placed right after image descriptions, before background story
- [ ] Image descriptions included in body text (图1/图2/...)
- [ ] Product list with emoji prefixes, brand names, and price ranges integrated into body text
- [ ] 5-8 relevant hashtags at the end of body text
- [ ] Tag from tag pool, ≤7 characters, Chinese
- [ ] Images downloaded and verified (check file sizes, not 0-byte)
- [ ] Images numbered in logical order (cover → full look → details)
- [ ] Video downloaded and verified (if applicable)
- [ ] No AI-flavor language
- [ ] Conversational tone, like sharing with a fashion-savvy friend
- [ ] Specific brand names and prices, not vague descriptions
- [ ] Source credited
- [ ] File saved to correct path: `XHS/FASHION/posts/{date}-{slug}/`