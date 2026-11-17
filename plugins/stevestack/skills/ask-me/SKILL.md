---
name: ask-me
description: Brainstorm an unsettled idea together, one question at a time.
license: MIT
metadata:
  author: stbenjam
  version: "0.1.0"
user-invocable: true
disable-model-invocation: true
argument-hint: "[topic]"
---

I don't quite know what I want yet, so let's brainstorm the topic together.
Ask me questions one at a time, and wait for my answer before asking the
next. Format each question like this:

**Q1** - **<question>**

Recommended answer: <your recommended answer>

Out-of-the-box alternative: <a bolder or unconventional option>

The absolute most minimal option: <the smallest thing that could work>

Trade-offs: <what each option gains and gives up>

Treat the topic as a tree of decisions, where each decision opens the ones
that depend on it. Only ask a question once everything it depends on is
settled; never make me answer on top of a guess. Each answer settles a
branch and opens new ones, so choose the next question from what is now
answerable.

Facts are yours to find; decisions are mine to make. When a question needs
something you could look up (code, files, tools, docs), send a subagent with
a fresh context to find it instead of asking me. Don't wait on it: only the
questions that depend on that fact wait, so keep asking the others.

We're done when no open questions remain: every branch explored and nothing
quietly assumed. Then summarize what we decided and wait for me to confirm
we agree before acting on it.
