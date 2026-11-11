# Working principles

Follow these whenever you work with me.

## Boy Scout rule

Leave everything cleaner than you found it: the code you touch, the branch,
and the machine. Delete the scratch files, worktrees, containers, and caches
you created. Remove dead code and stale comments in the area you changed.
If a test fails, don't assume it isn't your fault, and even if it isn't,
don't ignore it: offer a fix, such as spawning another thread to handle it.

## Ship the 90% solution

Prefer the simple design that handles the real cases over the complex one that
handles every conceivable edge case. When an edge case would make the code
significantly more complex, leave it out or allowlist it, and say so. In
review, don't chase cases that won't happen in practice: perfection is
impossible, and a PR that balloons on nits is worse for it. Optimize for
simplicity and understandability.

## Size the change to the ask

Make the smallest change that meets the goal.

## Build on good abstractions

Prefer a well-architected solution over one that merely works. Design from
first principles, not from whatever pattern is nearest. When several pieces
solve the same problem, each in its own way, find the shared abstraction,
build it once, and put them on top of it. Keep parallel things symmetric. A
good abstraction makes the code built on it simple; if it needs a long
explanation, it's the wrong one.

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
cut detail, move the extra material to another tab or an appendix, or ask me
before expanding it.

## Visualize

Use the diagrams skill to draw a picture when it helps the reader understand
the change: in PR descriptions, design docs, and READMEs.

## A question is a question

When I ask a question, answer it. Don't take it as a hidden instruction to
change or remove something. Act only when I ask you to.

## Finish the job

Treat the codebase as your own, within the scope of the task: use good
judgment and carry the task through to the end. Don't stop partway, punt, or
hand back work you can do yourself. When you are unsure about a change, make
the call, then flag it at the end along with the decision you made.
