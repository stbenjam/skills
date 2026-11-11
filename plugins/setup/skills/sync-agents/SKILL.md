---
name: sync-agents
description: Use when asked to set up, sync, or update all local AI agents (Claude Code, Codex, Grok, Muse, and their work/personal profiles) so every agent has the same skills and working principles.
license: MIT
metadata:
  author: stbenjam
  version: "0.5.0"
user-invocable: true
disable-model-invocation: true
---

# Sync local agents

Give every local agent the same skills, shared through `~/.agents/skills` instead of plugins or marketplaces, and the same working principles in its global instructions.

## Skills everyone gets

- `stbenjam/skills`: every skill in the `diagrams`, `loops`, `reviews`, `rules`, `steering`, and `setup` plugins
- `mattpocock/skills`: `grill-me` and its `grilling` dependency
- `addyosmani/agent-skills`: `idea-refine`, `code-simplification`

## Steps

1. Clone each repo above to `~/.agents/src/<owner>/<repo>`, or `git pull` it if it's already there.
2. Symlink each listed skill directory from those checkouts into `~/.agents/skills/<skill>`. Don't copy. If two skills have the same name, report it instead of overwriting.
3. Find every agent home, e.g. `~/.claude*`, `~/.codex`, `~/.grok*`, `~/.muse*`, `~/.config/muse*`, `CLAUDE_CONFIG_DIR`, `CODEX_HOME`. Treat each `~/.claude-*` directory as its own agent home. Skip `~/.codex-*` directories: T3 Code shadows them and every Codex profile shares `~/.codex`. Skip leftovers with no config file.
4. For each agent that doesn't read `~/.agents/skills` itself (Claude doesn't; Codex and Grok do), symlink each skill into that home's skills directory.
5. Install the principles. Read [principles.md](principles.md) and put its contents in each agent home's global instructions file: `CLAUDE.md` for Claude, `AGENTS.md` for Codex and Grok, and whatever file the agent's docs name for the rest. Wrap it in `<!-- BEGIN stbenjam/skills principles -->` and `<!-- END stbenjam/skills principles -->`, replacing any existing block between those markers. Leave the rest of the file alone. Load the block once per agent: if an agent also reads another agent's file (Grok reads `~/.claude/CLAUDE.md`), don't give it a second copy. Skip files managed by an organization policy.
6. Clean up old installs so skills don't appear twice: in every agent home, uninstall plugins from the listed repos, remove their marketplaces, and delete old copies or dangling symlinks of listed skills, including cached plugin copies.
7. List other plugins, marketplaces, and skills. Ignore built-ins that ship with the agent or sync from its account, such as Claude's official marketplace or Codex's curated one. For each extra, ask the user: remove it everywhere, or open a PR to `stbenjam/skills` adding it to this list.
8. Report what changed per agent home. Running sessions need a restart.
