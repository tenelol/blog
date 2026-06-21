#!/usr/bin/env python3
"""
ブログ記事のサムネイル画像を生成するスクリプト。
Blowfish テーマ用に 1200x630 の OGP サイズ画像を作る。

デザイン: アブストラクト + ジオメトリ
- 大きなグラデーション blob を背景に配置
- 幾何学的なアクセント（三角形、円弧、ドット列）
- テキストはクリーンなレイアウトで左寄せ

Usage:
    python generate_thumbnail.py --title "記事タイトル" --tags "tag1,tag2" --output path/to/featured.png
"""

import argparse
import hashlib
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

WIDTH, HEIGHT = 1200, 630

# カラーパレット（タイトルのハッシュで決定的に選ぶ）
PALETTES = [
    {
        "bg": (8, 8, 18),
        "blob1": (20, 80, 180),
        "blob2": (120, 40, 200),
        "accent": (100, 200, 255),
        "accent2": (180, 120, 255),
        "text": (245, 245, 250),
        "text_sub": (160, 170, 190),
    },
    {
        "bg": (12, 6, 18),
        "blob1": (160, 30, 120),
        "blob2": (60, 20, 160),
        "accent": (255, 120, 200),
        "accent2": (200, 100, 255),
        "text": (245, 245, 250),
        "text_sub": (180, 160, 185),
    },
    {
        "bg": (6, 14, 14),
        "blob1": (10, 120, 100),
        "blob2": (20, 60, 160),
        "accent": (60, 240, 200),
        "accent2": (80, 180, 255),
        "text": (245, 245, 250),
        "text_sub": (150, 185, 180),
    },
    {
        "bg": (14, 8, 6),
        "blob1": (160, 60, 20),
        "blob2": (180, 30, 80),
        "accent": (255, 160, 80),
        "accent2": (255, 100, 140),
        "text": (245, 245, 250),
        "text_sub": (190, 170, 155),
    },
    {
        "bg": (6, 10, 20),
        "blob1": (30, 60, 180),
        "blob2": (10, 140, 130),
        "accent": (80, 180, 255),
        "accent2": (60, 230, 200),
        "text": (245, 245, 250),
        "text_sub": (150, 170, 190),
    },
    {
        "bg": (10, 6, 16),
        "blob1": (100, 20, 160),
        "blob2": (180, 50, 60),
        "accent": (200, 120, 255),
        "accent2": (255, 100, 120),
        "text": (245, 245, 250),
        "text_sub": (175, 155, 185),
    },
]


def pick_palette(title: str) -> dict:
    h = int(hashlib.md5(title.encode()).hexdigest(), 16)
    return PALETTES[h % len(PALETTES)]


def lerp_color(c1, c2, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def draw_gradient_bg(img: Image.Image, palette: dict):
    """微かな対角グラデーション背景"""
    draw = ImageDraw.Draw(img)
    bg = palette["bg"]
    for y in range(HEIGHT):
        t = y / HEIGHT
        c = lerp_color(bg, tuple(min(v + 12, 255) for v in bg), t * 0.6)
        draw.line([(0, y), (WIDTH, y)], fill=c)


def draw_blobs(img: Image.Image, palette: dict, seed: int):
    """大きなぼかしblob を右側に配置（テキスト領域を避ける）"""
    rng = random.Random(seed)
    blob_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    blob_draw = ImageDraw.Draw(blob_layer)

    blob_configs = [
        {
            "color": palette["blob1"],
            "cx": rng.randint(WIDTH // 2 + 100, WIDTH + 80),
            "cy": rng.randint(-60, HEIGHT // 2),
            "rx": rng.randint(250, 400),
            "ry": rng.randint(200, 350),
            "alpha": rng.randint(50, 80),
        },
        {
            "color": palette["blob2"],
            "cx": rng.randint(WIDTH // 2 - 50, WIDTH - 100),
            "cy": rng.randint(HEIGHT // 2, HEIGHT + 80),
            "rx": rng.randint(200, 380),
            "ry": rng.randint(180, 320),
            "alpha": rng.randint(40, 70),
        },
        {
            "color": lerp_color(palette["blob1"], palette["blob2"], 0.5),
            "cx": rng.randint(WIDTH // 3, WIDTH // 2 + 100),
            "cy": rng.randint(HEIGHT // 4, HEIGHT * 3 // 4),
            "rx": rng.randint(150, 280),
            "ry": rng.randint(130, 250),
            "alpha": rng.randint(25, 45),
        },
    ]

    for b in blob_configs:
        c = b["color"]
        blob_draw.ellipse(
            [b["cx"] - b["rx"], b["cy"] - b["ry"],
             b["cx"] + b["rx"], b["cy"] + b["ry"]],
            fill=(*c, b["alpha"]),
        )

    # 大きめにぼかす
    blob_layer = blob_layer.filter(ImageFilter.GaussianBlur(radius=90))
    img_rgba = img.convert("RGBA")
    composite = Image.alpha_composite(img_rgba, blob_layer)
    img.paste(composite.convert("RGB"))


def draw_geometric_accents(draw: ImageDraw.Draw, palette: dict, seed: int):
    """幾何学的なアクセント要素"""
    rng = random.Random(seed + 100)
    accent = palette["accent"]
    accent2 = palette["accent2"]

    # --- 細いアーク（円弧）を右上と左下に ---
    for _ in range(rng.randint(2, 4)):
        cx = rng.randint(WIDTH // 2, WIDTH + 100)
        cy = rng.randint(-100, HEIGHT // 3)
        r = rng.randint(150, 350)
        start = rng.randint(0, 180)
        end = start + rng.randint(40, 120)
        arc_color = lerp_color(palette["bg"], accent if rng.random() > 0.5 else accent2, 0.2)
        draw.arc([cx - r, cy - r, cx + r, cy + r], start, end, fill=arc_color, width=2)

    # --- ドット列（等間隔のドットがラインを形成） ---
    for _ in range(rng.randint(2, 4)):
        sx = rng.randint(WIDTH // 2, WIDTH - 100)
        sy = rng.randint(50, HEIGHT - 50)
        angle = rng.uniform(-0.5, 0.5)
        dot_count = rng.randint(5, 15)
        spacing = rng.randint(18, 35)
        dot_color = lerp_color(palette["bg"], accent2, rng.uniform(0.15, 0.35))
        for i in range(dot_count):
            dx = sx + int(i * spacing * math.cos(angle))
            dy = sy + int(i * spacing * math.sin(angle))
            r = rng.choice([2, 2, 3])
            draw.ellipse([dx - r, dy - r, dx + r, dy + r], fill=dot_color)

    # --- 三角形のアウトライン ---
    for _ in range(rng.randint(1, 3)):
        cx = rng.randint(WIDTH // 2 + 50, WIDTH - 80)
        cy = rng.randint(80, HEIGHT - 80)
        size = rng.randint(30, 90)
        rotation = rng.uniform(0, math.pi * 2)
        tri_color = lerp_color(palette["bg"], accent, rng.uniform(0.1, 0.25))
        points = []
        for k in range(3):
            a = rotation + k * (2 * math.pi / 3)
            points.append((cx + size * math.cos(a), cy + size * math.sin(a)))
        draw.polygon(points, outline=tri_color)

    # --- 細い水平ライン（テキスト下あたり） ---
    line_y = rng.randint(HEIGHT - 120, HEIGHT - 60)
    line_color = lerp_color(palette["bg"], accent, 0.15)
    draw.line([(60, line_y), (WIDTH // 2 - 40, line_y)], fill=line_color, width=1)

    # --- 小さな十字マーク ---
    for _ in range(rng.randint(3, 6)):
        cx = rng.randint(100, WIDTH - 60)
        cy = rng.randint(40, HEIGHT - 40)
        s = rng.randint(4, 8)
        cross_color = lerp_color(palette["bg"], accent2, rng.uniform(0.08, 0.2))
        draw.line([(cx - s, cy), (cx + s, cy)], fill=cross_color, width=1)
        draw.line([(cx, cy - s), (cx, cy + s)], fill=cross_color, width=1)


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

    # 1. グラデーション背景
    draw_gradient_bg(img, palette)

    # 2. Blob（ぼかし）
    draw_blobs(img, palette, seed)

    # 3. 幾何学アクセント
    draw = ImageDraw.Draw(img)
    draw_geometric_accents(draw, palette, seed)

    # 4. テキスト配置
    title_font = load_font(46, bold=True)
    tag_font = load_font(17, bold=False)
    site_font = load_font(15, bold=False)

    max_text_width = WIDTH // 2 + 80
    title_lines = wrap_title(title, title_font, max_text_width)

    line_height = 64
    total_title_height = len(title_lines) * line_height

    # テキスト開始位置（左寄せ、垂直中央）
    text_x = 70
    title_y_start = (HEIGHT - total_title_height) // 2 - 20

    # アクセントバー（タイトル左の細い縦線、グラデーション）
    bar_top = title_y_start + 4
    bar_bottom = title_y_start + total_title_height - 8
    for y in range(int(bar_top), int(bar_bottom)):
        t = (y - bar_top) / max(bar_bottom - bar_top, 1)
        c = lerp_color(palette["accent"], palette["accent2"], t)
        draw.line([(text_x - 16, y), (text_x - 12, y)], fill=c)

    # タイトル描画（影付き）
    for i, line in enumerate(title_lines):
        y = title_y_start + i * line_height
        draw.text((text_x + 2, y + 2), line, fill=(0, 0, 0), font=title_font)
        draw.text((text_x, y), line, fill=palette["text"], font=title_font)

    # タグ描画
    tag_y = title_y_start + total_title_height + 18
    tag_x = text_x
    for tag in tags[:4]:
        label = f"#{tag}"
        bbox = tag_font.getbbox(label)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        pill_h = th + 12
        pill_w = tw + 18
        pill_color = lerp_color(palette["bg"], palette["accent"], 0.15)
        draw.rounded_rectangle(
            [tag_x, tag_y, tag_x + pill_w, tag_y + pill_h],
            radius=pill_h // 2,
            fill=pill_color,
        )
        outline_color = lerp_color(palette["bg"], palette["accent"], 0.3)
        draw.rounded_rectangle(
            [tag_x, tag_y, tag_x + pill_w, tag_y + pill_h],
            radius=pill_h // 2,
            outline=outline_color,
            width=1,
        )
        draw.text((tag_x + 9, tag_y + 5), label, fill=palette["text_sub"], font=tag_font)
        tag_x += pill_w + 10
        if tag_x > max_text_width:
            break

    # サイト名（右下、控えめに）
    site_text = "tenelol.dev"
    bbox = site_font.getbbox(site_text)
    sw = bbox[2] - bbox[0]
    draw.text(
        (WIDTH - sw - 40, HEIGHT - 38),
        site_text,
        fill=lerp_color(palette["text_sub"], palette["bg"], 0.3),
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
