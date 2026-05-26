#!/usr/bin/env python3
"""
韬见 AI 头像 — 最终版（基于 A 瞳孔光圈方向细化）

精修要点：
1. 暖金调低饱和 → 更"古典金"而非"广告金"
2. 焦点小圆加 3 层渐变高光（极小幅 PIL 绘制实现）
3. "洞察缺口"角度收窄到 18°、移到右上 30° 位置（更克制）
4. K 线脉冲改为 5 根（黄金分割），降低饱和度
5. 外环加细微的"刻度点"6 个（罗盘暗示）
6. 输出尺寸：1024（高保真）/ 512（公众号上传标准）/ 256 / 144（列表小尺寸预览）
"""

from PIL import Image, ImageDraw, ImageFilter
from pathlib import Path
import random

OUT = Path(__file__).parent
SIZE = 1024

# 调整后的配色
NAVY_DEEP   = (15, 30, 61)
NAVY_MID    = (28, 49, 86)
NAVY_SOFT   = (62, 84, 122)       # 略提亮，让中环可见
GOLD        = (198, 152, 72)      # 比 D4A24C 低饱和（更古典）
GOLD_LIGHT  = (228, 192, 122)
GOLD_HI     = (248, 220, 168)     # 高光
TEAL        = (72, 168, 156)      # 略低饱和的青
WHITE_SOFT  = (245, 240, 230)


def make_canvas():
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))


def fill_disk(img, color):
    ImageDraw.Draw(img).ellipse([0, 0, SIZE, SIZE], fill=color)


def add_grain(img, opacity=12):
    grain = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(grain)
    rnd = random.Random(2026)
    for y in range(0, SIZE, 2):
        for x in range(0, SIZE, 2):
            v = rnd.randint(0, 60)
            if v > 52:
                d.point((x, y), fill=(255, 255, 255, opacity))
            elif v < 5:
                d.point((x, y), fill=(0, 0, 0, opacity))
    return Image.alpha_composite(img, grain)


def add_radial_glow(img, cx, cy, r, color, intensity=40):
    """A soft radial glow centered at (cx,cy) — for the pupil halo."""
    glow = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(glow)
    for i, rad in enumerate(range(r, r // 3, -2)):
        alpha = int(intensity * (1 - i / ((r - r // 3) / 2)))
        alpha = max(0, min(255, alpha))
        d.ellipse([cx - rad, cy - rad, cx + rad, cy + rad],
                  fill=color + (alpha // 8,))
    glow = glow.filter(ImageFilter.GaussianBlur(radius=20))
    return Image.alpha_composite(img, glow)


def design_final():
    img = make_canvas()
    fill_disk(img, NAVY_DEEP)
    cx, cy = SIZE // 2, SIZE // 2

    # —— 1) 瞳孔金色 halo（背景柔光，先于环绘制）——
    img = add_radial_glow(img, cx, cy, int(SIZE * 0.32), GOLD, intensity=80)

    d = ImageDraw.Draw(img)

    # —— 2) 三层同心环 ——
    # 外环：暖金细线，4px
    outer_r = int(SIZE * 0.455)
    d.ellipse([cx - outer_r, cy - outer_r, cx + outer_r, cy + outer_r],
              outline=GOLD, width=4)

    # 外环"洞察缺口"：右上 18° 区间断开（用背景色覆盖一段弧）
    gap_pad = 7
    d.pieslice([cx - outer_r - gap_pad, cy - outer_r - gap_pad,
                cx + outer_r + gap_pad, cy + outer_r + gap_pad],
               start=-39, end=-21, fill=NAVY_DEEP)

    # 中环：柔蓝，3px
    mid_r = int(SIZE * 0.355)
    d.ellipse([cx - mid_r, cy - mid_r, cx + mid_r, cy + mid_r],
              outline=NAVY_SOFT, width=3)

    # 内环：柔蓝细线，2px
    inn_r = int(SIZE * 0.255)
    d.ellipse([cx - inn_r, cy - inn_r, cx + inn_r, cy + inn_r],
              outline=NAVY_SOFT, width=2)

    # —— 3) 外环刻度点（6 个，罗盘暗示，避开缺口位置）——
    # 缺口在 -30°（即 12 点钟方向偏右上），避开 -45° ~ -15°
    tick_angles_deg = [0, 60, 120, 180, 240, 300]
    import math
    for ang_deg in tick_angles_deg:
        # 跳过缺口附近
        if -45 <= ang_deg - 360 <= -15 or -45 <= ang_deg <= -15:
            continue
        ang = math.radians(ang_deg - 90)  # 0° 在顶部
        x = cx + int(outer_r * math.cos(ang))
        y = cy + int(outer_r * math.sin(ang))
        r = 5
        d.ellipse([x - r, y - r, x + r, y + r], fill=GOLD_LIGHT)

    # —— 4) 中心瞳孔金色实心圆 ——
    pupil_r = int(SIZE * 0.088)
    # 主体
    d.ellipse([cx - pupil_r, cy - pupil_r, cx + pupil_r, cy + pupil_r],
              fill=GOLD)
    # 中层柔光圈（径向渐变模拟）
    for i in range(8):
        rr = pupil_r - i * 2
        if rr <= 0: break
        alpha = 18 - i * 2
        if alpha <= 0: break
        ov = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
        ImageDraw.Draw(ov).ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                                   fill=GOLD_LIGHT + (alpha,))
        img = Image.alpha_composite(img, ov)
        d = ImageDraw.Draw(img)

    # 高光（左上小亮点）
    hi_r = int(pupil_r * 0.30)
    hi_x = cx - int(pupil_r * 0.32)
    hi_y = cy - int(pupil_r * 0.32)
    # 双层高光：底层柔，上层硬
    ov = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    ImageDraw.Draw(ov).ellipse([hi_x - hi_r - 4, hi_y - hi_r - 4,
                                 hi_x + hi_r + 4, hi_y + hi_r + 4],
                                fill=GOLD_HI + (120,))
    ov = ov.filter(ImageFilter.GaussianBlur(radius=4))
    img = Image.alpha_composite(img, ov)
    d = ImageDraw.Draw(img)
    d.ellipse([hi_x - hi_r, hi_y - hi_r, hi_x + hi_r, hi_y + hi_r],
              fill=GOLD_HI)

    # —— 5) 底部 K 线脉冲（5 根，黄金分割等高比，更克制）——
    bars = [
        (-2, 0.040),
        (-1, 0.062),
        (0,  0.048),
        (1,  0.080),
        (2,  0.052),
    ]
    bar_w = 7
    bar_gap = 5
    base_y = cy + int(SIZE * 0.355)
    bar_color = TEAL + (200,)
    ov = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for off, h in bars:
        x = cx + off * (bar_w + bar_gap)
        hh = int(SIZE * h)
        od.rectangle([x - bar_w // 2, base_y - hh, x + bar_w // 2, base_y],
                     fill=bar_color)
    img = Image.alpha_composite(img, ov)

    # —— 6) 颗粒 + 暗角 ——
    img = add_grain(img, 10)

    # 暗角
    vg = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    vd = ImageDraw.Draw(vg)
    max_r = int(SIZE * 0.50)
    for r in range(max_r, max_r - 80, -1):
        t = (max_r - r) / 80
        alpha = int(60 * (1 - t))
        vd.ellipse([cx - r, cy - r, cx + r, cy + r],
                   outline=(0, 0, 0, alpha), width=1)
    img = Image.alpha_composite(img, vg)

    return img


def save_multi_size(img, basename):
    sizes = [(1024, "1024"), (512, "512"), (256, "256"), (144, "144"), (64, "64")]
    for s, tag in sizes:
        out = img.resize((s, s), Image.LANCZOS)
        out.save(OUT / f"{basename}_{tag}.png", "PNG")
    print(f"saved {basename}_{{1024,512,256,144,64}}.png")


def build_preview_sheet(basename):
    """Show the avatar in multiple WeChat-realistic contexts side-by-side."""
    W, H = 1400, 700
    canvas = Image.new("RGB", (W, H), (245, 245, 245))
    d = ImageDraw.Draw(canvas)

    try:
        from PIL import ImageFont
        title_fnt = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 28)
        sub_fnt = ImageFont.truetype("/System/Library/Fonts/PingFang.ttc", 18)
    except:
        from PIL import ImageFont
        title_fnt = ImageFont.load_default()
        sub_fnt = ImageFont.load_default()

    contexts = [
        (512, "公众号头像（512×512 上传规格）", 100),
        (200, "推文列表头部头像", 700),
        (96,  "聊天列表内", 1050),
        (40,  "评论区头像", 1230),
    ]

    for s, label, cx in contexts:
        img = Image.open(OUT / f"{basename}_1024.png").resize((s, s), Image.LANCZOS)
        # 圆形 mask
        mask = Image.new("L", (s, s), 0)
        ImageDraw.Draw(mask).ellipse((0, 0, s, s), fill=255)
        x = cx - s // 2
        y = 120 + (180 - s // 2 if s < 200 else 0)
        canvas.paste(img, (x, y), mask)
        d.text((cx, 380), f"{s}×{s}", font=title_fnt, fill=(15, 30, 61), anchor="mt")
        d.text((cx, 415), label, font=sub_fnt, fill=(82, 96, 116), anchor="mt")

    # 顶部标题
    d.text((W // 2, 30), "「韬见 AI」最终头像 — 多场景预览", font=title_fnt, fill=(15, 30, 61), anchor="mt")
    d.text((W // 2, 75), "深靛蓝 + 古典金 + 微 K 线脉冲 · 同心环 + 罗盘刻度 + 洞察缺口", font=sub_fnt, fill=(82, 96, 116), anchor="mt")

    # 底部说明
    notes = [
        "✓ 圆形容器（微信默认 mask 兼容）",
        "✓ 中心金色焦点 = 洞见的视觉锚点",
        "✓ 外环右上'缺口' = 主动留白，暗示'看见未被看见的'",
        "✓ 底部 K 线 = 资本/数据，呼应'投资线索'定位",
    ]
    for i, n in enumerate(notes):
        d.text((100, 500 + i * 35), n, font=sub_fnt, fill=(52, 76, 114))

    canvas.save(OUT / f"{basename}_preview.png")
    print(f"saved {basename}_preview.png")


if __name__ == "__main__":
    img = design_final()
    save_multi_size(img, "final_A")
    build_preview_sheet("final_A")
