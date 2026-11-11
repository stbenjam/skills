---
name: diagrams
description: Draw black-and-white box diagrams (architecture, data flow, sequence of steps) for a design doc, RFC, README or slide, rendered to SVG and PNG from hand-placed coordinates with the bundled Python script. Use when a document needs a diagram that should look plain, consistent and monospace rather than auto-laid-out.
license: MIT
metadata:
  author: stbenjam
  version: "0.1.0"
---

# Diagrams

Box diagrams for documents, in one fixed style, generated from a Python file
that stays next to the document as the editable source. Use this when a design
doc, RFC, README or slide needs an architecture, data-flow or
sequence-of-steps picture. Do not use it for charts of data.

## The style

The script enforces most of this; the rest is on you.

- Black and white with two greys. Ink `#1f1f1f` for text, line grey `#70707a`
  for arrows and arrowheads, zone fill `#f3f3f3` with edge `#e2e2e2`, node
  fill `#d9d9d9` with no visible border. White background. No colour.
- Monospace everywhere: Adwaita Mono, then DejaVu Sans Mono, then Courier New.
  Title 34px bold at the top-left, labels 26px, small notes 21px.
- All labels lowercase except proper nouns.
- Five primitives plus free text:
  - `zone(x, y, w, h, label)`: light container, label in the top-left corner.
  - `bar(x, y, w, h, label)`: light container, label centred. Used as a
    full-width strip such as "host" beneath the top row. Pass `""` and add a
    `note` at label size when something sits in the middle of the bar.
  - `node(x, y, w, h, label)`: solid grey box, centred label, `\n` for lines.
  - `dashed(x, y, w, h, label, centered=False)`: dashed outline for a
    component that lives inside a zone.
  - `arrow(points, label, at, anchor)`: orthogonal polyline with a filled
    arrowhead. The label goes at explicit coordinates with a `start`,
    `middle` or `end` anchor.
  - `note(x, y, text, anchor, size)`: free text, small by default.
- Canvas 1600px wide. Height per diagram: 900 for a traffic diagram, shorter
  for a flow. 60px margins, zones about 400px tall, nodes 240x80.
- Coordinates are laid out by hand. No auto-layout.

## Workflow

1. Sketch the diagram in text first: what the zones are, what sits in each,
   which arrows matter. Fewer boxes is better. One idea per diagram.
2. Pick a grid shared by every diagram in the set, so they line up across the
   document: same top row, same bottom bar, same node sizes. Put those numbers
   in constants (`TOP`, `BAR_Y`, `NODE_W`) and reuse them.
3. Copy [scripts/diagrams.py](scripts/diagrams.py) from this skill into the document's directory
   (for example `docs/<topic>/diagrams/diagrams.py`) and fill in `DIAGRAMS`:
   a slug mapped to `{"title", "height", "shapes"}`. Leave `EXAMPLE` or delete
   it. The copied file is the record of the diagrams; edit and regenerate it
   rather than touching the outputs.
4. Run it. It writes `<slug>.svg` and `<slug>.png` next to the file:

   ```bash
   uv run diagrams.py              # or: python3 diagrams.py, with Pillow installed
   uv run diagrams.py --example    # the built-in client / proxy / server example
   uv run diagrams.py --scale 2    # sharper PNG for slides or Google Docs
   ```

   It needs Python 3.12+ and Pillow, nothing else. The PNG renderer requires a
   real Adwaita Mono or DejaVu Sans Mono font file and stops with a message
   naming the missing font rather than falling back to a bitmap font.
5. Look at every PNG. Check that labels do not overlap boxes or arrows, that
   arrows start and end on box edges, and that related diagrams line up.
   Adjust coordinates and rerun until it is right.

## Getting the images into the destination

- Repository docs and READMEs: commit the `diagrams.py`, the SVGs and the PNGs.
  Reference the SVG from Markdown; keep the PNG for places that cannot render
  SVG.
- Google Docs: the Docs API cannot embed local files. Publish the PNGs
  somewhere fetchable by URL, such as a secret gist, then insert each image by
  URL. Rerunning the script and re-uploading replaces the image.
- Slides: use the PNG, rendered at `--scale 2`.
