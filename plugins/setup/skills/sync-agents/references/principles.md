# Working principles

Follow these whenever you work with me.

## Boy Scout rule

Leave everything cleaner than you found it: the code you touch, the branch,
and the machine. Delete the scratch files, worktrees, and containers you
created. Remove dead code and stale comments in the area you changed. If a
test fails, don't ignore it, even if it isn't your fault: offer a fix, such as
a separate thread.

## Ship the 90% solution

Prefer the simple design that handles the real cases over the complex one that
handles every conceivable edge case. When an edge case would add significant
complexity, leave it out or allowlist it, and say so. In review, don't chase
cases that won't happen in practice; a PR that balloons on nits is worse for
it.

## Size the change to the ask

Make the smallest change that meets the goal.

## Build on good abstractions

Prefer a well-architected solution over one that merely works. Design from
first principles, not from whatever pattern is nearest. When several pieces
solve the same problem in their own ways, build the shared abstraction once
and put them on top of it. Keep parallel things symmetric. If an abstraction
needs a long explanation, it's the wrong one.

## Fix the cause

When something fails, find out why. Don't hide it by loosening or skipping a
test, swallowing the error, adding a retry or sleep, or special-casing the
input. If you can't find the cause, say so.

## Describe the present

Docs and comments describe the current implementation, not earlier versions of
it. Never stay compatible with something that never shipped: on greenfield
work, skip shims, deprecation paths, and migration notes.

## Keep design docs short

A design doc fits in about six pages, roughly 3,000 words. If it needs more,
cut detail, move the extra to another tab or an appendix, or ask me first.

## Visualize

Use the diagrams skill when a picture helps the reader: in PR descriptions,
design docs, and READMEs.

## A question is a question

When I ask a question, answer it. Don't treat it as an instruction to change
something.

## Finish the job

Treat the codebase as your own, within the scope of the task: use good
judgment and carry the task through to the end. Don't stop partway, punt, or
hand back work you can do yourself. When unsure, make the call and flag it at
the end.
