#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = ["pillow"]
# ///
"""Black-and-white box diagrams, laid out by hand, written as SVG and PNG.

Copy this file next to the document it illustrates, fill in ``DIAGRAMS`` and run
it. It writes ``<slug>.svg`` and ``<slug>.png`` beside itself for every entry:

    uv run diagrams.py            # render DIAGRAMS
    uv run diagrams.py --example  # render the built-in example instead
    uv run diagrams.py --out DIR  # write somewhere else

Plain ``python3`` works too when Pillow is installed. The PNG renderer needs a
real font file: Adwaita Mono or DejaVu Sans Mono.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Canvas and style. Everything below is fixed on purpose: the point of the
# style is that every diagram in a set looks the same.
W = 1600
MARGIN = 60
INK = "#1f1f1f"
LINE = "#70707a"
ZONE_FILL = "#f3f3f3"
ZONE_EDGE = "#e2e2e2"
NODE_FILL = "#d9d9d9"
WHITE = "#ffffff"
TITLE_SIZE = 34
LABEL_SIZE = 26
SMALL_SIZE = 21
STROKE = 2
HEAD = 14
SVG_FONT = "'Adwaita Mono', 'DejaVu Sans Mono', 'Courier New', monospace"

# Font files for the PNG renderer, in preference order: (regular, bold).
FONT_FILES = [
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


# Shape helpers. Coordinates are canvas pixels, origin top-left.


def zone(x, y, w, h, label):
    """A light container with its label in the top-left corner."""
    return {"kind": "zone", "x": x, "y": y, "w": w, "h": h, "label": label}


def bar(x, y, w, h, label):
    """A light container with its label centred; a full-width strip."""
    return {"kind": "bar", "x": x, "y": y, "w": w, "h": h, "label": label}


def node(x, y, w, h, label):
    """A solid grey box with a centred label; use ``\\n`` for more lines."""
    return {"kind": "node", "x": x, "y": y, "w": w, "h": h, "label": label}


def dashed(x, y, w, h, label, centered=False):
    """A dashed outline for a component inside a zone; label top-left unless centred."""
    return {"kind": "dashed", "x": x, "y": y, "w": w, "h": h,
            "label": label, "centered": centered}


def arrow(points, label="", at=None, anchor="middle"):
    """An orthogonal polyline ending in a filled arrowhead.

    ``points`` is a list of (x, y). The optional label is drawn at ``at`` with
    its ``anchor`` ("start", "middle" or "end") on that point.
    """
    if label and at is None:
        raise ValueError(f"arrow label {label!r} needs an 'at' coordinate")
    return {"kind": "arrow", "points": points, "label": label, "at": at, "anchor": anchor}


def note(x, y, text, anchor="start", size=SMALL_SIZE):
    """Free text, small by default; pass ``size=LABEL_SIZE`` for a heading."""
    return {"kind": "note", "x": x, "y": y, "label": text, "anchor": anchor, "size": size}


# A shared grid for a set of traffic diagrams: a top row of zones and a
# full-width bar beneath. Reuse the same numbers across related diagrams so
# they line up in the document.
TOP, TOP_H = 130, 400
BAR_Y, BAR_H = 640, 200
NODE_W, NODE_H = 240, 80

EXAMPLE = {
    "example-proxy": {
        "title": "requests through a proxy",
        "height": 900,
        "shapes": [
            zone(MARGIN, TOP, 640, TOP_H, "client"),
            zone(900, TOP, 640, TOP_H, "server"),
            bar(MARGIN, BAR_Y, 1480, BAR_H, ""),
            note(100, BAR_Y + 50, "host", size=LABEL_SIZE),
            node(120, 260, NODE_W, NODE_H, "browser"),
            node(120, 400, NODE_W, NODE_H, "session\ncookie"),
            node(1100, 260, NODE_W, NODE_H, "api"),
            dashed(480, 670, 640, 140, "proxy"),
            node(820, 700, NODE_W, NODE_H, "cache"),
            arrow([(360, 300), (560, 300), (560, 670)],
                  "request", at=(540, 585), anchor="end"),
            arrow([(1020, 670), (1020, 300), (1100, 300)],
                  "forwarded request", at=(1040, 585), anchor="start"),
        ],
    },
}

# Your diagrams go here: slug -> {"title", "height", "shapes"}.
DIAGRAMS: dict[str, dict] = {}


def _lines(label):
    return label.split("\n")


def _esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(spec):
    """Return the SVG document for one diagram as a string."""
    h = spec["height"]
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" '
        f'width="{W}" height="{h}" font-family="{SVG_FONT}">',
        '<defs><marker id="head" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" '
        f'markerHeight="9" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{LINE}"/>'
        "</marker></defs>",
        f'<rect width="{W}" height="{h}" fill="{WHITE}"/>',
        f'<text x="40" y="62" font-size="{TITLE_SIZE}" font-weight="700" fill="{INK}">'
        f'{_esc(spec["title"])}</text>',
    ]

    def text(x, y, label, size, anchor="middle"):
        lines = _lines(label)
        step = size * 1.3
        top = y - step * (len(lines) - 1) / 2
        for i, line in enumerate(lines):
            out.append(
                f'<text x="{x}" y="{top + i * step}" font-size="{size}" fill="{INK}" '
                f'text-anchor="{anchor}" dominant-baseline="middle">{_esc(line)}</text>'
            )

    def rect(s, **attrs):
        extra = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
        out.append(f'<rect x="{s["x"]}" y="{s["y"]}" width="{s["w"]}" height="{s["h"]}" {extra}/>')

    for s in spec["shapes"]:
        kind = s["kind"]
        if kind == "zone":
            rect(s, fill=ZONE_FILL, stroke=ZONE_EDGE, stroke_width=STROKE)
            text(s["x"] + 40, s["y"] + 50, s["label"], LABEL_SIZE, "start")
        elif kind == "bar":
            rect(s, fill=ZONE_FILL, stroke=ZONE_EDGE, stroke_width=STROKE)
            if s["label"]:
                text(s["x"] + s["w"] / 2, s["y"] + s["h"] / 2, s["label"], LABEL_SIZE)
        elif kind == "node":
            rect(s, fill=NODE_FILL)
            text(s["x"] + s["w"] / 2, s["y"] + s["h"] / 2, s["label"], LABEL_SIZE)
        elif kind == "dashed":
            rect(s, fill=WHITE, stroke=LINE, stroke_width=STROKE, stroke_dasharray="8 6")
            if s["centered"]:
                text(s["x"] + s["w"] / 2, s["y"] + s["h"] / 2, s["label"], LABEL_SIZE)
            else:
                text(s["x"] + 24, s["y"] + 34, s["label"], LABEL_SIZE, "start")
        elif kind == "arrow":
            pts = " ".join(f"{x},{y}" for x, y in s["points"])
            out.append(
                f'<polyline points="{pts}" fill="none" stroke="{LINE}" '
                f'stroke-width="{STROKE}" marker-end="url(#head)"/>'
            )
            if s["label"]:
                text(s["at"][0], s["at"][1], s["label"], SMALL_SIZE, s["anchor"])
        elif kind == "note":
            text(s["x"], s["y"], s["label"], s["size"], s["anchor"])
        else:
            raise ValueError(f"unknown shape kind {kind!r}")
    out.append("</svg>")
    return "\n".join(out) + "\n"


def find_fonts():
    """Return (regular, bold) font paths, or exit with a message naming what is missing."""
    for regular, bold in FONT_FILES:
        found = {}
        for root in FONT_DIRS:
            if not root.is_dir():
                continue
            for name in (regular, bold):
                if name not in found:
                    hit = next(root.rglob(name), None)
                    if hit:
                        found[name] = str(hit)
        if len(found) == 2:
            return found[regular], found[bold]
    wanted = " or ".join(f"{r} + {b}" for r, b in FONT_FILES)
    searched = ", ".join(str(d) for d in FONT_DIRS)
    sys.exit(
        f"diagrams.py: no monospace font found for PNG rendering.\n"
        f"  wanted: {wanted}\n  searched: {searched}\n"
        "  install Adwaita Mono or DejaVu Sans Mono, or add a font directory to FONT_DIRS."
    )


def png(spec, scale=1):
    """Return a Pillow image for one diagram."""
    from PIL import Image, ImageDraw, ImageFont

    regular, bold = find_fonts()
    h = spec["height"]
    img = Image.new("RGB", (W * scale, h * scale), WHITE)
    d = ImageDraw.Draw(img)
    fonts = {}

    def font(size, is_bold=False):
        key = (size, is_bold)
        if key not in fonts:
            fonts[key] = ImageFont.truetype(bold if is_bold else regular, size * scale)
        return fonts[key]

    def p(v):
        return int(round(v * scale))

    def text(x, y, label, size, anchor="middle", is_bold=False):
        lines = _lines(label)
        step = size * 1.3
        top = y - step * (len(lines) - 1) / 2
        code = {"start": "lm", "middle": "mm", "end": "rm"}[anchor]
        for i, line in enumerate(lines):
            d.text((p(x), p(top + i * step)), line, font=font(size, is_bold), fill=INK, anchor=code)

    def box(s):
        return [p(s["x"]), p(s["y"]), p(s["x"] + s["w"]), p(s["y"] + s["h"])]

    def dashed_line(a, b, dash=8, gap=6):
        (x1, y1), (x2, y2) = a, b
        length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
        pos = 0.0
        while pos < length:
            end = min(pos + dash, length)
            d.line(
                [(p(x1 + (x2 - x1) * pos / length), p(y1 + (y2 - y1) * pos / length)),
                 (p(x1 + (x2 - x1) * end / length), p(y1 + (y2 - y1) * end / length))],
                fill=LINE, width=STROKE * scale,
            )
            pos += dash + gap

    text(40, 50, spec["title"], TITLE_SIZE, "start", is_bold=True)
    for s in spec["shapes"]:
        kind = s["kind"]
        if kind == "zone":
            d.rectangle(box(s), fill=ZONE_FILL, outline=ZONE_EDGE, width=STROKE * scale)
            text(s["x"] + 40, s["y"] + 50, s["label"], LABEL_SIZE, "start")
        elif kind == "bar":
            d.rectangle(box(s), fill=ZONE_FILL, outline=ZONE_EDGE, width=STROKE * scale)
            if s["label"]:
                text(s["x"] + s["w"] / 2, s["y"] + s["h"] / 2, s["label"], LABEL_SIZE)
        elif kind == "node":
            d.rectangle(box(s), fill=NODE_FILL)
            text(s["x"] + s["w"] / 2, s["y"] + s["h"] / 2, s["label"], LABEL_SIZE)
        elif kind == "dashed":
            d.rectangle(box(s), fill=WHITE)
            x, y, w, hh = s["x"], s["y"], s["w"], s["h"]
            corners = [(x, y), (x + w, y), (x + w, y + hh), (x, y + hh), (x, y)]
            for a, b in zip(corners, corners[1:]):
                dashed_line(a, b)
            if s["centered"]:
                text(x + w / 2, y + hh / 2, s["label"], LABEL_SIZE)
            else:
                text(x + 24, y + 34, s["label"], LABEL_SIZE, "start")
        elif kind == "arrow":
            pts = s["points"]
            d.line([(p(x), p(y)) for x, y in pts], fill=LINE, width=STROKE * scale)
            (x1, y1), (x2, y2) = pts[-2], pts[-1]
            length = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
            ux, uy = (x2 - x1) / length, (y2 - y1) / length
            left = (x2 - ux * HEAD - uy * HEAD / 2, y2 - uy * HEAD + ux * HEAD / 2)
            right = (x2 - ux * HEAD + uy * HEAD / 2, y2 - uy * HEAD - ux * HEAD / 2)
            d.polygon([(p(x2), p(y2)), (p(left[0]), p(left[1])), (p(right[0]), p(right[1]))], fill=LINE)
            if s["label"]:
                text(s["at"][0], s["at"][1], s["label"], SMALL_SIZE, s["anchor"])
        elif kind == "note":
            text(s["x"], s["y"], s["label"], s["size"], s["anchor"])
        else:
            raise ValueError(f"unknown shape kind {kind!r}")
    return img


def render(diagrams, out_dir, scale=1):
    """Write <slug>.svg and <slug>.png for every diagram into out_dir."""
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for slug, spec in diagrams.items():
        (out_dir / f"{slug}.svg").write_text(svg(spec))
        png(spec, scale).save(out_dir / f"{slug}.png")
        print(f"{slug}.svg {slug}.png")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--example", action="store_true", help="render the built-in example instead of DIAGRAMS")
    ap.add_argument("--out", default=Path(__file__).resolve().parent, help="output directory (default: next to this file)")
    ap.add_argument("--scale", type=int, default=1, help="PNG scale factor, e.g. 2 for a sharper image")
    args = ap.parse_args(argv)
    diagrams = EXAMPLE if args.example else DIAGRAMS
    if not diagrams:
        sys.exit("diagrams.py: DIAGRAMS is empty; add a diagram or run with --example")
    render(diagrams, args.out, args.scale)


if __name__ == "__main__":
    main()
