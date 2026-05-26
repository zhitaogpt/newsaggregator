#!/usr/bin/env python3
"""
韬见 AI 日报封面渲染器

输出：900×384 PNG（微信公众号大图封面规格 2.35:1）

模板内容（左→右）：
  Left zone (60%):
    - 顶部："韬见 AI · AI 日报" 小字标签（暖金）
    - 主标题：日期 "2026-05-26"（大字、白色）
    - 副标题：摘要第 1 条（深一档白色，2 行内显示）
    - 底部："7 分钟读完今日 AI · 趋势 · 资本 · 投资线索" slogan
  Right zone (40%):
    - 抽象 K 线条形 / 同心圆装饰
    - 与公众号头像视觉一致（深靛蓝 + 古典金 + 微青）

用法：
    python3 cover_render.py INPUT.md OUTPUT.png

INPUT.md 需要包含：
    # AI 日报 | YYYY-MM-DD     ← 用于提取日期
    ## 今日摘要
    - 摘要一句话                ← 用于提取副标题
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import re
import sys
import math
import random

W, H = 900, 384

# 配色（与头像 final_A 完全一致）
NAVY_DEEP   = (15, 30, 61)
NAVY_MID    = (28, 49, 86)
NAVY_SOFT   = (62, 84, 122)
GOLD        = (198, 152, 72)
GOLD_LIGHT  = (228, 192, 122)
GOLD_HI     = (248, 220, 168)
TEAL        = (72, 168, 156)
WHITE_SOFT  = (245, 240, 230)
WHITE_DIM   = (200, 208, 220)

# 字体路径 — Hiragino Sans GB（macOS 自带，PIL 可正常打开；PingFang.ttc 在 PIL 下打不开）
# face index: 0 = W3 (Regular), 2 = W6 (Bold)
FONT_CN_PATH = "/System/Library/Fonts/Hiragino Sans GB.ttc"
FONT_CN_REG_IDX = 0   # W3
FONT_CN_BOLD_IDX = 2  # W6
FONT_LATIN = "/System/Library/Fonts/Helvetica.ttc"


def _font_cn(size, bold=False):
    """加载中文字体（W6 if bold else W3），失败时回退至 STHeiti 再回退至 default。"""
    fallbacks = [
        (FONT_CN_PATH, FONT_CN_BOLD_IDX if bold else FONT_CN_REG_IDX),
        ("/System/Library/Fonts/STHeiti Medium.ttc", 1),
        ("/System/Library/Fonts/STHeiti Light.ttc", 1),
    ]
    for path, idx in fallbacks:
        try:
            return ImageFont.truetype(path, size, index=idx)
        except Exception:
            continue
    return ImageFont.load_default()


def _font_latin(size, bold=False):
    """拉丁数字用 Helvetica。"""
    try:
        return ImageFont.truetype(FONT_LATIN, size, index=1 if bold else 0)
    except Exception:
        return _font_cn(size, bold=bold)


def extract_meta(md_text):
    """从 markdown 抽取 (date_str, summary_line1)。"""
    date_str = ""
    summary = ""
    for line in md_text.splitlines():
        s = line.strip()
        if not date_str:
            m = re.match(r"^#\s+.*?(\d{4}-\d{2}-\d{2})", s)
            if m:
                date_str = m.group(1)
        # find first "- " line under "## 今日摘要"
    # second pass for summary
    in_summary = False
    for line in md_text.splitlines():
        s = line.strip()
        if re.match(r"^##\s+今日摘要", s):
            in_summary = True
            continue
        if in_summary:
            if s.startswith("- "):
                summary = s[2:].strip()
                break
            if s.startswith("#") or re.fullmatch(r"-{3,}", s):
                break
    return date_str or "", summary or ""


def wrap_text(draw, text, font, max_width):
    """按字符宽度换行（中英混排，按字符切，简单粗暴但够用）。"""
    lines = []
    cur = ""
    for ch in text:
        trial = cur + ch
        w = draw.textlength(trial, font=font)
        if w > max_width and cur:
            lines.append(cur)
            cur = ch
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def draw_kline_decor(canvas, cx, cy, scale=1.0):
    """右侧 K 线 + 同心圆装饰（与头像视觉一致）。"""
    d = ImageDraw.Draw(canvas, "RGBA")
    # 同心圆 3 层（金、柔蓝、柔蓝）
    rings = [
        (int(120 * scale), GOLD + (200,), 3),
        (int(95 * scale),  NAVY_SOFT + (220,), 2),
        (int(70 * scale),  NAVY_SOFT + (160,), 2),
    ]
    for r, color, w in rings:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=w)

    # 外环缺口（右上 18°）
    outer_r = int(120 * scale)
    pad = 5
    d.pieslice([cx - outer_r - pad, cy - outer_r - pad,
                cx + outer_r + pad, cy + outer_r + pad],
               start=-39, end=-21, fill=NAVY_DEEP)

    # 中心金圆 + 高光
    pr = int(22 * scale)
    d.ellipse([cx - pr, cy - pr, cx + pr, cy + pr], fill=GOLD)
    hi_r = int(pr * 0.32)
    hi_x, hi_y = cx - int(pr * 0.32), cy - int(pr * 0.32)
    d.ellipse([hi_x - hi_r, hi_y - hi_r, hi_x + hi_r, hi_y + hi_r], fill=GOLD_HI)

    # 罗盘刻度点（避开缺口）
    for ang_deg in [0, 60, 120, 180, 240, 300]:
        if -45 <= ang_deg - 360 <= -15 or -45 <= ang_deg <= -15:
            continue
        ang = math.radians(ang_deg - 90)
        x = cx + int(outer_r * math.cos(ang))
        y = cy + int(outer_r * math.sin(ang))
        r = max(2, int(3 * scale))
        d.ellipse([x - r, y - r, x + r, y + r], fill=GOLD_LIGHT)

    # 底部 K 线 5 根
    bars = [(-2, 14), (-1, 22), (0, 16), (1, 28), (2, 18)]
    bar_w = max(3, int(5 * scale))
    bar_gap = max(2, int(4 * scale))
    base_y = cy + int(90 * scale)
    for off, h in bars:
        x = cx + off * (bar_w + bar_gap)
        hh = int(h * scale)
        d.rectangle([x - bar_w // 2, base_y - hh, x + bar_w // 2, base_y],
                    fill=TEAL + (220,))


def draw_grain(canvas, opacity=10):
    grain = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(grain)
    rnd = random.Random(2026)
    W2, H2 = canvas.size
    for y in range(0, H2, 2):
        for x in range(0, W2, 2):
            v = rnd.randint(0, 60)
            if v > 52:
                d.point((x, y), fill=(255, 255, 255, opacity))
            elif v < 5:
                d.point((x, y), fill=(0, 0, 0, opacity))
    return Image.alpha_composite(canvas, grain)


def render_cover(date_str, summary):
    canvas = Image.new("RGBA", (W, H), NAVY_DEEP + (255,))
    d = ImageDraw.Draw(canvas, "RGBA")

    # 渐变背景（左上略亮 → 右下深）
    grad = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grad)
    for y in range(H):
        t = y / H
        r = int(NAVY_DEEP[0] + (NAVY_MID[0] - NAVY_DEEP[0]) * t)
        g = int(NAVY_DEEP[1] + (NAVY_MID[1] - NAVY_DEEP[1]) * t)
        b = int(NAVY_DEEP[2] + (NAVY_MID[2] - NAVY_DEEP[2]) * t)
        gd.line([(0, y), (W, y)], fill=(r, g, b, 255))
    canvas = grad

    # 右侧装饰区（背景柔光）
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_d = ImageDraw.Draw(glow)
    cx_r, cy_r = int(W * 0.78), H // 2
    for rad in range(180, 60, -3):
        alpha = int(20 * (1 - (180 - rad) / 120))
        glow_d.ellipse([cx_r - rad, cy_r - rad, cx_r + rad, cy_r + rad],
                       fill=GOLD + (alpha // 4,))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=18))
    canvas = Image.alpha_composite(canvas, glow)

    # 装饰主体
    deco = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_kline_decor(deco, cx_r, cy_r, scale=1.0)
    canvas = Image.alpha_composite(canvas, deco)

    d = ImageDraw.Draw(canvas, "RGBA")

    # —— 左侧文字区 ——
    # 字号放大（封面在订阅号列表里实际显示 ~320px 宽，必须够大才看得清）
    pad_l = 56
    text_max_w = int(W * 0.58) - pad_l

    # 顶部 logo label（金色小字）
    label_fnt = _font_cn(22, bold=True)
    d.text((pad_l, 44), "韬见 AI  ·  AI 日报", font=label_fnt, fill=GOLD_LIGHT)

    # 一条金色细线分隔
    d.rectangle([pad_l, 80, pad_l + 44, 83], fill=GOLD)

    # 主标题：日期（Helvetica 大字，更挺拔）
    date_fnt = _font_latin(58, bold=True)
    d.text((pad_l, 100), date_str, font=date_fnt, fill=WHITE_SOFT)

    # 副标题：摘要（W3，最多 2 行）
    sub_fnt = _font_cn(24, bold=False)
    if summary:
        lines = wrap_text(d, summary, sub_fnt, text_max_w)
        lines = lines[:2]
        y = 184
        for line in lines:
            d.text((pad_l, y), line, font=sub_fnt, fill=WHITE_DIM)
            y += 38

    # Slogan（底部）
    slogan_fnt = _font_cn(17, bold=False)
    d.text((pad_l, H - 52), "7 分钟读完今日 AI  ·  趋势 · 资本 · 投资线索",
           font=slogan_fnt, fill=GOLD_LIGHT)

    # 颗粒纹理（极轻）
    canvas = draw_grain(canvas, opacity=8)

    return canvas.convert("RGB")


def main():
    if len(sys.argv) != 3:
        print("Usage: cover_render.py INPUT.md OUTPUT.png", file=sys.stderr)
        sys.exit(2)
    src = Path(sys.argv[1])
    dst = Path(sys.argv[2])
    md = src.read_text(encoding="utf-8")
    date_str, summary = extract_meta(md)
    if not date_str:
        print("warning: no date found in H1, using empty string", file=sys.stderr)
    if not summary:
        print("warning: no '## 今日摘要' bullets found, subtitle will be empty",
              file=sys.stderr)

    img = render_cover(date_str, summary)
    dst.parent.mkdir(parents=True, exist_ok=True)
    img.save(dst, "PNG", optimize=True)
    print(f"wrote {dst} ({W}×{H})  date='{date_str}'  summary='{summary[:40]}...'")


if __name__ == "__main__":
    main()
