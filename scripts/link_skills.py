#!/usr/bin/env python3
"""Make the skill registries mirror Masih's skills library, ~/Desktop/p/skills/<name>/SKILL.md.

- Each registry (~/.claude/skills, ~/.agents/skills, ~/.codex/skills) gets <name> -> the library folder; a link
  that points elsewhere is replaced. A link whose target is gone or has no SKILL.md is removed (os.unlink).
- $CLAUDE_CONFIG_DIR/skills mirrors ~/.claude/skills entry for entry: <name> -> ~/.claude/skills/<name>.
- Only symlinks are ever changed; Elpis's `synced` folder in the config dir is left alone. A real directory in the way, or one without SKILL.md, is reported as a conflict.
Usage: link_skills.py           apply; print one line per change or conflict (exit 1 if a conflict remains)
       link_skills.py --check   change nothing; print one line per problem, or `skills: ok` (exit 1 on problems)
Tests: python3 test_link_skills.py
"""
import os, sys
from pathlib import Path

HOME = Path.home()
LIBRARY = HOME / 'Desktop/p/skills'
REGISTRIES = (HOME / '.claude/skills', HOME / '.agents/skills', HOME / '.codex/skills')  # the first is Claude Code's
CONFIG = Path(os.environ.get('CLAUDE_CONFIG_DIR')
              or '/home/masih/.elpis-next/elpis-claude/claude-accounts/66601136-bf70-4727-8da3-0e2e8efc7e99') / 'skills'
NOT_SKILLS = {'dev', 'scripts'}
ELPIS_OWNED = {'synced'}  # Elpis recreates this in the config dir; it is not a skill


def show(path):
    return str(path).replace(str(HOME), '~', 1)


def library(root):
    """Every folder directly under root that holds a SKILL.md, by name."""
    return {d.name: d.absolute() for d in sorted(root.iterdir()) if d.is_dir() and not d.name.startswith('.')
            and d.name not in NOT_SKILLS and (d / 'SKILL.md').is_file()}


def entries(registry):
    """Visible entries, broken links included."""
    return sorted(p for p in registry.iterdir() if not p.name.startswith('.')) if registry.is_dir() else []


def sync(lib, registries, config, apply=False):
    """Return one line per problem; with apply=True, fix them and return one line per change or conflict."""
    out, skills = [], library(lib)

    def link(path, target):
        if path.is_symlink() and os.readlink(path) == str(target):
            return
        if path.exists() and not path.is_symlink():
            return out.append(f'conflict {show(path)}: a real directory, not a link to {show(target)}')
        if not apply:
            return out.append(f'{"wrong" if path.is_symlink() else "missing"} {show(path)}')
        if path.is_symlink():
            os.unlink(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.symlink_to(target)
        out.append(f'linked {show(path)} -> {show(target)}')

    def prune(path):
        if not path.is_symlink():
            return out.append(f'conflict {show(path)}: a real directory without SKILL.md')
        if apply:
            os.unlink(path)
        out.append(f'{"pruned" if apply else "dangling"} {show(path)}')

    for registry in registries:
        for name, folder in skills.items():
            link(registry / name, folder)
        for entry in entries(registry):
            if entry.name not in skills and not (entry / 'SKILL.md').is_file():
                prune(entry)

    claude = registries[0]
    names = {entry.name for entry in entries(claude)}
    for name in sorted(names):
        link(config / name, claude / name)
    for entry in entries(config):
        if entry.name not in names and entry.name not in ELPIS_OWNED:
            prune(entry)
    return out


def check():
    """The problems in the real registries (used by findability/check_pointers.py)."""
    return sync(LIBRARY, REGISTRIES, CONFIG)


def main(argv, lib=LIBRARY, registries=REGISTRIES, config=CONFIG):
    apply = '--check' not in argv
    out = sync(lib, registries, config, apply)
    print('\n'.join(out) or ('skills: nothing to change' if apply else 'skills: ok'))
    return int(any(line.startswith('conflict') for line in out) if apply else bool(out))


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
