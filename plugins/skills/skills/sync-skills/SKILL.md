---
name: sync-skills
description: Use when asked to set up, sync, or update skills across all local AI agents (Claude Code, Codex, Grok, Muse, and their work/personal profiles) so every agent has the same up-to-date set.
license: MIT
metadata:
  author: stbenjam
  version: "0.2.0"
---

# Sync skills across local agents

Share skills through `~/.agents/skills` instead of installing plugins or marketplaces.

## Skills everyone gets

- `stbenjam/skills`: every skill in the `loops`, `reviews`, `rules`, `steering`, and `skills` plugins
- `mattpocock/skills`: `grill-me` and its `grilling` dependency

## Steps

1. Clone each repo above to `~/.agents/src/<owner>/<repo>`, or `git pull` it if it's already there.
2. Symlink each listed skill directory from those checkouts into `~/.agents/skills/<skill>`. Don't copy. If two skills have the same name, report it instead of overwriting.
3. Find every agent home, e.g. `~/.claude*`, `~/.codex*`, `~/.grok*`, `~/.muse*`, `CLAUDE_CONFIG_DIR`, `CODEX_HOME`. Skip leftovers with no config file.
4. For each agent that doesn't read `~/.agents/skills` itself (Claude doesn't; Codex does), symlink each skill into that home's skills directory.
5. Clean up old installs so skills don't appear twice: in every agent home, uninstall plugins from the listed repos, remove their marketplaces, and delete old copies or dangling symlinks of listed skills.
6. List other plugins, marketplaces, and skills. Ignore built-ins that ship with the agent or sync from its account, such as Claude's official marketplace or Codex's curated one. For each extra, ask the user: remove it everywhere, or open a PR to `stbenjam/skills` adding it to this list.
7. Report what changed per agent home. Running sessions need a restart.
