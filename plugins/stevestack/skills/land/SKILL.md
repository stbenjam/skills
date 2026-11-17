---
name: land
description: Authorize merging the current PR yourself once it meets the bar.
license: MIT
metadata:
  author: stbenjam
  version: "0.1.0"
user-invocable: true
disable-model-invocation: true
argument-hint: "[pr-url]"
---

You are authorized to merge this PR yourself, without waiting for me, once
all of these hold:

- The latest `deep-review` round approved it, or you rejected every remaining
  finding as a nit and said why.
- No human has requested changes or left a comment you haven't addressed,
  and no question to me is pending.
- CI passes, the branch is mergeable, and no maintainer has taken it over.

Keep shepherding with `pr-loop` until then. Merge with the repository's
usual merge method, then clean up as `pr-loop` does when a PR merges. If a
condition can't be met, stop and tell me why instead of merging.
