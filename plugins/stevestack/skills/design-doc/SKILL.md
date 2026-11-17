---
name: design-doc
description: Write a short, accurate design doc in Google Docs with diagrams. Use when asked to write or update a design doc.
license: MIT
metadata:
  author: stbenjam
  version: "0.1.0"
argument-hint: "[topic]"
---

A design doc is a short, accurate description of the design as it stands
now.

## Style

- It fits in about six pages, roughly 3,000 words. Anything more moves to an
  appendix or a separate tab.
- It describes only the current design: no history of earlier versions, no
  compatibility with things that never shipped, and no results from
  particular runs, which go stale.
- The prose is plain and impersonal. It doesn't use "we" or "I", em dashes,
  or "this, not that" contrasts.
- Concrete examples carry the explanation, and diagrams from the `diagrams`
  skill show the architecture and the shape of a change.

## Steps

1. Write the doc in this style.
2. Draw its diagrams with the `diagrams` skill.
3. Send the text to the latest Gemini Flash model in Antigravity and ask it
   to make the text warm, readable and free of AI slopisms.
4. Read what comes back for correctness. Fix anything wrong, but keep its
   style choices.
5. Create the doc in Google Docs and insert the diagrams as the `diagrams`
   skill describes.

## Edits

Once written, the doc is kept correct rather than rewritten. Edits fix what's
wrong and leave the author's prose and examples alone.
