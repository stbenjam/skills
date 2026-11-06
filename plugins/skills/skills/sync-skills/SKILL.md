---
name: sync-skills
description: Use when asked to set up, sync, or update skills and plugins across all local AI agents (Claude Code, Codex, Grok, Muse, and their work/personal profiles) so every agent has the same up-to-date set.
license: MIT
metadata:
  author: stbenjam
  version: "0.1.0"
---

# Sync skills across local agents

## Plugins everyone gets

- `stbenjam/skills` marketplace: `loops`, `reviews`, `rules`, `steering`, `skills`
- `mattpocock/skills` marketplace: `mattpocock-skills`

## Steps

1. Find every agent home on this host, e.g. `~/.claude*`, `~/.codex*`, `~/.grok*`, `~/.muse*`, and `CLAUDE_CONFIG_DIR` or `CODEX_HOME`. Skip leftovers with no config file.
2. For each home, use the agent's own plugin CLI pointed at that home (check `--help`). Add the marketplaces, install anything missing, and update what's already installed to the latest version.
3. If an agent has no plugin support, symlink each plugin's `skills/*` directories into `~/.agents/skills`, then symlink them from `~/.agents/skills` into that agent's skills directory. Don't copy: links stay current when plugins update.
4. List plugins and marketplaces that aren't on the list above. For each, ask the user: remove it everywhere, or open a PR to `stbenjam/skills` adding it to this list.
5. Report a table of agent home × plugin with versions. Note that running sessions need a restart.
