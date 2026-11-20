---
name: unslop-prose
description: Spawn a T3 thread on Gemini 4 Neon to review and polish all prose added on this branch for clarity, warmth, and readability. Use when asked to polish, humanize, or improve writing on a branch before shipping.
license: MIT
metadata:
  author: stbenjam
  version: "0.1.0"
argument-hint: "[base-ref]"
---

# Unslop Prose

Strong coding models write stiff prose; Gemini writes with clarity and
warmth. Spawn a T3 thread on **Gemini 4 Neon** in the current checkout to
review and polish all prose added on this branch, layering a single commit
on top.

## Steps

1. **Locate Gemini 4 Neon.** Check `orchestrator_capabilities` and pick
   `gemini-4-neon` through Antigravity first, or another available harness
   that exposes it. If unavailable, report that and stop rather than
   substituting another model.
2. **Spawn the thread in this checkout.** Check `t3_worktree_status` and
   pass the matching `workspaceStrategy` (`existing_worktree` with
   `worktreePath`, or `root`) to `t3_thread_launch` so Gemini works on the
   current branch directly.
3. **Give it the brief.** Pass the branch name and merge base (defaulting
   to the default branch unless the user passed a base ref) and ask Gemini
   to:
   - Diff the current branch against the merge base and review all added or
     modified prose (docs, code comments, docstrings, user-facing copy).
   - Adjust the prose in place for clarity, warmth, and readability,
     cutting AI slopisms and diff narration while preserving every technical
     fact, link, identifier, and code behavior.
   - Leave untouched prose and code logic alone, and layer a single commit
     on top of the branch.
4. **Verify.** Wait with `t3_thread_wait`, read the reply with
   `t3_thread_read`, and check the new commit for factual or code
   regressions while keeping Gemini's voice choices. Share the spawned
   thread's verbatim `link`.
