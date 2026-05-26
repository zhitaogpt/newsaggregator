#!/usr/bin/env python3
"""
韬见 AI 公众号头像 — 候选生成

设计语言：
- 圆形容器（微信默认 mask 兼容）
- 深靛蓝 + 暖金 + 极少品牌青（克制）
- 主符号是抽象"瞳孔/光圈/同心圆"，承载"洞见 + 投资瞄准镜"双重隐喻
- 中心点用一个微小的"K 线脉冲"暗示资本/数据
- 远看是 logo mark，凑近看有"图表+视觉"的双重含义

生成 3 个方向：
  A. 瞳孔光圈版 — 同心圆 + 中心金色焦点
  B. 望远镜十字版 — 同心圆 + 内部测距十字 + K 线
  C. 韬字结构版 — 几何抽象出"韜"字韦字旁笔意，更东方
"""

from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pathlib import Path
import math

OUT = Path(__file__).parent
SIZE = 1024  # WeChat recommends >=200×200; we go 1024 for retina + downscaling

# ---------------------------------------------------------------------------
# Color palette — 「韬见 AI」 brand
# ---------------------------------------------------------------------------
NAVY_DEEP   = (15, 30, 61)      # #0F1E3D  深靛蓝（主背景）
NAVY_MID    = (28, 49, 86)      # #1C3156  中蓝（同心环）
NAVY_SOFT   = (52, 76, 114)     # #344C72  柔蓝
GOLD        = (212, 162, 76)    # #D4A24C  暖金（焦点/价值）
GOLD_LIGHT  = (240, 198, 116)   # #F0C674  浅金（高光）
TEAL        = (61, 191, 174)    # #3DBFAE  科技青（极少点缀）
WHITE_SOFT  = (245, 240, 230)   # #F5F0E6  暖白
INK_FAINT   = (180, 175, 165)   # 灰白

# ---------------------------------------------------------------------------
# Common helpers
# ---------------------------------------------------------------------------

def make_canvas(bg=NAVY_DEEP):
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    return img


def draw_circle_bg(img, color):
    """Fill a perfect circle that fits the canvas."""
    d = ImageDraw.Draw(img)
    d.ellipse([0, 0, SIZE, SIZE], fill=color)


def add_grain(img, opacity=18):
    """Subtle film-grain so the navy doesn't feel digitally flat."""
    import random
    grain = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(grain)
    rnd = random.Random(2026)
    step = 2
    for y in range(0, SIZE, step):
        for x in range(0, SIZE, step):
            v = rnd.randint(0, 60)
            if v > 50:
                d.point((x, y), fill=(255, 255, 255, opacity))
            elif v < 6:
                d.point((x, y), fill=(0, 0, 0, opacity))
    return Image.alpha_composite(img, grain)


def add_vignette(img, intensity=80):
    """Darken edges so the round logo gets a subtle inner glow center."""
    v = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(v)
    cx, cy = SIZE // 2, SIZE // 2
    max_r = int(SIZE * 0.72)
    for r in range(max_r, SIZE // 2, -1):
        alpha = int(intensity * (r - max_r) / (SIZE // 2 - max_r))
        d.ellipse([cx - r, cy - r, cx + r, cy + r],
                  outline=(0, 0, 0, max(0, min(255, alpha))), width=1)
    return Image.alpha_composite(img, v)


# ---------------------------------------------------------------------------
# Direction A: 瞳孔光圈 (Pupil / Aperture)
# 三层同心圆 + 中心金色实点 + 一个被打断的描边（暗示"洞察缺口"）
# ---------------------------------------------------------------------------

def design_A():
    img = make_canvas()
    draw_circle_bg(img, NAVY_DEEP)
    d = ImageDraw.Draw(img)
    cx, cy = SIZE // 2, SIZE // 2

    # 三层同心环（金 → 蓝 → 蓝），最外层是暖金细线（品牌主色）
    rings = [
        (int(SIZE * 0.46), GOLD,       4),    # 外环金线
        (int(SIZE * 0.36), NAVY_SOFT,  3),    # 中环柔蓝
        (int(SIZE * 0.26), NAVY_SOFT,  2),    # 内环柔蓝
    ]
    for r, color, w in rings:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=w)

    # 外环金线"洞察缺口"：在右上 30° 区间断开
    # 用背景色覆盖，模拟描边断开
    arc_r = int(SIZE * 0.46)
    d.pieslice([cx - arc_r - 4, cy - arc_r - 4, cx + arc_r + 4, cy + arc_r + 4],
               start=-45, end=-15, fill=NAVY_DEEP)

    # 中心金色实心圆（瞳孔焦点）
    pupil_r = int(SIZE * 0.085)
    d.ellipse([cx - pupil_r, cy - pupil_r, cx + pupil_r, cy + pupil_r],
              fill=GOLD)

    # 瞳孔高光（左上小亮点）
    hi_r = int(pupil_r * 0.32)
    hi_x, hi_y = cx - int(pupil_r * 0.35), cy - int(pupil_r * 0.35)
    d.ellipse([hi_x - hi_r, hi_y - hi_r, hi_x + hi_r, hi_y + hi_r],
              fill=GOLD_LIGHT)

    # 底部 K 线脉冲（暗示资本/数据），用极淡的青色细线
    bar_w = 6
    bar_color = TEAL + (180,)
    bars = [(-3, 0.04), (-2, 0.07), (-1, 0.05), (0, 0.10), (1, 0.06), (2, 0.09), (3, 0.05)]
    base_y = cy + int(SIZE * 0.34)
    for i, (off, h) in enumerate(bars):
        x = cx + off * (bar_w + 4)
        hh = int(SIZE * h)
        d.rectangle([x - bar_w // 2, base_y - hh, x + bar_w // 2, base_y],
                    fill=bar_color)

    img = add_grain(img, 14)
    img = add_vignette(img, 60)
    return img


# ---------------------------------------------------------------------------
# Direction B: 望远镜测距 (Telescope / Scope)
# 同心圆 + 测距十字 + 中心金 dot + 微 K 线
# ---------------------------------------------------------------------------

def design_B():
    img = make_canvas()
    draw_circle_bg(img, NAVY_DEEP)
    d = ImageDraw.Draw(img)
    cx, cy = SIZE // 2, SIZE // 2

    # 两层同心环
    for r, color, w in [
        (int(SIZE * 0.42), GOLD, 3),
        (int(SIZE * 0.30), NAVY_SOFT, 2),
    ]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=w)

    # 测距十字（中心镂空 — 不画穿中心圆）
    arm_outer = int(SIZE * 0.40)
    arm_inner = int(SIZE * 0.13)
    arm_w = 3
    # 横线
    d.rectangle([cx - arm_outer, cy - arm_w // 2, cx - arm_inner, cy + arm_w // 2], fill=INK_FAINT)
    d.rectangle([cx + arm_inner, cy - arm_w // 2, cx + arm_outer, cy + arm_w // 2], fill=INK_FAINT)
    # 竖线
    d.rectangle([cx - arm_w // 2, cy - arm_outer, cx + arm_w // 2, cy - arm_inner], fill=INK_FAINT)
    d.rectangle([cx - arm_w // 2, cy + arm_inner, cx + arm_w // 2, cy + arm_outer], fill=INK_FAINT)

    # 测距十字端点 tick
    tick = 14
    for (x1, y1, x2, y2) in [
        (cx - arm_outer, cy - tick, cx - arm_outer, cy + tick),
        (cx + arm_outer, cy - tick, cx + arm_outer, cy + tick),
        (cx - tick, cy - arm_outer, cx + tick, cy - arm_outer),
        (cx - tick, cy + arm_outer, cx + tick, cy + arm_outer),
    ]:
        d.line([x1, y1, x2, y2], fill=GOLD, width=3)

    # 中心金圆
    pupil_r = int(SIZE * 0.075)
    d.ellipse([cx - pupil_r, cy - pupil_r, cx + pupil_r, cy + pupil_r], fill=GOLD)

    # 中心 K 线脉冲（金色，在 pupil 内部）
    bar_w = 3
    bars = [(-2, 0.018), (-1, 0.030), (0, 0.022), (1, 0.034), (2, 0.020)]
    for off, h in bars:
        x = cx + off * (bar_w + 3)
        hh = int(SIZE * h)
        d.rectangle([x - bar_w // 2, cy - hh // 2, x + bar_w // 2, cy + hh // 2],
                    fill=NAVY_DEEP)

    img = add_grain(img, 12)
    img = add_vignette(img, 50)
    return img


# ---------------------------------------------------------------------------
# Direction C: 韬字几何抽象
# 用"韦"字旁的横竖结构 + 同心圆，更东方 / 更克制
# ---------------------------------------------------------------------------

def design_C():
    img = make_canvas()
    draw_circle_bg(img, NAVY_DEEP)
    d = ImageDraw.Draw(img)
    cx, cy = SIZE // 2, SIZE // 2

    # 大金色外环
    outer_r = int(SIZE * 0.43)
    d.ellipse([cx - outer_r, cy - outer_r, cx + outer_r, cy + outer_r],
              outline=GOLD, width=4)

    # 内层柔蓝中环
    inner_r = int(SIZE * 0.30)
    d.ellipse([cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r],
              outline=NAVY_SOFT, width=2)

    # "韬"字几何抽象：上横、中竖、下横（隐喻韦字旁框架）
    # 上横（金色，长）
    h_len = int(SIZE * 0.22)
    h_w = 8
    d.rectangle([cx - h_len // 2, cy - int(SIZE * 0.10) - h_w // 2,
                 cx + h_len // 2, cy - int(SIZE * 0.10) + h_w // 2],
                fill=GOLD)
    # 中竖
    v_h = int(SIZE * 0.22)
    v_w = 8
    d.rectangle([cx - v_w // 2, cy - v_h // 2, cx + v_w // 2, cy + v_h // 2],
                fill=GOLD)
    # 下横（柔蓝，短）— 暗示"藏"
    h2_len = int(SIZE * 0.14)
    d.rectangle([cx - h2_len // 2, cy + int(SIZE * 0.10) - h_w // 2,
                 cx + h2_len // 2, cy + int(SIZE * 0.10) + h_w // 2],
                fill=NAVY_SOFT)

    # 中央焦点小圆（白）
    dot_r = 9
    d.ellipse([cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r], fill=WHITE_SOFT)

    img = add_grain(img, 14)
    img = add_vignette(img, 50)
    return img


# ---------------------------------------------------------------------------
# Save + downsample for WeChat upload (recommends 200px+, but we provide both)
# ---------------------------------------------------------------------------

def save_variant(img, name):
    img.save(OUT / f"{name}_1024.png", "PNG")
    img.resize((144, 144), Image.LANCZOS).save(OUT / f"{name}_144.png", "PNG")
    print(f"  wrote {name}_1024.png  + _144.png")


if __name__ == "__main__":
    print("Generating 韬见 AI avatar candidates (3 directions)...")
    save_variant(design_A(), "A_pupil")
    save_variant(design_B(), "B_scope")
    save_variant(design_C(), "C_glyph")
    print("Done.")
