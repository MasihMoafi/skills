#!/usr/bin/env python3
"""Validate the tracked public SKILL.md set and its index documentation."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


PUBLIC_LINE = re.compile(
    r"^\s*\d+\s+general-purpose skills are public:\s*(?P<list>.+)$",
    re.MULTILINE,
)
README_ITEM = re.compile(
    r"^\s*-\s+\*\*\[`(?P<name>[a-z0-9][a-z0-9-]*)`\]"
    r"\((?P<path>[^)]+/SKILL\.md)\)",
    re.MULTILINE,
)
FRONTMATTER = re.compile(r"\A---\n(?P<body>.*?)\n---(?:\n|\Z)", re.DOTALL)
NAME_FIELD = re.compile(r"^name:\s*(?P<value>\S.*)\s*$", re.MULTILINE)
DESCRIPTION_FIELD = re.compile(
    r"^description:\s*(?P<value>\S.*)\s*$", re.MULTILINE
)


def git_output(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git command failed")
    return result.stdout


def tracked_skill_names(root: Path) -> set[str]:
    names = set()
    for raw_path in git_output(root, "ls-files", "--", "*/SKILL.md").splitlines():
        path = Path(raw_path)
        if len(path.parts) == 2 and path.name == "SKILL.md":
            names.add(path.parent.name)
    return names


def public_skill_names(vision: str) -> set[str]:
    match = PUBLIC_LINE.search(vision)
    if not match:
        raise ValueError("VISION.md does not declare the public skill list")
    public_part = match.group("list").split("Deliberately excluded", 1)[0]
    return set(re.findall(r"`([a-z0-9][a-z0-9-]*)`", public_part))


def readme_skill_names(readme: str) -> set[str]:
    start = readme.find("## Available skills")
    end = readme.find("\n## ", start + 1) if start >= 0 else -1
    if start < 0:
        raise ValueError("README.md does not contain '## Available skills'")
    section = readme[start:] if end < 0 else readme[start:end]
    return {match.group("name") for match in README_ITEM.finditer(section)}


def ignored(root: Path, relative_path: str) -> bool:
    result = subprocess.run(
        ["git", "-C", str(root), "check-ignore", "-q", "--", relative_path],
        check=False,
    )
    return result.returncode == 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "root",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="skills repository root (default: parent of scripts/)",
    )
    args = parser.parse_args()
    root = args.root.resolve()

    errors: list[str] = []
    warnings: list[str] = []
    try:
        tracked = tracked_skill_names(root)
        public = public_skill_names((root / "VISION.md").read_text(encoding="utf-8"))
        documented = readme_skill_names((root / "README.md").read_text(encoding="utf-8"))
    except (OSError, RuntimeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    for label, actual in (("VISION.md", public), ("README.md", documented)):
        missing = sorted(tracked - actual)
        extra = sorted(actual - tracked)
        if missing:
            errors.append(f"{label} is missing tracked skills: {', '.join(missing)}")
        if extra:
            errors.append(f"{label} lists non-public/untracked skills: {', '.join(extra)}")

    for name in sorted(tracked):
        path = root / name / "SKILL.md"
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            errors.append(f"{path}: {exc}")
            continue
        match = FRONTMATTER.match(text)
        if not match:
            errors.append(f"{path}: missing YAML frontmatter")
            continue
        body = match.group("body")
        name_match = NAME_FIELD.search(body)
        description_match = DESCRIPTION_FIELD.search(body)
        frontmatter_name = (
            name_match.group("value").strip("\"'") if name_match else None
        )
        if frontmatter_name != name:
            errors.append(f"{path}: frontmatter name must be {name!r}")
        if not description_match:
            errors.append(f"{path}: frontmatter description is missing")

    for child in sorted(root.iterdir()):
        skill_path = child / "SKILL.md"
        if not child.is_dir() or child.name in tracked or not skill_path.exists():
            continue
        relative = skill_path.relative_to(root).as_posix()
        if not ignored(root, relative):
            warnings.append(f"untracked local skill candidate: {relative}")

    for warning in warnings:
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"OK: {len(tracked)} tracked public skills match VISION.md and README.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
