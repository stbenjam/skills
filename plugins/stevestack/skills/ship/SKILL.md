---
name: ship
description: Take work from any stage to an open, deep-reviewed PR.
license: MIT
metadata:
  author: stbenjam
  version: "0.1.0"
user-invocable: true
disable-model-invocation: true
argument-hint: "[instructions]"
---

Take the work from wherever it stands to an open PR, then see it through
review:

1. **Pick up.** Work out where things stand from the user's instructions, the
   conversation and the repo: is there a branch, uncommitted work, or an
   existing PR? Continue from there and skip steps that are already done. If
   there is no branch yet, create one.
2. **Finish the change.** Follow the `principles` skill: make the smallest
   change that meets the goal, using good abstractions, and don't balloon it.
   Check any assumption the change depends on before relying on it. Show the
   change works, then commit it using Conventional Commits.
3. **Review.** Spawn a new thread or a dedicated subagent on the latest Codex
   GPT Astra model to run `deep-review` on the branch. Use your best
   judgement on the findings: this is your codebase, and you are its owner
   and long-term maintainer. Accept the findings that make the change better
   and reject nits and unrealistic edge cases. Commit the fixes, then review
   again, passing the reviewer the round number, the previous verdict and
   what you fixed. Stop after three rounds or once a round finds nothing
   blocking.
4. **Open the PR.** Unless the maintainer asks otherwise, shape the branch
   into a logical series of commits: squash a small change into one commit,
   and split a large change only where it has independent parts, to help
   review or stacking. Push and open the PR, or update the existing one. Keep
   the description brief: what changed and why, the evidence that it works,
   and anything you chose to leave out. Where a complex workflow needs
   explaining, use the `diagrams` skill, upload the images it makes to a
   gist, and embed them in the description by their gist URLs.
5. **Shepherd.** Hand the PR to `pr-loop`. Watch for feedback from trusted
   maintainers and review bots, and judge it the way you judged the
   `deep-review` findings in step 3, keeping `pr-loop`'s check-in before
   declining human feedback. Keep the commit series logical by folding fixes
   into the commits they belong to; this overrides `pr-loop`'s no-rebase
   rule, so push with `--force-with-lease`.
