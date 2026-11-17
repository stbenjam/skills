---
name: braintrust
description: Convene a mini or mega panel of different models on a design, codebase or decision, and lead with the findings only one panelist raised. Use when the user asks for a braintrust, panel, council, mini-panel or mega-panel, or wants several independent opinions.
license: MIT
metadata:
  author: stbenjam
  version: "0.1.0"
argument-hint: "[mini|mega] [topic]"
---

Convene a panel of different models to review a design, codebase or
decision. Run each panelist in parallel as its own subagent or thread on its
model.

## Rosters

- **Mega-panel (7):** the latest Codex GPT model (like Astra), the latest
  Gemini model in Antigravity (like Hydrogen or Carbon), the latest Sol and
  Terra models, and the latest Claude Haiku, Sonnet and Fable.
- **Mini-panel (3):** one model from each provider.

If the user doesn't say which, run a mini-panel.

## Prompt rules

- Every panelist gets the same brief, word for word. Save it with the results
  so the panel can be rerun and compared like with like.
- Keep the brief neutral. Don't name the idea you're testing; if a panelist
  finds it unprompted, that's the signal.
- Panelists only read and report. No running code, no changes.

## Synthesis

1. Lead with the minority reports: points only one panelist raised, grouped
   by panelist and ordered by your own judgement of how valid they are.
2. Check every specific claim against the code before passing it on, and mark
   each one verified or unverified.
3. Then list the consensus briefly. Agreement mostly confirms trade-offs the
   user already knows.
4. Separately flag points that conflict with the user's past decisions.
