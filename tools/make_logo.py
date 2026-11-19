"""Regenerate the LeanEdge logo SVGs.

The mark is redrawn from Elias's original logo (geometry traced from the JPEG).
The wordmark is "LeanEdge" in Inter Bold, converted to outlines so the SVG
does not depend on any installed font.

Run from the repo root:  python tools/make_logo.py
Needs: pip install fonttools brotli
"""
import os
from pathlib import Path

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
OUT = Path(os.environ["LOGO_OUT"]) if "LOGO_OUT" in os.environ else IMG

WEIGHT = os.environ.get("LOGO_WEIGHT", "700")
FONT = ROOT / "assets" / "fonts" / f"inter-latin-{WEIGHT}-normal.woff2"

NAVY = "#011B3C"
WHITE = "#FFFFFF"
WORD = "LeanEdge"

# ---------------------------------------------------------------- mark
# Coordinates traced from the original 508x334 JPEG (mark box x 152..331, y 30..182).
K = 0.7  # slope of both diagonals (dx per dy)
MARK_POLYS = [
    # top bar, both ends cut on the diagonal
    [(152, 30), (331, 30), (331 - K * 20, 50), (152 + K * 20, 50)],
    # upper-left diagonal, running down-right until it meets the long stroke
    [(152, 30), (184, 30), (257, 137.3), (227.1, 137.3)],
    # long stroke from the right arm down-left to the bottom bar
    [(263, 86), (293, 86), (293 - K * 96, 182), (263 - K * 96, 182)],
    # bottom bar, left end cut on the diagonal
    [(263 - K * 76, 162), (323, 162), (323, 182), (263 - K * 96, 182)],
]
MARK_BOX = (152, 30, 331, 182)  # x0, y0, x1, y1
MARK_W = MARK_BOX[2] - MARK_BOX[0]
MARK_H = MARK_BOX[3] - MARK_BOX[1]


def mark_path(dx=0.0, dy=0.0, scale=1.0):
    parts = []
    for poly in MARK_POLYS:
        pts = [((x - MARK_BOX[0]) * scale + dx, (y - MARK_BOX[1]) * scale + dy) for x, y in poly]
        parts.append("M" + " L".join(f"{x:.2f} {y:.2f}" for x, y in pts) + " Z")
    return " ".join(parts)


# ---------------------------------------------------------------- wordmark
font = TTFont(FONT)
glyphs = font.getGlyphSet()
cmap = font.getBestCmap()
CAP = font["OS/2"].sCapHeight  # 1490 units
TRACK = -0.012 * CAP  # slight tightening, matched to the original letter spacing


def word_path(x, y_baseline, cap_px):
    """Path for WORD with its cap height = cap_px and baseline at y_baseline. Returns (d, width_px)."""
    s = cap_px / CAP
    pen = SVGPathPen(glyphs)
    cursor = 0.0
    first_lsb = None
    last_right = 0.0
    for i, ch in enumerate(WORD):
        name = cmap[ord(ch)]
        bp = BoundsPen(glyphs)
        glyphs[name].draw(bp)
        if first_lsb is None:
            first_lsb = bp.bounds[0]
        tp = TransformPen(pen, (s, 0, 0, -s, x + (cursor - first_lsb) * s, y_baseline))
        glyphs[name].draw(tp)
        last_right = cursor + bp.bounds[2]
        cursor += font["hmtx"][name][0] + (TRACK if i < len(WORD) - 1 else 0)
    return pen.getCommands(), (last_right - first_lsb) * s


def svg(w, h, body, title):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {h:.2f}" '
        f'role="img" aria-labelledby="t">\n<title id="t">{title}</title>\n{body}\n</svg>\n'
    )


def write(name, text):
    (OUT / name).write_text(text, encoding="utf-8")
    print("wrote", name)


# Stacked logo, proportions from the original: cap = 69, mark height 152, gap 47.
CAP_PX = 69
_, word_w = word_path(0, 0, CAP_PX)
W = word_w
mark_x = (W - MARK_W) / 2
gap = 47
H = MARK_H + gap + CAP_PX + 24  # 24 = room for the g descender
for color, suffix in ((NAVY, ""), (WHITE, "-white")):
    wd, _ = word_path(0, MARK_H + gap + CAP_PX, CAP_PX)
    body = f'<g fill="{color}"><path d="{mark_path(mark_x, 0)}"/><path d="{wd}"/></g>'
    write(f"logo{suffix}.svg", svg(W, H, body, "LeanEdge"))

# Mark only
for color, suffix in ((NAVY, ""), (WHITE, "-white")):
    write(f"logo-mark{suffix}.svg", svg(MARK_W, MARK_H, f'<path fill="{color}" d="{mark_path()}"/>', "LeanEdge"))

# Horizontal lockup for the site header: mark height = 1.55 x cap height.
hcap = 69
hs = hcap * 1.55 / MARK_H
mw, mh = MARK_W * hs, MARK_H * hs
hgap = hcap * 0.55
baseline = (mh + hcap) / 2
for color, suffix in ((NAVY, ""), (WHITE, "-white")):
    wd, ww = word_path(mw + hgap, baseline, hcap)
    body = f'<g fill="{color}"><path d="{mark_path(0, 0, hs)}"/><path d="{wd}"/></g>'
    write(f"logo-horizontal{suffix}.svg", svg(mw + hgap + ww, max(mh, baseline + 24), body, "LeanEdge"))

# Favicon: white mark on a navy rounded square
size = 64
fs = 40 / MARK_H
fx = (size - MARK_W * fs) / 2
fy = (size - MARK_H * fs) / 2
fav = (
    f'<rect width="{size}" height="{size}" rx="12" fill="{NAVY}"/>'
    f'<path fill="{WHITE}" d="{mark_path(fx, fy, fs)}"/>'
)
write("favicon.svg", svg(size, size, fav, "LeanEdge"))


# ---------------------------------------------------------------- PNG icons (Pillow, 8x supersampled)
def png_icon(name, size, rounded):
    from PIL import Image, ImageDraw

    ss = 8
    big = size * ss
    im = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    navy = tuple(int(NAVY[i:i + 2], 16) for i in (1, 3, 5))
    if rounded:
        d.rounded_rectangle((0, 0, big - 1, big - 1), radius=int(big * 12 / 64), fill=navy)
    else:
        d.rectangle((0, 0, big, big), fill=navy)
    s = big * (40 / 64 if rounded else 0.56) / MARK_H
    ox = (big - MARK_W * s) / 2
    oy = (big - MARK_H * s) / 2
    for poly in MARK_POLYS:
        d.polygon([((x - MARK_BOX[0]) * s + ox, (y - MARK_BOX[1]) * s + oy) for x, y in poly], fill="white")
    im.resize((size, size), Image.LANCZOS).save(OUT / name)
    print("wrote", name)


png_icon("favicon-32.png", 32, rounded=True)
png_icon("apple-touch-icon.png", 180, rounded=False)
