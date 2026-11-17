# Resolving review threads

Details for Phase 4 Step 4.2 of SKILL.md.

## Reply, then resolve

After pushing your changes, for **each addressed thread**:

1. **Reply first** — always reply to the review comment *before*
   resolving. Reference the commit SHA that addressed it, e.g.
   `Fixed in <sha>.` For declined suggestions, explain your
   reasoning so the reviewer understands before the thread closes.
   Post via `gh api` to the review comment.
2. **Then resolve** the thread via the GraphQL mutation:

```bash
gh api graphql -f query='
mutation($threadId: ID!) {
  resolveReviewThread(input: {threadId: $threadId}) {
    thread { id isResolved }
  }
}' -f threadId="<thread_node_id>"
```

Only resolve threads you actually addressed. Reply-to (do not
resolve) threads you answered, deferred, or skipped.

## Verify resolution

After resolving, re-query the PR's review threads and confirm
each thread you resolved now reports `isResolved: true`:

```bash
gh api graphql -f query='
query($owner: String!, $repo: String!, $pr: Int!) {
  repository(owner: $owner, name: $repo) {
    pullRequest(number: $pr) {
      reviewThreads(first: 100) {
        nodes { id isResolved }
      }
    }
  }
}' -f owner="<owner>" -f repo="<repo>" -F pr=<pr_number>
```

Retry the resolve mutation for any thread that did not stick.
**Do not report a thread as resolved without confirming
`isResolved: true` in this re-query.**

## Threads with filtered originals

A thread's original comment may be filtered as untrusted (e.g.
by `fetch_comments.py`) while a later trusted reply claims a fix
already landed. Do not resolve on the claim alone:

1. Verify the claimed fix actually exists in the branch — check
   the referenced commit or the cited code.
2. If confirmed, reply and resolve the thread (see above).
3. If not confirmed, leave the thread unresolved and notify the
   user.
