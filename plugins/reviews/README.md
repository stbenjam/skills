# reviews

Code review with specialist reviewers and runtime reproducers, plus guided eval
and benchmark task walkthroughs.

See the [main installation guide](../../README.md#installation) for Claude
Code, Codex, and standalone Agent Skills setup.

## Skills

<!-- BEGIN GENERATED SKILLS -->
- [`deep-review`](skills/deep-review/SKILL.md) — Use when a deeper level of code review is requested. Multi-agent panel code review with specialist reviewers and forced runtime reproducers for all BLOCKING bug findings. Optionally posts to GitHub/GitLab as a PENDING review.
- [`task-walkthrough`](skills/task-walkthrough/SKILL.md) — Walk through a Terminal-Bench task, internal eval, or benchmark task PR for a competent CS engineer, explain its verifier and review rubric, then check understanding with one applied question at a time. Use when the user wants to understand or present a task before reviewing it.
<!-- END GENERATED SKILLS -->

## Task walkthroughs

Use `task-walkthrough` with a task directory or task PR. It explains the domain,
model difficulty, realism, task flow, verifier and isolation, and rubric
compliance, then points to the key code sections. After the summary, it asks
3–5 applied questions one at a time to check your understanding.

```text
Use $task-walkthrough to walk me through this eval task PR.
```
