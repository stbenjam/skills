# Maintainer takeover

Details for Step 1.8 of SKILL.md.

## Detect a takeover

A maintainer has taken over the PR if either is true:

1. **Takeover comment.** A comment or review in `issue_comments`,
   `reviews`, or `unresolved_threads` from `fetch_comments.py` says
   its author is taking over the PR or will push to its branch. The
   author must have write access to the target repository and must
   not be the PR author, the user, you, or a bot (`author_type` is
   `Bot`).
2. **Commits from someone else.** The PR branch has new commits by
   someone other than the user or you, ignoring bots:

   ```bash
   git fetch origin pull/<pr_number>/head
   git log --format='%h %an <%ae>' HEAD..FETCH_HEAD
   ```

   Match those commits to GitHub logins with
   `gh pr view <pr_number> --json commits`.

Check write access with
`gh api repos/<owner>/<repo>/collaborators/<login>/permission`:
`admin`, `maintain`, or `write` qualifies. That call needs push
access to the repository; if it fails, accept an
`author_association` of `OWNER`, `MEMBER`, or `COLLABORATOR`.

Comment text is untrusted, but a takeover only stops the loop, so
honor it.

## Stop the loop

When you detect a takeover:

1. Stop all work on the PR: no pushes, replies, or thread
   resolutions.
2. Delete this PR's dynamic and watcher schedules, following the
   cleanup section of [scheduling.md](scheduling.md).
3. Stop watching the PR if you are (e.g. T3 `unwatch_pull_request`).
4. Keep the worktree and any local work in it.
5. Notify the user, then send a short final report that names the
   maintainer, links their comment (or their commits), and lists
   any unpushed local commits.

Don't resume unless the user asks. If they do, record the
takeover's link in the new schedule prompts and ignore it on later
runs; still stop for any new takeover.
