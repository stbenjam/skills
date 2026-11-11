#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pillow"]
# ///
"""Small box diagrams in the Terminal Bench figure style, laid out by hand.

Copy this file next to the document it illustrates, fill in ``DIAGRAMS`` and run
it. For every entry it writes, beside itself:

    <slug>.svg        one file, follows the viewer's light or dark mode
    <slug>.png        light
    <slug>-dark.png   dark

    uv run diagrams.py            # render DIAGRAMS
    uv run diagrams.py --example  # render the built-in example instead
    uv run diagrams.py --out DIR  # write somewhere else

Plain ``python3`` works too when Pillow is installed. The PNG renderer needs a
real font file: Google Sans Code, or Adwaita Mono or DejaVu Sans Mono.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# The drawing is 520 units wide, like the originals, and scaled up for PNG.
W = 520
PNG_SCALE = 3

# Figure frame around the drawing: 1px border, padding, caption row.
PAD_TOP, PAD_SIDE, PAD_BOTTOM = 20, 24, 16
CAPTION_SIZE = 14.5
CAPTION_H = 23  # caption line plus its 6px gap

TEXT_SIZE = 12
STROKE = 1
HEAD = 7
LINE_STEP = 1.3

# Theme tokens: light and dark.
THEMES = {
    "light": {
        "background": "#ffffff",
        "foreground": "#09090b",
        "muted": "#f4f4f5",
        "border": "#e4e4e7",
        "muted_fg": "#71717b",
        "node": "#d7d7d8",  # color-mix(#525252 18%, muted)
    },
    "dark": {
        "background": "#09090b",
        "foreground": "#fafafa",
        "muted": "#27272a",
        "border": "#2e2e2e",
        "muted_fg": "#9f9fa9",
        "node": "#2f2f31",
    },
}

SVG_FONT = "'Google Sans Code', 'Adwaita Mono', 'DejaVu Sans Mono', monospace"

# Font files for the PNG renderer, in preference order. A single variable font
# covers both weights; otherwise give (regular, bold).
FONT_FILES = [
    ("GoogleSansCode[wght].ttf",),
    ("AdwaitaMono-Regular.ttf", "AdwaitaMono-Bold.ttf"),
    ("DejaVuSansMono.ttf", "DejaVuSansMono-Bold.ttf"),
]
FONT_DIRS = [
    Path("/usr/share/fonts"),
    Path("/usr/local/share/fonts"),
    Path.home() / ".local/share/fonts",
    Path.home() / ".fonts",
    Path("/Library/Fonts"),
    Path("/System/Library/Fonts"),
    Path.home() / "Library/Fonts",
]


# Shape helpers. Coordinates are drawing units, origin top-left, 520 wide.


def zone(x, y, w, h, label):
    """A muted container with its label in the top-left corner."""
    return {"kind": "zone", "x": x, "y": y, "w": w, "h": h, "label": label}


def bar(x, y, w, h, label):
    """A muted container with its label centred; a full-width strip."""
    return {"kind": "bar", "x": x, "y": y, "w": w, "h": h, "label": label}


def node(x, y, w, h, label):
    """A darker filled box with a thin outline and a centred label; ``\\n`` for lines."""
    return {"kind": "node", "x": x, "y": y, "w": w, "h": h, "label": label}


def solid(x, y, w, h, label):
    """A foreground-filled box with background-coloured text, for flow charts."""
    return {"kind": "solid", "x": x, "y": y, "w": w, "h": h, "label": label}


def dashed(x, y, w, h, label, centered=False):
    """A dashed outline for a component inside a zone; label top-left unless centred."""
    return {"kind": "dashed", "x": x, "y": y, "w": w, "h": h,
            "label": label, "centered": centered}


def dotted(x, y, w, h, label):
    """A dotted outline for a step on a path, such as a filter; label centred."""
    return {"kind": "dotted", "x": x, "y": y, "w": w, "h": h, "label": label}


def arrow(points, label="", at=None, anchor="middle"):
    """An orthogonal polyline ending in a filled arrowhead.

    ``points`` is a list of (x, y). The optional label is drawn with its
    baseline at ``at`` and its ``anchor`` ("start", "middle" or "end") there.
    """
    if label and at is None:
        raise ValueError(f"arrow label {label!r} needs an 'at' coordinate")
    return {"kind": "arrow", "points": points, "label": label, "at": at, "anchor": anchor}


def note(x, y, text, anchor="start"):
    """Free text with its baseline at (x, y)."""
    return {"kind": "note", "x": x, "y": y, "label": text, "anchor": anchor}


def dim(*shapes):
    """Draw the given shapes at 30% opacity, for an inactive part of the picture."""
    return {"kind": "group", "opacity": 0.3, "shapes": list(shapes)}


# A shared grid for a set of traffic diagrams: a top row of zones and a
# full-width bar beneath. Reuse the same numbers across related diagrams so
# they line up in the document.
TOP, TOP_H = 24, 182
BAR_Y, BAR_H = 264, 56
NODE_W, NODE_H = 140, 38

EXAMPLE = {
    "boundary": {
        "title": "requests cross the proxy",
        "height": 340,
        "shapes": [
            zone(18, TOP, 230, TOP_H, "client"),
            node(63, 128, NODE_W, NODE_H, "browser"),
            zone(272, TOP, 230, TOP_H, "server"),
            dashed(290, 76, 194, 112, "api worker"),
            node(317, 128, NODE_W, NODE_H, "handler"),
            arrow([(133, 166), (133, 218)]),
            dotted(83, 218, 100, 28, "proxy"),
            arrow([(133, 246), (133, 264)]),
            bar(18, BAR_Y, 484, BAR_H, "host"),
            arrow([(387, 264), (387, 166)]),
        ],
    },
    "replay": {
        "title": "replay with a cached response",
        "height": 316,
        "shapes": [
            dim(zone(18, TOP, 230, TOP_H, "client")),
            zone(272, TOP, 230, TOP_H, "server"),
            bar(18, 230, 484, BAR_H, "host"),
            arrow([(387, 230), (387, 166)]),
            node(317, 128, NODE_W, NODE_H, "cached response"),
        ],
    },
    "steps": {
        "title": "how a token is issued and retired",
        "height": 190,
        "shapes": [
            node(18, 24, 108, 64, "1\nclient asks\nfor a token"),
            arrow([(126, 56), (143, 56)]),
            node(143, 24, 108, 64, "2\nissuer mints\na short-lived\ntoken"),
            arrow([(251, 56), (268, 56)]),
            node(268, 24, 108, 64, "3\nproxy swaps\nit for the\nreal key"),
            arrow([(376, 56), (393, 56)]),
            node(393, 24, 108, 64, "4\ntoken\nexpires"),
            note(18, 130, "the real key never leaves the proxy."),
            note(18, 150, "what shows in logs is the short-lived token."),
        ],
    },
    "flow": {
        "title": "how a change gets merged",
        "height": 200,
        "shapes": [
            solid(18, 82, 90, 36, "draft"),
            arrow([(108, 100), (160, 100)]),
            solid(160, 82, 200, 36, "pull request"),
            solid(190, 18, 90, 36, "reviewer"),
            arrow([(230, 54), (230, 82)]),
            arrow([(240, 82), (240, 54)]),
            solid(185, 146, 70, 36, "lint"),
            arrow([(215, 146), (215, 118)]),
            arrow([(225, 118), (225, 146)]),
            solid(265, 146, 70, 36, "tests"),
            arrow([(295, 146), (295, 118)]),
            arrow([(305, 118), (305, 146)]),
            arrow([(360, 100), (412, 100)]),
            solid(412, 82, 90, 36, "merge"),
        ],
    },
}

# Your diagrams go here: slug -> {"title", "height", "shapes"}.
DIAGRAMS: dict[str, dict] = {}


def _lines(label):
    return label.split("\n")


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _frame(spec):
    """Return (width, height, drawing offset) of the framed figure."""
    caption = CAPTION_H if spec.get("title") else 0
    width = W + 2 * PAD_SIDE
    height = PAD_TOP + caption + spec["height"] + PAD_BOTTOM
    return width, height, (PAD_SIDE, PAD_TOP + caption)


def _walk(shapes, opacity=1.0):
    """Yield (shape, opacity) for every leaf shape, flattening groups."""
    for s in shapes:
        if s["kind"] == "group":
            yield from _walk(s["shapes"], opacity * s["opacity"])
        else:
            yield s, opacity


def _text_lines(y, label, size):
    """Baselines for a possibly multi-line label centred vertically on y."""
    lines = _lines(label)
    step = size * LINE_STEP
    top = y - step * (len(lines) - 1) / 2
    return [(line, top + i * step) for i, line in enumerate(lines)]


def _centre_baseline(s):
    return s["y"] + s["h"] / 2 + TEXT_SIZE / 3


def _css(t):
    """Style rules for one theme; the dark rules override inside a media query."""
    return "".join([
        f".frame{{fill:{t['background']};stroke:{t['border']};stroke-width:1}}",
        f".caption{{fill:{t['foreground']};font-size:{CAPTION_SIZE}px;font-weight:700;letter-spacing:.02em}}",
        f".zone{{fill:{t['muted']};stroke:{t['border']};stroke-width:1}}",
        f".node{{fill:{t['node']};stroke:{t['muted_fg']};stroke-width:1}}",
        f".solid{{fill:{t['foreground']};stroke:{t['foreground']};stroke-width:1}}",
        f".dashed{{fill:{t['background']};stroke:{t['muted_fg']};stroke-width:1;stroke-dasharray:4 3}}",
        f".dotted{{fill:{t['background']};stroke:{t['muted_fg']};stroke-width:1;stroke-dasharray:1 3;stroke-linecap:round}}",
        f".flow{{fill:none;stroke:{t['muted_fg']};stroke-width:1}}",
        f".head{{fill:{t['muted_fg']};stroke:none}}",
        f".label{{fill:{t['foreground']}}}",
        f".inverse{{fill:{t['background']}}}",
    ])


def svg(spec):
    """Return the SVG document for one diagram, with light and dark styles."""
    width, height, (ox, oy) = _frame(spec)
    light, dark = THEMES["light"], THEMES["dark"]

    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" font-family="{SVG_FONT}" font-size="{TEXT_SIZE}">',
        "<style>",
        _css(light),
        f"@media (prefers-color-scheme: dark){{{_css(dark)}}}",
        "</style>",
        '<defs><marker id="head" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" '
        'markerHeight="7" orient="auto-start-reverse"><path d="M1 1L7 4L1 7Z" class="head"/>'
        "</marker></defs>",
        f'<rect x="0.5" y="0.5" width="{width - 1}" height="{height - 1}" class="frame"/>',
    ]
    if spec.get("title"):
        out.append(
            f'<text x="{PAD_SIDE}" y="{PAD_TOP + CAPTION_SIZE - 2}" class="caption">'
            f'{_esc(spec["title"])}</text>'
        )
    out.append(f'<g transform="translate({ox} {oy})">')

    def text(x, y, label, anchor="start", cls="label"):
        for line, by in _text_lines(y, label, TEXT_SIZE):
            out.append(
                f'<text x="{x}" y="{by:g}" text-anchor="{anchor}" class="{cls}">{_esc(line)}</text>'
            )

    def rect(s, cls):
        out.append(
            f'<rect x="{s["x"]}" y="{s["y"]}" width="{s["w"]}" height="{s["h"]}" class="{cls}"/>'
        )

    current = 1.0
    for s, opacity in _walk(spec["shapes"]):
        if opacity != current:
            if current != 1.0:
                out.append("</g>")
            if opacity != 1.0:
                out.append(f'<g opacity="{opacity:g}">')
            current = opacity
        kind = s["kind"]
        if kind == "zone":
            rect(s, "zone")
            text(s["x"] + 16, s["y"] + 24, s["label"])
        elif kind == "bar":
            rect(s, "zone")
            if s["label"]:
                text(s["x"] + s["w"] / 2, _centre_baseline(s), s["label"], "middle")
        elif kind == "node":
            rect(s, "node")
            text(s["x"] + s["w"] / 2, _centre_baseline(s), s["label"], "middle")
        elif kind == "solid":
            rect(s, "solid")
            text(s["x"] + s["w"] / 2, _centre_baseline(s), s["label"], "middle", "inverse")
        elif kind == "dashed":
            rect(s, "dashed")
            if s["centered"]:
                text(s["x"] + s["w"] / 2, _centre_baseline(s), s["label"], "middle")
            else:
                text(s["x"] + 14, s["y"] + 24, s["label"])
        elif kind == "dotted":
            rect(s, "dotted")
            text(s["x"] + s["w"] / 2, _centre_baseline(s), s["label"], "middle")
        elif kind == "arrow":
            pts = " ".join(f"{x},{y}" for x, y in s["points"])
            out.append(f'<polyline points="{pts}" class="flow" marker-end="url(#head)"/>')
            if s["label"]:
                text(s["at"][0], s["at"][1], s["label"], s["anchor"])
        elif kind == "note":
            text(s["x"], s["y"], s["label"], s["anchor"])
        else:
            raise ValueError(f"unknown shape kind {kind!r}")
    if current != 1.0:
        out.append("</g>")
    out.append("</g></svg>")
    return "\n".join(out) + "\n"


def find_fonts():
    """Return (regular, bold) font paths, or exit with a message naming what is missing."""
    for files in FONT_FILES:
        found = {}
        for root in FONT_DIRS:
            if not root.is_dir():
                continue
            for name in files:
                if name not in found:
                    hit = next(root.rglob(name), None)
                    if hit:
                        found[name] = str(hit)
        if len(found) == len(files):
            paths = [found[name] for name in files]
            return paths[0], paths[-1]
    wanted = " or ".join(" + ".join(files) for files in FONT_FILES)
    searched = ", ".join(str(d) for d in FONT_DIRS)
    sys.exit(
        f"diagrams.py: no monospace font found for PNG rendering.\n"
        f"  wanted: {wanted}\n  searched: {searched}\n"
        "  install Google Sans Code (fonts.google.com), Adwaita Mono or DejaVu Sans Mono,\n"
        "  or add a font directory to FONT_DIRS."
    )


def png(spec, theme="light", scale=PNG_SCALE):
    """Return a Pillow image for one diagram in the given theme."""
    from PIL import Image, ImageDraw, ImageFont

    t = THEMES[theme]
    regular, bold = find_fonts()
    width, height, (ox, oy) = _frame(spec)
    img = Image.new("RGBA", (width * scale, height * scale), t["background"])
    fonts = {}

    def font(size, weight=400):
        key = (size, weight)
        if key not in fonts:
            f = ImageFont.truetype(bold if weight >= 700 else regular, round(size * scale))
            try:
                f.set_variation_by_axes([weight])
            except OSError:
                pass  # static font: the file already has the right weight
            fonts[key] = f
        return fonts[key]

    def p(v):
        return int(round(v * scale))

    def layer():
        """A transparent layer; shapes drawn on it are blended down at reduced opacity."""
        return Image.new("RGBA", img.size, (0, 0, 0, 0))

    def blend(layer_img, opacity):
        if opacity < 1.0:
            alpha = layer_img.getchannel("A").point(lambda a: int(a * opacity))
            layer_img.putalpha(alpha)
        img.alpha_composite(layer_img)

    def text(d, x, y, label, anchor="start", fill=None):
        code = {"start": "ls", "middle": "ms", "end": "rs"}[anchor]
        for line, by in _text_lines(y, label, TEXT_SIZE):
            d.text((p(ox + x), p(oy + by)), line, font=font(TEXT_SIZE),
                   fill=fill or t["foreground"], anchor=code)

    def box(s):
        return [p(ox + s["x"]), p(oy + s["y"]), p(ox + s["x"] + s["w"]), p(oy + s["y"] + s["h"])]

    def patterned_rect(d, s, dash, gap, round_caps=False):
        x, y, w, h = ox + s["x"], oy + s["y"], s["w"], s["h"]
        corners = [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)]
        for (x1, y1), (x2, y2) in zip(corners, corners[1:]):
            length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            ux, uy = (x2 - x1) / length, (y2 - y1) / length
            pos = 0.0
            while pos < length:
                end = min(pos + dash, length)
                a = (p(x1 + ux * pos), p(y1 + uy * pos))
                b = (p(x1 + ux * end), p(y1 + uy * end))
                if round_caps:
                    r = STROKE * scale / 2
                    d.ellipse([a[0] - r, a[1] - r, a[0] + r, a[1] + r], fill=t["muted_fg"])
                else:
                    d.line([a, b], fill=t["muted_fg"], width=STROKE * scale)
                pos += dash + gap

    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, img.width - 1, img.height - 1], outline=t["border"], width=STROKE * scale)
    if spec.get("title"):
        d.text((p(PAD_SIDE), p(PAD_TOP + CAPTION_SIZE - 2)), spec["title"],
               font=font(CAPTION_SIZE, 700), fill=t["foreground"], anchor="ls")

    current, cur_img = 1.0, None
    for s, opacity in _walk(spec["shapes"]):
        if opacity != current:
            if cur_img is not None:
                blend(cur_img, current)
            cur_img = layer() if opacity < 1.0 else None
            d = ImageDraw.Draw(cur_img if cur_img is not None else img)
            current = opacity
        kind = s["kind"]
        if kind in ("zone", "bar"):
            d.rectangle(box(s), fill=t["muted"], outline=t["border"], width=STROKE * scale)
            if kind == "zone":
                text(d, s["x"] + 16, s["y"] + 24, s["label"])
            elif s["label"]:
                text(d, s["x"] + s["w"] / 2, _centre_baseline(s), s["label"], "middle")
        elif kind == "node":
            d.rectangle(box(s), fill=t["node"], outline=t["muted_fg"], width=STROKE * scale)
            text(d, s["x"] + s["w"] / 2, _centre_baseline(s), s["label"], "middle")
        elif kind == "solid":
            d.rectangle(box(s), fill=t["foreground"])
            text(d, s["x"] + s["w"] / 2, _centre_baseline(s), s["label"], "middle", t["background"])
        elif kind == "dashed":
            d.rectangle(box(s), fill=t["background"])
            patterned_rect(d, s, 4, 3)
            if s["centered"]:
                text(d, s["x"] + s["w"] / 2, _centre_baseline(s), s["label"], "middle")
            else:
                text(d, s["x"] + 14, s["y"] + 24, s["label"])
        elif kind == "dotted":
            d.rectangle(box(s), fill=t["background"])
            patterned_rect(d, s, 1, 3, round_caps=True)
            text(d, s["x"] + s["w"] / 2, _centre_baseline(s), s["label"], "middle")
        elif kind == "arrow":
            pts = [(ox + x, oy + y) for x, y in s["points"]]
            d.line([(p(x), p(y)) for x, y in pts], fill=t["muted_fg"], width=STROKE * scale)
            (x1, y1), (x2, y2) = pts[-2], pts[-1]
            length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            ux, uy = (x2 - x1) / length, (y2 - y1) / length
            # Marker geometry: a 7-unit head whose tip sits on the line end.
            left = (x2 - ux * HEAD * 6 / 7 - uy * HEAD * 3 / 7, y2 - uy * HEAD * 6 / 7 + ux * HEAD * 3 / 7)
            right = (x2 - ux * HEAD * 6 / 7 + uy * HEAD * 3 / 7, y2 - uy * HEAD * 6 / 7 - ux * HEAD * 3 / 7)
            d.polygon([(p(x2), p(y2)), (p(left[0]), p(left[1])), (p(right[0]), p(right[1]))], fill=t["muted_fg"])
            if s["label"]:
                text(d, s["at"][0], s["at"][1], s["label"], s["anchor"])
        elif kind == "note":
            text(d, s["x"], s["y"], s["label"], s["anchor"])
        else:
            raise ValueError(f"unknown shape kind {kind!r}")
    if cur_img is not None:
        blend(cur_img, current)
    return img.convert("RGB")


def render(diagrams, out_dir, scale=PNG_SCALE):
    """Write <slug>.svg, <slug>.png and <slug>-dark.png for every diagram into out_dir."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for slug, spec in diagrams.items():
        (out_dir / f"{slug}.svg").write_text(svg(spec))
        png(spec, "light", scale).save(out_dir / f"{slug}.png")
        png(spec, "dark", scale).save(out_dir / f"{slug}-dark.png")
        print(f"{slug}.svg {slug}.png {slug}-dark.png")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--example", action="store_true", help="render the built-in example instead of DIAGRAMS")
    ap.add_argument("--out", default=Path(__file__).resolve().parent, help="output directory (default: next to this file)")
    ap.add_argument("--scale", type=int, default=PNG_SCALE, help=f"PNG pixels per drawing unit (default {PNG_SCALE})")
    args = ap.parse_args(argv)
    diagrams = EXAMPLE if args.example else DIAGRAMS
    if not diagrams:
        sys.exit("diagrams.py: DIAGRAMS is empty; add a diagram or run with --example")
    render(diagrams, args.out, args.scale)


if __name__ == "__main__":
    main()
