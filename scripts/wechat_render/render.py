#!/usr/bin/env python3
"""
Markdown -> WeChat-compatible inline-style HTML renderer.

Theme: tech-navy
Optimized for: AI/tech daily-digest newsletters.

Design principles (see README):
- Reading time first: cards, anchor emojis, micro-spacing, scannable.
- No marketing aesthetics: no gradients, no glow, no excessive emojis.
- Inline style only (WeChat strips <style>, classes, scripts).
- All semantic patterns from our daily-report markdown are recognized:
    H1 -> hero header
    H2 -> section banner (color-coded by category)
    H4 (#### N. [title](url)) -> news card
    First bullet (- 🔥 ... | [link]) -> meta-line under title
    Subsequent bullets / paragraphs -> body
    **含义** / **与本报...形成** patterns -> 💡 takeaway block
    Inline links -> moved to bottom of card as ↗ chips

Usage:
    python render.py INPUT.md OUTPUT.html
"""

import re
import sys
from pathlib import Path
from html import escape

# ----------------------------------------------------------------------------
# Theme: tech-navy
# ----------------------------------------------------------------------------

THEME = {
    # Palette
    "bg":            "#FAFAF7",   # off-white page background
    "card_bg":       "#FFFFFF",
    "ink":           "#1F2933",   # body text
    "ink_dim":       "#52606D",   # secondary text
    "ink_faint":     "#7B8794",   # tertiary text
    "navy":          "#1E3A5F",   # primary brand
    "navy_deep":     "#142A47",
    "accent":        "#E07B3F",   # callout orange (sparingly)
    "rule":          "#E4E7EB",   # divider
    "soft":          "#F3F5F7",   # subtle fill (chips, code)

    # Section category colors
    "cat_headline":  "#C0392B",   # 头条速递 - red
    "cat_tech":      "#1E3A5F",   # AI 技术前沿 - navy
    "cat_industry":  "#2E7D5B",   # AI 产业动态 - green
    "cat_market":    "#B5892C",   # AI 金融市场 - gold
    "cat_dev":       "#5B4E8A",   # 开发者 - purple
    "cat_longread":  "#7B5E3B",   # 长文精选 - brown
    "cat_default":   "#52606D",

    # Typography
    "font":          "-apple-system, BlinkMacSystemFont, 'PingFang SC', 'Helvetica Neue', Arial, sans-serif",
    "size_body":     "16px",
    "size_meta":     "13px",
    "size_h1":       "26px",
    "size_h2":       "20px",
    "size_card_title":"18px",
    "size_card_num": "32px",
    "lh_body":       "1.85",
}

# Map section title (text after H2) to category color.
CATEGORY_MAP = [
    (re.compile(r"头条"),            ("cat_headline", "🔥", "头条速递")),
    (re.compile(r"技术前沿|技术"),   ("cat_tech",     "🧠", "AI 技术前沿")),
    (re.compile(r"产业动态|产业"),   ("cat_industry", "🏭", "AI 产业动态")),
    (re.compile(r"金融|市场"),       ("cat_market",   "💰", "AI 金融市场")),
    (re.compile(r"开发者|开源"),     ("cat_dev",      "🛠", "开发者与开源")),
    (re.compile(r"长文|精选"),       ("cat_longread", "📖", "长文精选")),
]


# ----------------------------------------------------------------------------
# Inline markdown helpers
# ----------------------------------------------------------------------------

def _esc(s):
    return escape(s, quote=False)


def render_inline(text, collected_links=None):
    """
    Render a single line of markdown inline syntax to HTML.

    - **bold** -> <strong>
    - *italic* -> <em>
    - `code`  -> <code>
    - [text](url) -> if collected_links is a list, removed from text & appended
                    there as (label, url); else rendered as styled link.
    - Numbers/percent inside <strong> get accent treatment via post-pass.
    """
    s = text

    # 1) extract links first (so bold/italic don't tangle with them)
    def _link_repl(m):
        label, url = m.group(1), m.group(2)
        if collected_links is not None:
            collected_links.append((label.strip(), url.strip()))
            return label  # keep label in text, drop the URL
        return f'<a href="{_esc(url)}" style="color:{THEME["navy"]};text-decoration:none;border-bottom:1px solid {THEME["navy"]}33;">{_esc(label)}</a>'

    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", _link_repl, s)

    # 2) inline code
    s = re.sub(
        r"`([^`]+)`",
        lambda m: f'<code style="background:{THEME["soft"]};padding:2px 6px;border-radius:4px;font-size:13px;color:{THEME["navy_deep"]};font-family:SFMono-Regular,Menlo,Consolas,monospace;">{_esc(m.group(1))}</code>',
        s,
    )

    # 3) bold (must come before italic to avoid ** being eaten by *)
    def _bold_repl(m):
        inner = m.group(1)
        # Heuristic: pure number/percent/$/字数 -> accent color + slight upscale
        if re.fullmatch(r"[\d¥$€£][\d¥$€£.,%\s亿万千百兆BMK+\-x×一-鿿]*", inner) or re.search(r"\d+%|\$\d|\d+\s?亿|\d+\s?万", inner):
            return f'<strong style="color:{THEME["accent"]};font-weight:600;">{_esc(inner)}</strong>'
        return f'<strong style="color:{THEME["navy_deep"]};font-weight:600;">{_esc(inner)}</strong>'

    s = re.sub(r"\*\*([^*]+)\*\*", _bold_repl, s)

    # 4) italic
    s = re.sub(
        r"(?<!\*)\*([^*]+)\*(?!\*)",
        lambda m: f'<em style="color:{THEME["ink_dim"]};font-style:italic;">{_esc(m.group(1))}</em>',
        s,
    )

    # NOTE: We intentionally escaped only inside our specific replacements.
    # Outside text was NOT escaped because then our <strong>/<a> would get
    # escaped too. We rely on input being plain prose (no raw HTML). For
    # daily-report markdown this is true.
    return s


# ----------------------------------------------------------------------------
# Markdown block parser (purpose-built, not generic)
# ----------------------------------------------------------------------------

def parse_blocks(md_text):
    """
    Walk the markdown and emit a sequence of typed blocks:
      ("h1", text)
      ("blockquote", text)
      ("h2", text)
      ("hr",)
      ("news", {
          "num": int,
          "title": str, "title_url": str|None,
          "meta": str|None,  # rendered HTML for the 1st bullet
          "body": [str],     # remaining paragraphs (raw markdown lines)
          "links": [(label, url), ...]
      })
      ("p", text)            # standalone paragraph (footer date etc.)
    """
    blocks = []
    lines = md_text.splitlines()
    i = 0
    n = len(lines)

    h4_re = re.compile(r"^####\s+(\d+)\.\s*(.*)$")
    title_link_re = re.compile(r"^\[([^\]]+)\]\(([^)]+)\)\s*$")

    while i < n:
        line = lines[i].rstrip()

        if not line.strip():
            i += 1
            continue

        # H1
        if line.startswith("# ") and not line.startswith("## "):
            blocks.append(("h1", line[2:].strip()))
            i += 1
            continue

        # H2 — 跳过 "## 今日摘要" 区块（它会通过 extract_highlights_from_md 单独提取）
        if line.startswith("## ") and not line.startswith("### "):
            h2_text = line[3:].strip()
            if re.fullmatch(r"今日摘要", h2_text):
                # 跳过整个摘要区块直到下一个 H1/H2/HR
                i += 1
                while i < n:
                    nxt = lines[i].rstrip().strip()
                    if nxt.startswith("# ") or nxt.startswith("## ") \
                       or re.fullmatch(r"-{3,}", nxt):
                        break
                    i += 1
                continue
            blocks.append(("h2", h2_text))
            i += 1
            continue

        # Blockquote (single line — daily report uses one-liners)
        if line.startswith("> "):
            blocks.append(("blockquote", line[2:].strip()))
            i += 1
            continue

        # Horizontal rule
        if re.fullmatch(r"-{3,}", line):
            blocks.append(("hr",))
            i += 1
            continue

        # H4 news card start
        m = h4_re.match(line)
        if m:
            num = int(m.group(1))
            title_remainder = m.group(2).strip()
            title_url = None
            title_text = title_remainder
            tm = title_link_re.match(title_remainder)
            if tm:
                title_text = tm.group(1).strip()
                title_url = tm.group(2).strip()

            i += 1
            # Collect bullet/paragraph lines until next H4/H2/H1/hr/EOF
            meta_line = None
            body_lines = []
            while i < n:
                nxt = lines[i].rstrip()
                if not nxt.strip():
                    body_lines.append("")
                    i += 1
                    continue
                if nxt.startswith("## ") or nxt.startswith("# ") \
                   or h4_re.match(nxt) or re.fullmatch(r"-{3,}", nxt):
                    break
                # First bullet is meta; subsequent bullets become regular paragraphs
                if nxt.startswith("- "):
                    content = nxt[2:].strip()
                    if meta_line is None:
                        meta_line = content
                    else:
                        body_lines.append(content)
                else:
                    body_lines.append(nxt)
                i += 1

            blocks.append(("news", {
                "num": num,
                "title": title_text,
                "title_url": title_url,
                "meta_raw": meta_line,
                "body_raw": body_lines,
            }))
            continue

        # Italic-only single line treated as small caption (e.g. "*2026-05-25*")
        if line.startswith("*") and line.endswith("*") and len(line) > 2:
            blocks.append(("caption", line.strip("*").strip()))
            i += 1
            continue

        # Fallback paragraph
        blocks.append(("p", line))
        i += 1

    return blocks


# ----------------------------------------------------------------------------
# Block -> HTML rendering (tech-navy theme)
# ----------------------------------------------------------------------------

def section_meta(title_text):
    """Return (color_key, emoji, clean_title) for an H2 title."""
    # Strip leading emoji that's already in source
    clean = re.sub(r"^[\U0001F300-\U0001FAFF☀-➿]+\s*", "", title_text).strip()
    for pat, info in CATEGORY_MAP:
        if pat.search(clean):
            return info
    return ("cat_default", "·", clean)


def render_h1(text):
    return f"""
<section style="margin:0 0 28px 0;padding:24px 22px 22px 22px;background:{THEME['navy']};border-radius:10px;">
  <h1 style="margin:0;font-size:{THEME['size_h1']};line-height:1.3;color:#FFFFFF;font-weight:700;letter-spacing:0.5px;">{_esc(text)}</h1>
  <p style="margin:8px 0 0 0;font-size:13px;color:#B7C6D6;letter-spacing:1px;">7 分钟读完 · 今日 AI</p>
</section>
"""


def render_blockquote(text):
    # v2: 信源行不显示（用户反馈：开头信源去掉）。仍然返回空串以维持原触发位
    # 让 render_md_to_html 在 blockquote 位置插入摘要。
    return ""


def render_h2(text):
    color_key, emoji, clean = section_meta(text)
    color = THEME[color_key]
    return f"""
<section style="margin:32px 0 18px 0;">
  <div style="display:inline-block;padding:6px 14px 6px 12px;background:{color};border-radius:4px;">
    <span style="font-size:15px;color:#FFFFFF;font-weight:600;letter-spacing:0.5px;">{emoji}&nbsp;&nbsp;{_esc(clean)}</span>
  </div>
  <div style="margin-top:10px;height:1px;background:{THEME['rule']};"></div>
</section>
"""


def render_hr():
    # Use a subtle "···" instead of harsh line between card groups
    return f"""
<section style="margin:24px 0;text-align:center;">
  <span style="color:{THEME['ink_faint']};letter-spacing:6px;font-size:14px;">· · ·</span>
</section>
"""


def render_caption(text):
    return f"""
<section style="margin:24px 0 16px 0;text-align:center;">
  <span style="color:{THEME['ink_faint']};font-size:12px;letter-spacing:1px;">{_esc(text)}</span>
</section>
"""


def render_p(text):
    inner = render_inline(text)
    return f"""
<p style="margin:0 0 14px 0;font-size:{THEME['size_body']};line-height:{THEME['lh_body']};color:{THEME['ink']};">{inner}</p>
"""


def _process_body_paragraph(raw, links):
    """
    Render one body paragraph and detect '含义' / '与本报...形成镜像' patterns.
    Returns (html_block, is_takeaway).
    """
    # Detect takeaway: starts with **含义** or contains "形成镜像/形成对仗/形成共振"
    is_takeaway = bool(
        re.match(r"^\*\*(含义|结论|读图|资金主线读图)\*\*", raw)
        or re.search(r"\*\*与本报.*?形成.*?\*\*", raw)
    )
    inner = render_inline(raw, collected_links=links)

    if is_takeaway:
        return (f"""
<section style="margin:14px 0 4px 0;padding:12px 14px;background:#FFF7EE;border-left:3px solid {THEME['accent']};border-radius:0 6px 6px 0;">
  <p style="margin:0;font-size:15px;line-height:1.75;color:{THEME['ink']};">
    <span style="color:{THEME['accent']};font-weight:600;letter-spacing:0.5px;">💡 含义&nbsp;·&nbsp;</span>{inner}
  </p>
</section>
""", True)

    return (f"""
<p style="margin:0 0 12px 0;font-size:{THEME['size_body']};line-height:{THEME['lh_body']};color:{THEME['ink']};">{inner}</p>
""", False)


def render_news(card):
    num = card["num"]
    title = card["title"]
    title_url = card["title_url"]

    links = []  # collected from meta + body via render_inline
    # Title link goes first in the link chip list
    if title_url:
        links.append(("原文", title_url))

    # Meta
    meta_html = ""
    if card["meta_raw"]:
        meta_inner = render_inline(card["meta_raw"], collected_links=links)
        meta_html = f"""
<p style="margin:0 0 14px 0;font-size:{THEME['size_meta']};color:{THEME['ink_faint']};line-height:1.6;">{meta_inner}</p>
"""

    # Body
    body_html_parts = []
    for raw in card["body_raw"]:
        raw = raw.strip()
        if not raw:
            continue
        block, _ = _process_body_paragraph(raw, links)
        body_html_parts.append(block)
    body_html = "".join(body_html_parts)

    # Link chips (dedupe while preserving order)
    # 微信草稿强制移除非白名单外链，所以 chip 视觉上保留但同时显示纯文本 URL，方便读者长按复制
    seen = set()
    rows = []
    for label, url in links:
        key = (label, url)
        if key in seen:
            continue
        seen.add(key)
        rows.append(
            f'<p style="margin:0 0 6px 0;font-size:12px;line-height:1.6;color:{THEME["ink_faint"]};word-break:break-all;">'
            f'<span style="display:inline-block;padding:1px 8px;margin-right:8px;background:{THEME["soft"]};color:{THEME["navy"]};font-size:12px;border-radius:3px;border:1px solid #E2E8F0;">↗ {_esc(label)}</span>'
            f'<span style="color:{THEME["ink_faint"]};">{_esc(url)}</span>'
            f'</p>'
        )
    chips_html = ""
    if rows:
        chips_html = f"""
<section style="margin:14px 0 0 0;padding-top:12px;border-top:1px dashed {THEME['rule']};">
  {''.join(rows)}
</section>
"""

    # Title (with optional anchor link)
    title_inner = _esc(title)
    title_block = f'<span style="color:{THEME["ink"]};">{title_inner}</span>'

    # 序号 + 标题：用 inline-block 组合，避免 table 在微信里被强加边框
    # 序号缩小并改成 accent 色 chip，更紧凑、不出现大方框
    num_chip = (
        f'<span style="display:inline-block;padding:2px 8px;margin-right:8px;'
        f'background:{THEME["navy"]};color:#FFFFFF;font-size:13px;font-weight:600;'
        f'border-radius:3px;font-family:\'Helvetica Neue\',Arial,sans-serif;'
        f'letter-spacing:0.5px;vertical-align:middle;">No. {num:02d}</span>'
    )

    return f"""
<section style="margin:0 0 22px 0;padding:18px 18px 16px 18px;background:{THEME['card_bg']};border:1px solid {THEME['rule']};border-radius:8px;">
  <p style="margin:0 0 12px 0;font-size:{THEME['size_card_title']};line-height:1.5;font-weight:600;">{num_chip}{title_block}</p>
  {meta_html}
  {body_html}
  {chips_html}
</section>
"""


# ----------------------------------------------------------------------------
# Cross-reference rewrite: "本报第 X 条" -> "下文 #X" / "前文 #X"
# ----------------------------------------------------------------------------

def rewrite_cross_refs(blocks):
    """In-place rewrite of '本报第 N 条' inside news bodies/metas based on the
    current card's number relative to the referenced number."""
    cur = 0
    for block in blocks:
        if block[0] != "news":
            continue
        payload = block[1]
        cur = payload["num"]
        if payload["meta_raw"]:
            payload["meta_raw"] = _rewrite_ref_in_text(payload["meta_raw"], cur)
        payload["body_raw"] = [_rewrite_ref_in_text(s, cur) for s in payload["body_raw"]]
    return blocks


def _rewrite_ref_in_text(text, cur):
    if not text:
        return text

    def repl(m):
        ref = int(m.group(1))
        if ref < cur:
            return f"前文 #{ref}"
        if ref > cur:
            return f"下文 #{ref}"
        return f"#{ref}"

    return re.sub(r"本报第\s*(\d+)\s*条", repl, text)


# ----------------------------------------------------------------------------
# Today-highlights summary (READ from explicit "## 今日摘要" section in MD)
# ----------------------------------------------------------------------------

def extract_highlights_from_md(md_text):
    """
    从 markdown 中提取显式撰写的"## 今日摘要"区块。
    格式约定：
        ## 今日摘要
        - 第一句话（作者人为提炼，确保完整不省略）
        - 第二句话
        - 第三句话

    返回 list[str]（已剥掉前导 '- '），无该区块时返回 []。
    摘要内容由日报作者撰写，渲染器不做任何截断/压缩/猜测。
    """
    lines = md_text.splitlines()
    n = len(lines)
    items = []
    i = 0
    header_re = re.compile(r"^##\s+今日摘要\s*$")
    while i < n:
        if header_re.match(lines[i].strip()):
            i += 1
            while i < n:
                line = lines[i].rstrip()
                stripped = line.strip()
                if not stripped:
                    i += 1
                    continue
                # 遇到下一个 H1/H2/HR 则区块结束
                if stripped.startswith("# ") or stripped.startswith("## ") \
                   or re.fullmatch(r"-{3,}", stripped):
                    return items
                if stripped.startswith("- "):
                    items.append(stripped[2:].strip())
                i += 1
            return items
        i += 1
    return items


def render_highlights(items):
    if not items:
        return ""
    lis = []
    for raw in items:
        # 支持 inline markdown（bold/italic/code），但摘要里通常是纯文本一句话
        inner = render_inline(raw)
        # 改用 inline span 前缀（微信会剥 position:absolute 导致圆点跨行）
        lis.append(
            f'<p style="margin:0 0 12px 0;line-height:1.75;color:{THEME["ink"]};font-size:14px;">'
            f'<span style="display:inline-block;width:14px;color:{THEME["navy"]};font-weight:700;vertical-align:top;">·</span>'
            f'<span style="display:inline-block;width:calc(100% - 18px);vertical-align:top;">{inner}</span>'
            f'</p>'
        )
    return f"""
<section style="margin:0 0 26px 0;padding:16px 18px;background:#F6F8FB;border:1px solid #E4EBF3;border-radius:8px;">
  <p style="margin:0 0 10px 0;font-size:13px;color:{THEME['navy']};font-weight:600;letter-spacing:1px;">📋 今日摘要</p>
  {"".join(lis)}
</section>
"""


# ----------------------------------------------------------------------------
# Footer (subscribe nudge)
# ----------------------------------------------------------------------------

def render_footer():
    return f"""
<section style="margin:32px 0 0 0;padding:18px 18px;background:{THEME['navy']};border-radius:8px;text-align:center;">
  <p style="margin:0 0 4px 0;color:#FFFFFF;font-size:15px;font-weight:600;letter-spacing:0.5px;">👋 关注「token 日报」</p>
  <p style="margin:0;color:#B7C6D6;font-size:13px;line-height:1.7;">模型在卷、芯片在涨、资金在动<br/>每天 7 分钟，读完今日 AI</p>
</section>
"""


# ----------------------------------------------------------------------------
# Main entry
# ----------------------------------------------------------------------------

def render_md_to_html(md_text):
    blocks = parse_blocks(md_text)
    blocks = rewrite_cross_refs(blocks)
    highlights = extract_highlights_from_md(md_text)

    parts = []
    h1_done = False
    quote_done = False
    highlights_inserted = False

    for block in blocks:
        kind = block[0]
        payload = block[1] if len(block) > 1 else None
        if kind == "h1":
            parts.append(render_h1(payload))
            h1_done = True
        elif kind == "blockquote":
            parts.append(render_blockquote(payload))
            quote_done = True
            # Insert highlights right after the source line
            if not highlights_inserted:
                parts.append(render_highlights(highlights))
                highlights_inserted = True
        elif kind == "hr":
            parts.append(render_hr())
        elif kind == "h2":
            # Safety: if no blockquote existed, insert highlights before first H2
            if h1_done and not highlights_inserted:
                parts.append(render_highlights(highlights))
                highlights_inserted = True
            parts.append(render_h2(payload))
        elif kind == "news":
            parts.append(render_news(payload))
        elif kind == "p":
            parts.append(render_p(payload))
        elif kind == "caption":
            parts.append(render_caption(payload))

    parts.append(render_footer())

    body = "".join(parts)

    # Outer container — single root <section> per WeChat best practice
    return f"""<section style="background:{THEME['bg']};padding:20px 14px;font-family:{THEME['font']};color:{THEME['ink']};max-width:677px;margin:0 auto;">{body}</section>"""


def _extract_h1(md_text):
    """Extract first H1 text for use as <title>."""
    for line in md_text.splitlines():
        s = line.strip()
        if s.startswith("# ") and not s.startswith("## "):
            return s[2:].strip()
    return "AI 日报"


def main():
    import argparse
    p = argparse.ArgumentParser(description="Markdown -> WeChat-compatible HTML renderer.")
    p.add_argument("input", help="INPUT.md")
    p.add_argument("output", help="OUTPUT.html")
    p.add_argument("--cover", help="Optional cover image local path; embedded as first <img> "
                                    "so publisher auto-uploads and uses as draft cover.")
    args = p.parse_args()

    src = Path(args.input)
    dst = Path(args.output)
    md = src.read_text(encoding="utf-8")
    html_body = render_md_to_html(md)
    page_title = _extract_h1(md)

    # 若指定 --cover：在 <body> 最前面插一个绝对路径的 <img>
    # publisher 见到本地路径会自动上传到微信素材库，并将首张图作为草稿封面（SKILL.md 第 326 行）
    cover_img_html = ""
    if args.cover:
        cover_path = str(Path(args.cover).resolve())
        cover_img_html = (
            f'<p style="margin:0 0 16px 0;text-align:center;">'
            f'<img src="{cover_path}" alt="封面" '
            f'style="max-width:100%;border-radius:8px;display:block;margin:0 auto;" />'
            f'</p>'
        )

    # Wrap with minimal full HTML for local preview convenience.
    # When publishing to WeChat, publisher reads <title> for the draft title,
    # so we set it to the real H1 (e.g. "AI 日报 | 2026-05-26").
    full = f"""<!DOCTYPE html>
<html lang="zh-CN"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(page_title, quote=False)}</title>
<style>body{{margin:0;background:#ECECEC;}}</style>
</head><body>{cover_img_html}{html_body}</body></html>"""

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(full, encoding="utf-8")
    cover_info = f"  cover='{args.cover}'" if args.cover else ""
    print(f"wrote {dst} ({len(full):,} bytes)  title='{page_title}'{cover_info}")


if __name__ == "__main__":
    main()
