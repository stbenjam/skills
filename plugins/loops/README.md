# loops

Autonomous loops that shepherd work to completion.

See the [main installation guide](../../README.md#installation) for Claude
Code, Codex, and standalone Agent Skills setup.

## Skills

<!-- BEGIN GENERATED SKILLS -->
- [`pr-loop`](skills/pr-loop/SKILL.md) — Shepherd a PR: merge base branch, fix CI, address review comments, resolve threads, and monitor until merged. Use when asked to drive a pull request through to merge.
<!-- END GENERATED SKILLS -->

## Usage

Invoke the `pr-loop` skill with a full GitHub pull request URL, or ask it to
detect the open pull request for the current branch. It prefers native T3
scheduled tasks via MCP and falls back to native `Cron*` tools only when T3
scheduling tools are absent. The skill manages a dynamic schedule with
exponential backoff and an 8-hour watcher, then removes both when the PR is
merged or the one-week limit is reached.
