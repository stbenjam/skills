# Phase 2 — Specialist dispatch details

**Sub-agents and serial reviewers MUST NOT modify any files, and
MUST NOT run remote-write git commands** (`git push`, force-push
variants, push to protected branches, or pushes to any remote).
They are read-only reviewers.

## Findings JSON schema

Append this schema to each specialist prompt:

```json
[
  {
    "file": "src/example.py",
    "line": 42,
    "severity": "BLOCKING",
    "title": "Short title",
    "body": "Description of the issue",
    "suggestion": "Recommended action or null",
    "reproducer_needed": true
  }
]
```

**Severity values**: `BLOCKING` | `SUGGESTION` | `NOTE`

If no issues found, return an empty array and state what was checked.

Specialist severity rules describe the round 1 baseline. On later rounds, the
[iterative review policy](iterative-reviews.md) takes precedence for every new
BLOCKING classification; unresolved carried blockers retain their severity.

## Prompt path resolution

Resolve specialist prompts from the skill directory (repository
root relative):
`plugins/stevestack/skills/deep-review/references/specialists/{specialist}.md`.
Prefer that absolute-from-repository-root path over a bare
`references/specialists/...` path — agents may not share the
skill's working directory.

## Parallel mode

Launch **all enabled specialist sub-agents in a single message** so
they run concurrently, using the Agent tool with
`run_in_background: true`.

Each sub-agent gets:
- The prompt: "You are a {specialist}. Read
  `plugins/stevestack/skills/deep-review/references/specialists/{specialist}.md`
  for your review instructions."
- The merge base ref
- The PR number or branch name being reviewed
- Any prior review findings (if detected in Step 1.4)
- The current review round and threshold multiplier from the
  [iterative review policy](iterative-reviews.md), including which prior
  blockers carry forward and that the multiplier applies only to new BLOCKING
  findings
- The findings JSON schema above

Sub-agents have full read access to the locally checked-out
repository. They explore the repository on their own — read files, grep,
run git commands, etc. Apply the read-only contract at the top of
this file.

Use `subagent_type: "general-purpose"`. Do NOT set the `model`
parameter, except for the security specialist (see
[Security specialist model](#security-specialist-model)).

## Security specialist model

Before dispatch, check whether either of these models is available
to launch a sub-agent on, in this order of preference:

1. `gpt-daybreak-blue` (Daybreak)
2. `claude-mythos-5-1` (Mythos)

Check the host's live model catalog rather than a native tool's
fixed model list. For example, in T3 Code call
`orchestrator_capabilities` and launch through `delegate_task` with
the matching provider and model, even for a cross-provider model.

- **Daybreak or Mythos available**: run the security specialist
  on that model. Tell it the model it is running on and that it
  may build and run exploit reproducers for its findings (under
  the same `/tmp`-only, non-destructive rules as
  [reproducer-prompt.md](reproducer-prompt.md)). Launch any Phase 4
  reproducer for a security finding on the same model.
- **Neither available**: run the security specialist on the same
  model as the other specialists. Tell it it is on the default
  model and must not create or run reproducers. It sets
  `reproducer_needed: false` on every finding, and Phase 4 skips
  reproducers for security findings.

State the selected security model in the verdict's Stats section.
In serial mode, still dispatch the security specialist as a
sub-agent when Daybreak or Mythos is available; otherwise review
it inline like the other specialists.

## Serial mode (`--serial`)

Run all enabled specialists **inline in the main agent**, one after
another. Do **not** launch sub-agents for specialist dispatch.
(Phase 4 reproducer sub-agents are still launched even in serial
mode — the no-sub-agent constraint applies only to specialists.)

Then for each specialist in roster order, state the specialist name
as a heading, read
`plugins/stevestack/skills/deep-review/references/specialists/{specialist}.md`
for review instructions, review through that lens, and produce
findings in the same JSON format. Context from earlier specialists'
file reads and findings carries over automatically.

Before the first specialist, read the
[iterative review policy](iterative-reviews.md) and apply the current round's
threshold consistently to every specialist's severity classification.

**Do NOT modify any files, and do NOT push to any remote.** Serial
mode is read-only, same as parallel.

## External reviewers

If external reviewers were requested, launch them in parallel with
(or before, in serial mode) the specialist dispatch.

**CodeRabbit** (`--coderabbit`):
```bash
timeout 300 coderabbit review --agent --base "$MERGE_BASE" 2>&1
```

**Codex** (`--codex`):
```bash
timeout 300 codex review 2>&1
```

External reviewer output is captured as-is and included in the
arbiter's synthesis input as a peer specialist. If a command fails
(non-zero exit, tool not found, timeout), record the error and
continue — never block the panel on an external tool failure.
