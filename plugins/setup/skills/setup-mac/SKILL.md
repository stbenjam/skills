---
name: setup-mac
description: Use when asked to set up a Mac with the user's favorite software and preferred configuration.
license: MIT
metadata:
  author: stbenjam
  version: "0.1.0"
disable-model-invocation: true
---

# Set up a Mac

Install and configure this software the way the user likes it. Check what's already installed and use current official sources and installation methods. Adapt to the machine and the user's requests.

- Apps: Amphetamine, BetterDisplay, Discord, iTerm2, Linear, LookAway, Portal, Rectangle, Shottr, T3 Code (stable), Tailscale, TypeWhisper, Visual Studio Code, and Xiaomi Interconnectivity.
- Development: Homebrew, Apple Command Line Tools, Bun, Claude Code, Codex CLI, GitHub CLI, Go, Harbor CLI, uv, Podman, Docker CLI and Compose, GnuPG, Pinentry Mac, YubiKey Manager CLI, ripgrep, ShellCheck, tmux, yamllint, and yq. Prefer Podman; Colima is optional and shouldn't start automatically.
- Shell and editor: zsh with Oh My Zsh, a Powerline prompt, MesloLGS Nerd Font, and a dark Gruvbox iTerm2 theme with a slightly darker background. Install Even Better TOML in VS Code.
- TypeWhisper: local Parakeet TDT v3, activated with right Command.
- LG ultrawide: use BetterDisplay's flexible scaling and a 2752 × 1152 HiDPI custom resolution at 60 Hz when supported. Apply and activate the configuration, then verify the active mode.

Help with sign-ins, permissions, and YubiKey-backed SSH as needed; let the user enter credentials and PINs. Keep account identities, hostnames, device identifiers, and other private details out of this skill.
