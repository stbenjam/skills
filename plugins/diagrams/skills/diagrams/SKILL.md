---
name: diagrams
description: Draw minimal monospace box diagrams (architecture, trust boundaries, data flow, sequence of steps) for a design doc, RFC, README or slide, rendered to a light-and-dark SVG plus PNGs from hand-placed coordinates with the bundled Python script. Use whenever a document needs a diagram and the ask is for a clean, high-level picture rather than an auto-laid-out graph.
license: MIT
metadata:
  author: stbenjam
  version: "0.2.0"
---

# Diagrams

Small, quiet box diagrams in the style of the Terminal Bench blog figures:
monospace type, black and grey only, a handful of boxes, thin arrows, and
nothing decorative. Each diagram is a Python dict of hand-placed shapes that
the script renders to one SVG (which follows the viewer's light or dark mode)
and a light and a dark PNG. The Python file stays next to the document as the
editable source.

Use this when a design doc, RFC, README or slide needs an architecture,
boundary, data-flow or sequence-of-steps picture. Do not use it for charts of
data.

## Look at the samples first

Before drawing anything, view these. They are the style; match them.

- [boundary](assets/examples/boundary.png) ([svg](assets/examples/boundary.svg)):
  the primary style. Two muted environments on a top row, a full-width host
  strip beneath, a dashed box for a component inside an environment, a dotted
  box for a step on the path, and three unlabeled arrows.
- [replay](assets/examples/replay.png) ([svg](assets/examples/replay.svg)):
  the same grid with the inactive environment dimmed to 30%. Reuse one grid
  across a set so the reader's eye does not have to re-learn the layout.
- [steps](assets/examples/steps.png) ([svg](assets/examples/steps.svg)): a
  sequence as a row of numbered nodes with one or two lines of plain notes
  beneath. Shorter canvas, same type and strokes.
- [flow](assets/examples/flow.png) ([svg](assets/examples/flow.svg)): the
  secondary style for a process. Solid boxes with inverted text, paired
  one-way arrows for back-and-forth, no containers.

Their source is `EXAMPLE` in the script. The dark renders are
[boundary-dark](assets/examples/boundary-dark.png),
[replay-dark](assets/examples/replay-dark.png),
[steps-dark](assets/examples/steps-dark.png) and
[flow-dark](assets/examples/flow-dark.png).

## What makes the style

- Say one thing per diagram. If it needs a legend, it is two diagrams.
- Eight boxes or fewer. Label with nouns, one or two words, lowercase except
  proper nouns. Prefer the general name ("host", "worker") to the product name.
- Arrows show direction and rarely carry labels. If the reader cannot tell
  what flows without a label, rename the boxes.
- Containment carries meaning: a `zone` is a trust or process boundary, a
  `dashed` box is a component inside it, a `dotted` box is a filter or step a
  thing passes through, a `node` is data or a thing at rest, a `bar` is the
  shared substrate underneath.
- Emphasis is by omission: dim what is inactive instead of highlighting what
  is active. No colour, no icons, no shadows, no rounded corners.
- The drawing is 520 units wide; the script scales it. Boxes are about 140x38,
  environments about 230x182, strokes 1 unit, text 12 units. Leave room: the
  samples are roughly half empty.

## Primitives

All coordinates are drawing units with the origin at the top-left. Multi-line
labels use `\n`.

- `zone(x, y, w, h, label)`: muted container, label top-left.
- `bar(x, y, w, h, label)`: muted container, label centred; the host strip.
- `node(x, y, w, h, label)`: slightly darker filled box with a thin outline.
- `solid(x, y, w, h, label)`: foreground-filled box with inverted text.
- `dashed(x, y, w, h, label, centered=False)`: dashed outline.
- `dotted(x, y, w, h, label)`: dotted outline, label centred.
- `arrow(points, label="", at=None, anchor="middle")`: orthogonal polyline
  with a filled head; `points` is a list of `(x, y)`.
- `note(x, y, text, anchor="start")`: free text with its baseline at `(x, y)`.
- `dim(*shapes)`: draw the given shapes at 30% opacity.

## Workflow

1. Sketch in text: the boundaries, what sits in each, which two or three
   arrows matter. Cut until it fits the rules above.
2. Pick a grid shared by every diagram in the set: same top row, same bottom
   bar, same box sizes. Keep the numbers in constants (`TOP`, `BAR_Y`,
   `NODE_W`) and reuse them.
3. Copy [scripts/diagrams.py](scripts/diagrams.py) into the document's
   directory (for example `docs/<topic>/diagrams/diagrams.py`) and fill in
   `DIAGRAMS`: a slug mapped to `{"title", "height", "shapes"}`. Delete
   `EXAMPLE` or leave it; it is only rendered with `--example`.
4. Run it. It writes `<slug>.svg`, `<slug>.png` and `<slug>-dark.png` next to
   the file:

   ```bash
   uv run diagrams.py              # or: python3 diagrams.py, with Pillow installed
   uv run diagrams.py --example    # the four samples
   uv run diagrams.py --scale 4    # larger PNGs
   ```

   It needs Python 3.12+ and Pillow, nothing else. The PNG renderer requires a
   real font file: Google Sans Code (the blog's face, free from Google Fonts),
   or Adwaita Mono or DejaVu Sans Mono. It stops with a message naming the
   missing font rather than falling back to a bitmap font.
5. View every PNG, light and dark. Check that labels clear the box edges,
   arrows start and end on edges, and related diagrams line up. Adjust the
   coordinates and rerun until it is right.

## Getting the images into the destination

- Repository docs and READMEs: commit `diagrams.py`, the SVGs and the PNGs.
  Reference the SVG from Markdown; it switches with the reader's colour
  scheme on GitHub and in browsers. Keep the PNGs for viewers that cannot
  render SVG.
- Google Docs: the Docs API cannot embed local files. Publish the light PNGs
  somewhere fetchable by URL, such as a secret gist, then insert each image by
  URL. Rerunning the script and re-uploading replaces the image.
- Slides: use the PNG that matches the slide background.
