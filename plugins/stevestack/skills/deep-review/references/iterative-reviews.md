# Iterative review convergence

Read this reference when an earlier deep-review verdict exists for the same
PR/MR or the user identifies the current review as a later round. It governs
severity classification and final disposition in both parallel and serial
modes.

## Determine the round and multiplier

Round 1 uses the ordinary baseline for a blocking finding. Each successive
round doubles the threshold for a **new** blocking finding:

| Round | New-blocker threshold |
|------:|----------------------:|
| 1 | 1x (baseline) |
| 2 | 2x |
| 3 | 4x |
| 4 | 8x |
| N | `2^(N-1)`x |

For a PR/MR, count completed deep-review panel verdicts from earlier
invocations; the current invocation is the next round. A retry, duplicate post,
or repost of one verdict does not create another round. If the user explicitly
supplies a round, use it. Without review history or explicit round context, use
round 1.

## Classify carried and new findings

1. Inventory prior BLOCKING findings by their underlying defect, not by title,
   line number, or wording, which may change between revisions.
2. Keep every unresolved prior blocker BLOCKING. It does not need to satisfy the
   current multiplier again. Require evidence before treating it as resolved.
3. Treat a finding as new when no earlier verdict classified the underlying
   defect as BLOCKING. Promoting an earlier suggestion or note is also a new
   blocker. A defect shown resolved in an intervening verdict and later
   reintroduced is a new regression.
4. Apply the multiplier only when deciding whether a new finding is BLOCKING.
   The multiplier raises the combined bar for evidence, confidence, likelihood
   in supported use, and consequence of merging. It is a comparative decision
   rule, not an arithmetic bug score: at 2x a candidate must be materially more
   compelling than an ordinary blocker; at 4x it needs high confidence and
   severe merge impact; at 8x and beyond only increasingly exceptional,
   well-supported risks should block.
5. Report a new finding that misses the current blocking threshold as a
   SUGGESTION or NOTE. Do not suppress it, and do not let it determine the
   disposition.

Reproducer confirmation strengthens the evidence side of the threshold but
does not bypass the multiplier for a new finding. An unresolved blocker from an
earlier round continues to block even if no new reproduction is needed.

## Arbiter output

State the round and multiplier in the disposition. Separate carried blockers
from new findings, and say whether each new BLOCKING finding cleared the
current threshold. This makes convergence decisions auditable across rounds.
