---
name: clean-system
description: Use when the user asks to clean up, reclaim disk space, or clear the clutter Claude Code, Codex and Elpis keep adding (old chat logs, file history, logs, backups). Agent clutter is cleared aggressively by default; caches and Docker still need approval.
metadata:
  short-description: Aggressively clear agent clutter; audit other disk use
---

# System clean-up

Masih (14 Oct 2026): "make it more aggressive as claude and codex just keep adding shit"; "I hate backups"; "make sure all those get deleted safely".

## 1. Agent clutter: clear it, don't ask per item

Run `python3 ~/Desktop/p/skills/clean-system/clean.py` (dry run), show the per-category totals, then run it with `--apply`.
- **What it clears:** old Claude, Codex and Elpis chat logs, Claude file history and scratch, Codex and Elpis logs, Codex per-run configs, and backups (`*.bak`, `*.pre-*`, `*.before-*`, `*backup*`) in the agent config folders.
- **One-off targets:** add them with `--also PATH ...`.
- **What it always spares:**
  - anything touched in the last 24 hours, or open in a running process;
  - memory folders, credentials, live `config.toml` and `settings.json`, databases, prompt history;
  - skills, plugins, jobs, plans, `ES.md`.
- Everything goes to the desktop trash (`gio trash`), never `rm`.
- **Make no backups.** The trash is the only safety net.
- If an auto-mode classifier blocks `--apply`, don't work around it. Give Masih the exact `! python3 … --apply` command to run himself.

## 2. Everything else: audit, then ask

Package caches and Docker hold other projects' state, so list the targets with sizes and get Masih's yes per category.
- **Caches:**
  - **uv:** `du -sh ~/.cache/uv`, cleaned by `uv cache clean`.
  - **pip:** `~/.cache/pip`, cleaned by `pip cache purge`.
  - **conda:** `~/miniconda3/pkgs`, cleaned by `conda clean --all -y`.
  - **npm:** `~/.npm/_cacache`, cleaned by `npm cache clean --force`.
  - **pnpm:** `pnpm store prune`. Never delete the store folder.
- **Docker:** run `docker system df`. Images, containers and build cache are separate approvals. Volumes need their own explicit yes because they may hold irreplaceable data.
- Never target a home directory, workspace root, unresolved variable or broad glob.

## 3. Verify

Rerun the dry run and `df -h /`. Report what moved and how much space was freed. Note that it all sits in the trash until Masih empties it.
