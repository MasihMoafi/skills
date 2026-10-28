#!/usr/bin/env python3
"""Clear the clutter Claude Code, Codex, Elpis and AGY keep adding. Moves to the desktop trash (gio trash), never rm.

Dry run by default: prints what would go, per category. `--apply` moves it. `--list` prints every path.
`--also PATH ...` adds explicit one-off targets. Spared, always: anything touched in the last 24 hours
(`--hours` to change), anything a running process has open, memory folders, credentials, live configs,
databases, prompt history, skills, plugins, jobs and plans.
"""
import argparse
import os
import re
import subprocess
import sys
import time
from pathlib import Path

HOME = Path.home()
PROTECTED_NAME = re.compile(r'^(auth\.json|\.credentials.*|.*\.key|config\.toml|settings(\.local)?\.json|history\.jsonl'
                            r'|.*\.sqlite(-shm|-wal)?|CLAUDE\.md|AGENTS\.md|ES\.md)$')
PROTECTED_PART = {'memory', 'memories', 'skills', 'plugins', 'jobs', 'plans', 'hooks', '.ES'}
CLAUDE_ROOTS = [HOME / '.claude', *sorted(HOME.glob('.elpis-next/elpis-claude/claude-accounts/*'))]
AGY = HOME / '.gemini/antigravity-cli'
BACKUP_NAME = re.compile(r'(\.bak\b|\.bak-|\.orig$|\.old$|\.pre-|\.before-|backup)', re.I)


def open_files():
    found = set()
    for fd_dir in Path('/proc').glob('[0-9]*/fd'):
        try:
            for fd in fd_dir.iterdir():
                try:
                    found.add(os.readlink(fd))
                except OSError:
                    pass
        except OSError:
            pass
    return found


def newest(path):
    """Latest modification time inside a file or folder."""
    if path.is_file() or path.is_symlink():
        return path.lstat().st_mtime
    times = [path.stat().st_mtime]
    for p in path.rglob('*'):
        try:
            times.append(p.lstat().st_mtime)
        except OSError:
            pass
    return max(times)


def size(path):
    if path.is_file() or path.is_symlink():
        return path.lstat().st_size
    return sum(p.lstat().st_size for p in path.rglob('*') if p.is_file())


def files_under(*roots, pattern='*'):
    for root in roots:
        root = HOME / root
        if root.is_dir():
            yield from (p for p in root.rglob(pattern) if p.is_file())


def claude_dirs(*names):
    return (p for root in CLAUDE_ROOTS for d in names for p in (root / d).glob('*'))


def claude_sessions():
    """A Claude session is its transcript plus the same-named folder (subagents, tool results)."""
    for root in CLAUDE_ROOTS:
        for transcript in (root / 'projects').glob('*/*.jsonl'):
            yield (transcript, transcript.with_suffix(''))


def agy_sessions():
    """An AGY session is its conversation database, brain folder and annotation, all named by its ID."""
    ids = {p.stem for p in (AGY / 'conversations').glob('*.db')} | {p.name for p in (AGY / 'brain').glob('*-*')}
    for i in sorted(ids):
        yield (AGY / 'conversations' / f'{i}.db', AGY / 'brain' / i, AGY / 'annotations' / f'{i}.pbtxt')


def backups():
    for root in ('.claude', '.codex', '.elpis', '.elpis-next', '.gemini', '.config/rag'):
        root = HOME / root
        if root.is_dir():
            yield from (p for p in root.iterdir() if p.is_file() and BACKUP_NAME.search(p.name))
    claude_backups = HOME / '.claude/backups'
    if claude_backups.is_dir():
        yield from claude_backups.iterdir()


CATEGORIES = {
    'Claude chat logs': claude_sessions,
    'Claude file history': lambda: claude_dirs('file-history'),
    'Claude scratch (shell snapshots, paste cache, debug)': lambda: claude_dirs('shell-snapshots', 'paste-cache', 'debug'),
    'Codex chat logs': lambda: files_under('.codex/sessions', '.codex/archived_sessions', pattern='*.jsonl'),
    'Elpis chat logs': lambda: files_under('.elpis/sessions', '.elpis-next/sessions', '.elpis/archived_sessions',
                                           '.elpis-next/archived_sessions', pattern='*.jsonl'),
    'AGY chat logs': agy_sessions,
    'Agent logs (Codex, Elpis, AGY)': lambda: (p for p in files_under('.codex/logs', '.codex/log', '.elpis/logs',
                                                                       '.elpis-next/logs', '.gemini/antigravity-cli/log')
                                               if p.suffix != '.sqlite'),
    'Codex per-run configs': lambda: (p for p in (HOME / '.codex').glob('*.config.toml')),
    'Backups': backups,
}


def spared(path, cutoff, busy):
    if PROTECTED_NAME.match(path.name) or PROTECTED_PART & set(path.relative_to(HOME).parts[:-1] + (path.name,)):
        return 'protected'
    if newest(path) > cutoff:
        return 'recent'
    if str(path) in busy or (path.is_dir() and any(b.startswith(str(path) + '/') for b in busy)):
        return 'open'
    return None


def human(n):
    for unit in ('B', 'K', 'M', 'G'):
        if n < 1024:
            return f'{n:.0f}{unit}'
        n /= 1024
    return f'{n:.1f}T'


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--apply', action='store_true', help='move the targets to the trash')
    ap.add_argument('--list', action='store_true', help='print every target path')
    ap.add_argument('--hours', type=float, default=24, help='spare anything touched this recently (default 24)')
    ap.add_argument('--also', nargs='*', default=[], help='extra explicit paths to trash')
    args = ap.parse_args()

    cutoff, busy = time.time() - args.hours * 3600, open_files()
    plan, skipped = [], {}
    sources = dict(CATEGORIES)
    if args.also:
        sources['Named extras'] = lambda: (Path(p).expanduser().resolve() for p in args.also)
    for name, source in sources.items():
        targets = []
        for item in source():
            # A tuple is one session: its parts go together or stay together.
            group = [p for p in (item if isinstance(item, tuple) else (item,)) if p.exists() or p.is_symlink()]
            if not group:
                continue
            reasons = [None if name == 'Named extras' else spared(p, cutoff, busy) for p in group]
            if name == 'Named extras' and any(p == HOME or HOME not in p.parents for p in group):
                reasons.append('outside home')
            reason = next((r for r in reasons if r), None)
            if reason:
                skipped[reason] = skipped.get(reason, 0) + 1
            else:
                targets.extend(group)
        total = sum(size(p) for p in targets)
        plan.append((name, targets, total))
        print(f'{human(total):>7}  {len(targets):6} items  {name}')
        if args.list:
            print('\n'.join(f'           {p}' for p in targets))
    print(f'{human(sum(t for _, _, t in plan)):>7}  total;  spared: {skipped}')

    if not args.apply:
        print('Dry run. Add --apply to move these to the trash.')
        return
    moved = 0
    for _, targets, _ in plan:
        for i in range(0, len(targets), 200):
            batch = [str(p) for p in targets[i:i + 200] if p.exists()]
            if batch:
                subprocess.run(['gio', 'trash', '--', *batch], check=True)
                moved += len(batch)
    print(f'Moved {moved} items to the trash.')


if __name__ == '__main__':
    sys.exit(main())
