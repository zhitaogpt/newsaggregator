---
name: ai-daily-report
description: >
  Generate a curated daily AI report (AI 日报) covering both AI technology and AI financial markets.
  Use when the user asks for: AI 日报, AI daily report, AI 深度日报, 每日 AI 简报, or similar requests
  for a comprehensive daily AI news digest. The report is organized by TOPIC (not by source),
  treats all news sources as data-gathering tools, and emphasizes selective curation with deep insight
  over exhaustive coverage. Covers: AI industry moves, frontier research, capital & markets,
  product ecosystem, and long-form essays.
---

# AI Daily Report Skill

Generate a high-quality, insight-driven daily AI report in Simplified Chinese.

## Design Philosophy

1. **Source-agnostic**: Sources are data-gathering tools, NOT report sections. Never organize by source.
2. **Topic-driven**: Group items by theme/topic for narrative coherence.
3. **Selective curation**: 10-15 items total. Quality over quantity — skip noise, keep signal.
4. **Insight-first**: Every item MUST have original analysis, not just summary. Ask: "So what? Why does this matter?"
5. **Cross-reference**: Connect related items across sources to surface patterns and trends.

---

## Workflow

### Step 1: Gather Raw Data (parallel background)

Run from `news-aggregator-skill` base directory. **All commands launched as parallel background Bash calls** (`run_in_background: true`), outputting to temp files. After all finish, read results.

Note: The script uses a single `--keyword` for all sources in one invocation, so sources needing different keywords must be separate commands.

Launch these 4 Bash calls simultaneously (single message, all `run_in_background: true`):

```bash
# Bash 1: No-keyword sources (huggingface, chinai, essays, podcasts, latentspace, bensbites)
export https_proxy=http://127.0.0.1:13659 http_proxy=http://127.0.0.1:13659 && cd /Users/guanxuan.zzt/repos/newsaggregator/.claude/skills/news-aggregator-skill && python3 scripts/fetch_news.py --source huggingface,chinai,latentspace,bensbites,essays,podcasts --limit 15 --deep --no-save > /tmp/ai_daily_nokw.json 2>&1

# Bash 2: AI keyword sources (hackernews, github, producthunt, v2ex)
export https_proxy=http://127.0.0.1:13659 http_proxy=http://127.0.0.1:13659 && cd /Users/guanxuan.zzt/repos/newsaggregator/.claude/skills/news-aggregator-skill && python3 scripts/fetch_news.py --source hackernews,github,producthunt,v2ex --keyword "AI,LLM,GPT,Claude,Anthropic,OpenAI,Agent,RAG,DeepSeek,Gemini,model,transformer,大模型" --limit 20 --deep --no-save > /tmp/ai_daily_tech.json 2>&1

# Bash 3: China tech + finance keyword sources (wallstreetcn, 36kr)
export https_proxy=http://127.0.0.1:13659 http_proxy=http://127.0.0.1:13659 && cd /Users/guanxuan.zzt/repos/newsaggregator/.claude/skills/news-aggregator-skill && python3 scripts/fetch_news.py --source wallstreetcn,36kr --keyword "AI,芯片,GPU,大模型,算力,英伟达,OpenAI,Anthropic,融资,IPO,估值,NVIDIA,AMD" --limit 15 --no-save > /tmp/ai_daily_cn.json 2>&1

# Bash 4: Finance-specific (wallstreetcn deep)
export https_proxy=http://127.0.0.1:13659 http_proxy=http://127.0.0.1:13659 && cd /Users/guanxuan.zzt/repos/newsaggregator/.claude/skills/news-aggregator-skill && python3 scripts/fetch_news.py --source wallstreetcn --keyword "Stock,Crypto,Fed,Earnings,财报,营收,投资,基金" --limit 15 --deep --no-save > /tmp/ai_daily_finance.json 2>&1
```

After all background tasks complete, read `/tmp/ai_daily_*.json` files.

### Step 2: Time-Gate, Curate & Deduplicate (with Previous-Day Dedup)

From all gathered data, **time-gate FIRST, then cross-day dedup, then curate**:

1. **⏰ Time-Gate (MANDATORY FIRST STEP)**: For EVERY candidate item, verify publish date is within 24h of report date. Drop ALL items older than 24h immediately. See "时效性强制校验" section below for detailed rules. **This step is non-negotiable and must be done before any other curation.**
2. **📰 跨日去重（MANDATORY SECOND STEP）**: Read the previous day's report from `daily_reports/` (e.g., for today 2026-04-28, read `daily_reports/2026-04-27_ai_daily_report.md`). Compare every surviving candidate against the previous report's items:
   - **Same event/story** (same URL, same project, same announcement, same funding round) → ❌ **Remove** — already reported yesterday
   - **Follow-up or significant new development** of a previously reported story → ✅ Keep, but explicitly note it's an update (e.g., "续报：...") and reference what changed
   - If the previous day's report does not exist, skip this step
   - **This dedup happens BEFORE the general filter/rank step below, to ensure the final 10-15 items are all fresh**
3. **Deduplicate (same-day)**: Same story from multiple sources → merge into one item, cite strongest source
4. **Filter**: Remove low-signal items (routine product updates, minor version bumps, clickbait)
5. **Rank**: Prioritize by: (a) impact on AI industry, (b) novelty, (c) source heat/engagement, (d) cross-source corroboration
6. **Supplement**: If fewer than 10 items survive after dedup + filtering, expand wallstreetcn/36kr keyword coverage, increase their `--limit`, and increase HuggingFace Papers and GitHub Trending limits (these sources have the most reliable timestamps).
7. **Target**: 10-15 final items across all sections

### Step 3: Organize by Topic

Assign each curated item to ONE section (see Report Template below). If an item spans topics, place it where its PRIMARY impact lies.

### Step 4: Write with Insight

For each item, write:
- **Summary**: One clear sentence — what happened
- **Insight**: 2-5 sentences — why it matters, connections to broader trends, implications for developers/investors/industry. Use specific data points. Cross-reference other items in the report when relevant.

### Step 5: Save & Present

Save to: `daily_reports/YYYY-MM-DD_ai_daily_report.md` (relative to project root directory, NOT in a date subdirectory)
Then display the full report to the user.

---

## Report Template

```markdown
# AI 日报 | YYYY-MM-DD

> 信源：Hacker News · HuggingFace · GitHub Trending · Latent Space · Ben's Bites · 长文博客 | 过去 24h

## 今日摘要
<!-- 强制：3 条人工撰写的一句话摘要。每条 25-45 字，必须语义完整、无省略号、无截断。
     这是公众号读者首屏看到的"为什么我要读"，由作者亲自提炼，不可由脚本自动从标题截取。
     建议：3 条覆盖头条速递 + 1 条技术/产业 + 1 条市场/资金主线 的最高信号。 -->

- 一句话摘要 1
- 一句话摘要 2
- 一句话摘要 3

---

## 头条速递
<!-- 2-4 items: The biggest stories of the day across all categories -->

#### N. [标题](url)
- 🔥 Heat | [Discussion](url)
- 摘要 + 深度 insight。交叉引用其他条目中的相关信号。

---

## AI 技术前沿
<!-- 1-3 items: Research papers, technical breakthroughs, model releases, benchmarks -->

#### N. [标题](url)
- 🔥 Heat | [Discussion](url) | [GitHub](url)
- 摘要 + 技术洞察。点明对开发者的实际影响。

---

## AI 产业动态
<!-- 1-3 items: Company moves, product launches, strategy shifts, partnerships -->

#### N. [标题](url)
- 🔥 Heat | [Discussion](url)
- 摘要 + 产业洞察。分析竞争格局变化。

---

## 💰 AI 金融市场
<!-- 1-3 items: Funding, IPOs, stock moves, chip market, valuations -->

#### N. 标题
- 数据点 + 市场分析。连接产业事件与资本信号。

---

## 开发者工具与开源生态
<!-- 1-2 items: GitHub trending, new tools, frameworks, developer experience -->

#### N. [项目名](github_url) — 🌟 Stars
- 项目定位 + 为什么值得关注。与行业趋势的关联。

---

## 📖 长文精选
<!-- 1-3 items: Essays, podcasts, deep dives worth reading in full -->

#### N. [标题](url)
- **Source**: 来源 | **Time**: 时间
- 核心论点 + 为什么值得读。与当下 AI 发展的关联。

---

*YYYY-MM-DD*
```

---

## Section Guidelines

| Section | Target Count | Selection Criteria |
|---|---|---|
| 头条速递 | 2-4 | Highest impact, cross-category significance |
| AI 技术前沿 | 1-3 | Novel research, model releases, important benchmarks |
| AI 产业动态 | 1-3 | Strategic moves, product launches, competitive shifts |
| AI 金融市场 | 1-3 | Funding rounds, IPOs, stock movements, chip market |
| 开发者工具与开源生态 | 1-2 | GitHub trending, new frameworks, developer tools |
| 长文精选 | 1-2 | Deep essays/podcasts worth full read, timeless insights |

---

## Quality Rules

1. **Language**: Simplified Chinese. Keep well-known English proper nouns (ChatGPT, NVIDIA, etc.)
2. **Anti-hallucination**: Only use data from fetched sources and search results. Never invent.
3. **Cross-reference**: When items relate to each other, explicitly connect them (e.g., "结合本报第 N 条...")
4. **Data-driven insight**: Include specific numbers (funding amounts, star counts, benchmark scores, stock prices) — not vague claims.
5. **Contrarian pairs**: When sources present opposing views on the same topic, include BOTH and note the tension.
6. **Time marking**: Always include time/date for each item. Mark supplementary (non-24h) items clearly.
7. **Smart keyword expansion**: "AI" → "AI,LLM,GPT,Claude,Agent,RAG,DeepSeek,Gemini,model,transformer"
8. **今日摘要必写**: `## 今日摘要` 区块强制存在，3 条人工撰写的一句话摘要，每条 25-45 字、语义完整、**禁止省略号 / 禁止截断**。摘要面向公众号读者首屏，决定打开率，必须作者亲自提炼，禁止从 H4 标题自动截取。

---

## ⚠️ 时效性强制校验（CRITICAL）

**所有条目必须通过 24 小时时效性校验，无例外。**

### 校验流程（在 Step 2 Curate 阶段执行）

对每一条候选条目，执行以下校验：

1. **提取原始发布时间**：从 JSON 的 `time` 字段获取。注意区分：
   - `"Today"` / `"3 hours ago"` → 当天，OK
   - `"Fri, 10 Apr 2026 23:30:58 GMT"` → 精确日期，必须计算差值
   - `"2026-04-14"` → 精确日期，必须验证是否在 24h 内
   - `"⚠️ 2026-04-14"` / `smart_fill: true` → 补充数据，需额外审查

2. **计算时间差**：条目发布时间距今天（报告日期）是否 ≤ 24 小时
   - ≤ 24h → ✅ 可用
   - 24h-48h → ❌ 剔除，除非是重大事件且仍在活跃发酵，必须标注原始日期
   - > 48h → ❌ 强制剔除，无论内容多重要

3. **警惕"转发延迟"陷阱**：
   - HN 的 `time: "Today"` 仅表示 HN 帖子是今天发的，**原始文章可能更早**
   - Newsletter（Latent Space、Ben's Bites）的 RSS time 是发布时间，但其内容可能覆盖更早的事件
   - 当 `--deep` 抓取的 content 中包含明确日期时，以**原始事件日期**为准

4. **GitHub Trending 和 HuggingFace Papers 特殊处理**：
   - GitHub Trending `time: "Today"` 表示当日热门，✅ 可用
   - HuggingFace Papers 的日期是论文上线日，仅当日期 = 报告日期时 ✅ 可用

### 违规处理

如果校验后可用条目不足 15 条：
- 扩展 wallstreetcn/36kr 的关键词覆盖范围，增加 `--limit` 数量
- 增加 HuggingFace Papers 和 GitHub Trending 的收录数量（这两个源时效性最可靠）
- **绝不**为了凑数降低时效标准
