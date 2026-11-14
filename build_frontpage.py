#!/usr/bin/env python3
"""Build 'The Daily Meridian' newspaper front page for the news-image-01 entry.

All text is typeset programmatically with PIL (Liberation Serif) so every
word is spelled exactly as written in the copy below. Photos are AI artwork
with no lettering. Output: entry.png (JPEG bytes, 1024x1024).
"""
from PIL import Image, ImageDraw, ImageFont
import textwrap
import os

ART = os.path.expanduser("~/workspace/makefun/frontpage-art")
LEAD = os.path.join(ART, "media-generation-lead-repatriation-0-503a5842-7d27-40c7-9039-b5b29861c973.webp")
FIRE = os.path.join(ART, "media-generation-panel-forest-fire-0-5c326870-7e7e-4218-b81d-35593b81d9fd.webp")
PEACE = os.path.join(ART, "media-generation-panel-peace-table-0-becdd582-07dd-409c-84ef-fde0c5ea02d1.webp")
CHIP = os.path.join(ART, "media-generation-panel-cracked-chip-0-90f5f6a8-5893-44b2-9070-0bc56f4a79f5.webp")

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"

W = H = 1024
PAPER = (246, 240, 224)
INK = (18, 16, 12)

# ---------------- copy (verbatim) ----------------
MASTHEAD = "The Daily Meridian"
DATELINE = "JAKARTA EDITION \u2014 FRIDAY, 13 NOVEMBER 2026 \u2014 VOL. XIII, No. 13"
HEAD_L1 = "A SOLDIER COMES HOME"
HEAD_L2 = "AFTER EIGHTY YEARS"

LEAD_TEXT = (
    "A soldier who never came home has begun his last journey. At Halim "
    "Perdanakusuma Air Base on Friday, Indonesia and the United States held a "
    "solemn ceremony to return the remains of an American serviceman killed "
    "in the Second World War and recovered on Morotai Island, North Maluku. "
    "Morotai was a great Allied base from 1944, a stepping stone to the "
    "Philippines. The fallen soldier now flies to Hawaii for identification. "
    "Some 2,500 American personnel are still missing in Indonesia; the two "
    "nations have pledged to keep searching until every one of them is "
    "accounted for."
)

S2_HEAD = "FORESTS BURN, HAZE CHOKES THE ISLANDS"
S2_TEXT = (
    "Wildfires raging across Kalimantan and Sumatra have sent thick haze "
    "over cities and toward neighbouring countries, in one of the worst "
    "fire seasons in Indonesia's history. The government has refused to "
    "declare a national disaster even as support for the president falls."
)

S3_HEAD = "TALKS WIDEN AS DRONES FILL THE SKY"
S3_TEXT = (
    "Ukraine's peace talks widened to European security in Dublin on "
    "Friday, even as Kyiv launched one of its largest drone attacks of "
    "the war, some 1,200 drones against targets in Russia."
)

S4_HEAD = "CHIP GIANT'S CHIEF RESIGNS"
S4_TEXT = (
    "Nvidia chief executive Jensen Huang stepped down on Friday, sending "
    "technology shares lower and closing a turbulent week for the world's "
    "most valuable chipmaker."
)

S5_HEAD = "BRIEFING"
S5_TEXT = (
    "A global Microsoft 365 outage entered its second day, disrupting "
    "offices in dozens of countries. In the United States, a four-hour "
    "nationwide ground stop was lifted Friday evening after a "
    "communications failure. At the COP31 summit in Antalya, the UN chief "
    "urged drastic emissions cuts as climate finance pledges fell sharply."
)

# ---------------- helpers ----------------

def font(path, size):
    return ImageFont.truetype(path, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def wrap(draw, text, f, width):
    """Greedy word wrap by pixel width."""
    words = text.split()
    lines, cur = [], ""
    for wd in words:
        trial = wd if not cur else cur + " " + wd
        if text_w(draw, trial, f) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = wd
    if cur:
        lines.append(cur)
    return lines


def draw_justified(draw, lines, x, y, width, f, lh, ink=INK):
    """Draw wrapped lines, justified except the last line."""
    for i, line in enumerate(lines):
        if i < len(lines) - 1 and " " in line:
            words = line.split(" ")
            total_words_w = sum(text_w(draw, w, f) for w in words)
            gap = (width - total_words_w) / (len(words) - 1)
            cx = x
            for w in words:
                draw.text((cx, y), w, font=f, fill=ink)
                cx += text_w(draw, w, f) + gap
        else:
            draw.text((x, y), line, font=f, fill=ink)
        y += lh
    return y


def draw_centered(draw, s, cx, y, f, ink=INK):
    w = text_w(draw, s, f)
    draw.text((cx - w / 2, y), s, font=f, fill=ink)


def crop_to(img, tw, th, y_bias=0.5):
    """Center-crop image to aspect tw:th (y_bias 0=top, 1=bottom), resize."""
    iw, ih = img.size
    target = tw / th
    cur = iw / ih
    if cur > target:  # too wide
        nw = int(ih * target)
        x0 = (iw - nw) // 2
        box = (x0, 0, x0 + nw, ih)
    else:  # too tall
        nh = int(iw / target)
        y0 = int((ih - nh) * y_bias)
        box = (0, y0, iw, y0 + nh)
    return img.crop(box).resize((tw, th), Image.LANCZOS)


def photo(img_path, tw, th, y_bias=0.5):
    im = Image.open(img_path).convert("L").convert("RGB")
    return crop_to(im, tw, th, y_bias)


def rule(draw, x0, x1, y, thick=3, thin=1, gap=3):
    draw.rectangle([x0, y, x1, y + thick - 1], fill=INK)
    draw.rectangle([x0, y + thick + gap, x1, y + thick + gap + thin - 1], fill=INK)
    return y + thick + gap + thin


# ---------------- build ----------------

def build(body_size=16, verbose=True):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 30                      # side margin
    CW = W - 2 * M              # content width = 964
    body = font(SERIF, body_size)
    body_lh = int(body_size * 1.24)

    # masthead
    mast = font(SERIF_B, 58)
    draw_centered(d, MASTHEAD, W // 2, 14, mast)
    y = 14 + 66
    y = rule(d, M, M + CW, y) + 6

    # dateline
    dl = font(SERIF_B, 17)
    draw_centered(d, DATELINE, W // 2, y, dl)
    y += 26
    d.line([M, y, M + CW, y], fill=INK, width=1)
    y += 10

    # main headline
    hf = font(SERIF_B, 55)
    draw_centered(d, HEAD_L1, W // 2, y, hf)
    y += 64
    draw_centered(d, HEAD_L2, W // 2, y, hf)
    y += 72

    # lead section: photo left, article right
    lead_top = y
    PHOTO_W, PHOTO_H = 548, 264
    img.paste(photo(LEAD, PHOTO_W, PHOTO_H, y_bias=0.42), (M, lead_top))
    d.rectangle([M, lead_top, M + PHOTO_W - 1, lead_top + PHOTO_H - 1], outline=INK, width=2)

    tx = M + PHOTO_W + 18
    tw = M + CW - tx
    lines = wrap(d, LEAD_TEXT, body, tw)
    avail = PHOTO_H
    max_lines = avail // body_lh
    if verbose:
        print(f"lead: {len(lines)} lines, box fits {max_lines}")
    used = lines[:max_lines]
    draw_justified(d, used, tx, lead_top, tw, body, body_lh)
    rest = lines[max_lines:]
    y = lead_top + PHOTO_H + 10
    if rest:
        # continue in 3 columns under the photo
        colw = (CW - 2 * 16) // 3
        per = (len(rest) + 2) // 3
        for c in range(3):
            chunk = rest[c * per:(c + 1) * per]
            if chunk:
                draw_justified(d, chunk, M + c * (colw + 16), y, colw, body, body_lh)
        y += per * body_lh + 6
    y = rule(d, M, M + CW, y) + 8

    # stories row: 3 columns
    colw = (CW - 2 * 16) // 3
    stories = [
        (FIRE, 0.45, S2_HEAD, S2_TEXT),
        (PEACE, 0.35, S3_HEAD, S3_TEXT),
        (CHIP, 0.5, S4_HEAD, S4_TEXT),
    ]
    head_f = font(SERIF_B, 19)
    row_bottom = y
    PH2 = 118
    for i, (path, bias, head, text) in enumerate(stories):
        cx = M + i * (colw + 16)
        img.paste(photo(path, colw, PH2, y_bias=bias), (cx, y))
        d.rectangle([cx, y, cx + colw - 1, y + PH2 - 1], outline=INK, width=2)
        cy = y + PH2 + 8
        hlines = wrap(d, head, head_f, colw)
        for hl in hlines:
            d.text((cx, cy), hl, font=head_f, fill=INK)
            cy += 24
        cy += 3
        blines = wrap(d, text, body, colw)
        cy = draw_justified(d, blines, cx, cy, colw, body, body_lh)
        row_bottom = max(row_bottom, cy)
    y = rule(d, M, M + CW, row_bottom + 4) + 8

    # briefing
    bf = font(SERIF_B, 19)
    d.text((M, y), S5_HEAD, font=bf, fill=INK)
    hw = text_w(d, S5_HEAD, bf)
    blines = wrap(d, S5_TEXT, body, CW - hw - 14)
    draw_justified(d, blines, M + hw + 14, y + 2, CW - hw - 14, body, body_lh)
    y += max(26, len(blines) * body_lh) + 8
    y = rule(d, M, M + CW, y)

    if verbose:
        print(f"final bottom y = {y} (canvas {H})")
    return img, y


if __name__ == "__main__":
    img, bottom = build()
    assert bottom <= H - 6, f"overflow: bottom {bottom}"
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out, format="JPEG", quality=88)
    size = os.path.getsize(out)
    print(f"saved {out}: {size} bytes")
    with open(out, "rb") as fh:
        print("magic:", fh.read(3).hex())
