#!/usr/bin/env python3
"""
ブログ記事のサムネイル画像を生成するスクリプト。
Blowfish テーマ用に 1200x630 の OGP サイズ画像を作る。

Usage:
    python generate_thumbnail.py --title "記事タイトル" --tags "tag1,tag2" --output path/to/featured.png
    python generate_thumbnail.py --title "記事タイトル" --tags "tag1,tag2" --output path/to/featured.png --style dark
"""

import argparse
import hashlib
import math
import random
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1200, 630

# カラーパレット（タイトルのハッシュで決定的に選ぶ）
PALETTES = [
    {"bg": (15, 15, 35), "accent": (0, 200, 150), "accent2": (0, 120, 220), "text": (240, 240, 245)},
    {"bg": (10, 10, 30), "accent": (255, 100, 80), "accent2": (255, 180, 50), "text": (240, 240, 245)},
    {"bg": (20, 10, 35), "accent": (160, 80, 255), "accent2": (80, 180, 255), "text": (240, 240, 245)},
    {"bg": (5, 20, 20), "accent": (0, 220, 180), "accent2": (0, 160, 255), "text": (240, 240, 245)},
    {"bg": (25, 10, 10), "accent": (255, 80, 120), "accent2": (255, 150, 80), "text": (240, 240, 245)},
    {"bg": (10, 15, 30), "accent": (60, 180, 255), "accent2": (120, 80, 255), "text": (240, 240, 245)},
]


def pick_palette(title: str) -> dict:
    h = int(hashlib.md5(title.encode()).hexdigest(), 16)
    return PALETTES[h % len(PALETTES)]


def lerp_color(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def draw_grid_pattern(draw: ImageDraw.Draw, palette: dict, seed: int):
    """テック感のあるグリッド + ノード + 接続線を描画"""
    rng = random.Random(seed)
    accent = palette["accent"]
    accent2 = palette["accent2"]

    # 薄いグリッド線
    grid_color = lerp_color(palette["bg"], (60, 60, 80), 0.3)
    step = 60
    for x in range(0, WIDTH, step):
        opacity = rng.randint(20, 60)
        c = lerp_color(palette["bg"], grid_color, opacity / 100)
        draw.line([(x, 0), (x, HEIGHT)], fill=c, width=1)
    for y in range(0, HEIGHT, step):
        opacity = rng.randint(20, 60)
        c = lerp_color(palette["bg"], grid_color, opacity / 100)
        draw.line([(0, y), (WIDTH, y)], fill=c, width=1)

    # ランダムなノードと接続線
    nodes = []
    for _ in range(rng.randint(12, 22)):
        x = rng.randint(50, WIDTH - 50)
        y = rng.randint(50, HEIGHT - 50)
        nodes.append((x, y))

    # 接続線（近いノード同士を結ぶ）
    for i, (x1, y1) in enumerate(nodes):
        for x2, y2 in nodes[i + 1:]:
            dist = math.hypot(x2 - x1, y2 - y1)
            if dist < 250:
                alpha = max(0.05, 0.25 - dist / 1000)
                line_color = lerp_color(palette["bg"], accent if rng.random() > 0.4 else accent2, alpha)
                draw.line([(x1, y1), (x2, y2)], fill=line_color, width=1)

    # ノードの描画
    for x, y in nodes:
        r = rng.randint(2, 5)
        node_color = lerp_color(accent, accent2, rng.random())
        alpha = rng.uniform(0.3, 0.8)
        c = lerp_color(palette["bg"], node_color, alpha)
        draw.ellipse([x - r, y - r, x + r, y + r], fill=c)

    # コーナーにグロウ効果
    for _ in range(3):
        cx = rng.choice([rng.randint(0, 200), rng.randint(WIDTH - 200, WIDTH)])
        cy = rng.choice([rng.randint(0, 150), rng.randint(HEIGHT - 150, HEIGHT)])
        for radius in range(120, 0, -2):
            alpha = 0.02 * (1 - radius / 120)
            c = lerp_color(palette["bg"], accent if rng.random() > 0.5 else accent2, alpha)
            draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=c)


def draw_floating_shapes(draw: ImageDraw.Draw, palette: dict, seed: int):
    """浮遊する幾何学模様"""
    rng = random.Random(seed + 42)
    accent = palette["accent"]
    accent2 = palette["accent2"]

    for _ in range(rng.randint(4, 8)):
        shape = rng.choice(["circle", "rect", "diamond"])
        x = rng.randint(50, WIDTH - 50)
        y = rng.randint(50, HEIGHT - 50)
        size = rng.randint(20, 80)
        alpha = rng.uniform(0.05, 0.15)
        c = lerp_color(palette["bg"], rng.choice([accent, accent2]), alpha)

        if shape == "circle":
            draw.ellipse([x - size, y - size, x + size, y + size], outline=c, width=2)
        elif shape == "rect":
            draw.rectangle([x - size, y - size, x + size, y + size], outline=c, width=2)
        elif shape == "diamond":
            points = [(x, y - size), (x + size, y), (x, y + size), (x - size, y)]
            draw.polygon(points, outline=c)


def load_font(size: int, bold: bool = False):
    """日本語フォントを読み込む"""
    font_paths = [
        # Linux (sandbox)
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc" if bold
        else "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        # macOS
        "/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc" if bold
        else "/System/Library/Fonts/ヒラギノ角ゴシック W3.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        # Fallback
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold
        else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for p in font_paths:
        try:
            return ImageFont.truetype(p, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def wrap_title(title: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    """タイトルをピクセル幅で折り返す"""
    lines = []
    current = ""
    for ch in title:
        test = current + ch
        bbox = font.getbbox(test)
        w = bbox[2] - bbox[0]
        if w > max_width and current:
            lines.append(current)
            current = ch
        else:
            current = test
    if current:
        lines.append(current)
    return lines[:4]  # 最大4行


def generate_thumbnail(title: str, tags: list[str], output_path: str):
    palette = pick_palette(title)
    seed = int(hashlib.md5(title.encode()).hexdigest()[:8], 16)

    img = Image.new("RGB", (WIDTH, HEIGHT), palette["bg"])
    draw = ImageDraw.Draw(img)

    # 背景パターン
    draw_grid_pattern(draw, palette, seed)
    draw_floating_shapes(draw, palette, seed)

    # 下部にグラデーション帯
    for y in range(HEIGHT - 200, HEIGHT):
        t = (y - (HEIGHT - 200)) / 200
        c = lerp_color(palette["bg"], (0, 0, 0), t * 0.5)
        draw.line([(0, y), (WIDTH, y)], fill=c)

    # タイトル描画
    title_font = load_font(44, bold=True)
    max_text_width = WIDTH - 140
    title_lines = wrap_title(title, title_font, max_text_width)

    # タイトル位置（中央やや上）
    line_height = 60
    total_title_height = len(title_lines) * line_height
    title_y_start = (HEIGHT - total_title_height) // 2 - 30

    # タイトル背景の半透明帯
    pad = 30
    bg_top = title_y_start - pad
    bg_bottom = title_y_start + total_title_height + pad + 60  # タグ分のスペース
    overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    overlay_draw = ImageDraw.Draw(overlay)
    overlay_draw.rectangle(
        [40, bg_top, WIDTH - 40, bg_bottom],
        fill=(*palette["bg"], 180),
    )
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # アクセント線（タイトル左端）
    draw.rectangle(
        [55, bg_top + 15, 60, bg_bottom - 15],
        fill=palette["accent"],
    )

    for i, line in enumerate(title_lines):
        y = title_y_start + i * line_height
        draw.text((80, y), line, fill=palette["text"], font=title_font)

    # タグ描画
    tag_font = load_font(20, bold=False)
    tag_y = title_y_start + total_title_height + 10
    tag_x = 80
    for tag in tags[:5]:
        label = f"#{tag}"
        bbox = tag_font.getbbox(label)
        tw = bbox[2] - bbox[0]
        tag_bg_color = lerp_color(palette["bg"], palette["accent"], 0.2)
        draw.rounded_rectangle(
            [tag_x - 6, tag_y - 4, tag_x + tw + 6, tag_y + 28],
            radius=4,
            fill=tag_bg_color,
        )
        draw.text((tag_x, tag_y), label, fill=palette["accent"], font=tag_font)
        tag_x += tw + 20
        if tag_x > WIDTH - 100:
            break

    # サイト名（右下）
    site_font = load_font(18, bold=False)
    site_text = "tenelol.dev"
    bbox = site_font.getbbox(site_text)
    sw = bbox[2] - bbox[0]
    draw.text(
        (WIDTH - sw - 50, HEIGHT - 45),
        site_text,
        fill=lerp_color(palette["text"], palette["bg"], 0.4),
        font=site_font,
    )

    # 保存
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, "PNG", optimize=True)
    print(f"Generated: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate blog thumbnail")
    parser.add_argument("--title", required=True, help="記事タイトル")
    parser.add_argument("--tags", default="", help="カンマ区切りタグ")
    parser.add_argument("--output", required=True, help="出力パス")
    args = parser.parse_args()

    tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    generate_thumbnail(args.title, tags, args.output)


if __name__ == "__main__":
    main()
