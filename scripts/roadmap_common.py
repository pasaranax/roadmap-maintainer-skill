#!/usr/bin/env python3

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import List, Optional

PHASE_FILE_NAME = "00-phase.md"
MIN_PYTHON = (3, 8)


def ensure_supported_python() -> None:
    if sys.version_info < MIN_PYTHON:
        raise SystemExit(
            "Roadmap scripts require Python {0}.{1}+; current interpreter is {2}.{3}.{4}".format(
                MIN_PYTHON[0],
                MIN_PYTHON[1],
                sys.version_info.major,
                sys.version_info.minor,
                sys.version_info.micro,
            )
        )


def today_iso() -> str:
    return date.today().isoformat()


def slugify(value: str) -> str:
    slug = value.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    if not slug:
        raise ValueError("Could not derive a non-empty slug from the provided title.")
    return slug


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def ensure_phase_dir(path: Path) -> None:
    if not path.exists() or not path.is_dir():
        raise ValueError(f"Phase directory not found: {path}")
    phase_file = path / PHASE_FILE_NAME
    if not phase_file.exists():
        raise ValueError(f"Missing phase file: {phase_file}")


def parse_heading_title(phase_file: Path) -> str:
    for line in read_text(phase_file).splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError(f"Could not find a markdown heading in {phase_file}")


def next_slice_number(phase_dir: Path) -> int:
    max_number = 0
    for path in phase_dir.glob("*.md"):
        match = re.match(r"^(\d{2})-.*\.md$", path.name)
        if not match or path.name == PHASE_FILE_NAME:
            continue
        max_number = max(max_number, int(match.group(1)))
    return max_number + 1


def set_metadata_value(content: str, key: str, value: str, after_key: Optional[str] = None) -> str:
    pattern = re.compile(rf"^{re.escape(key)}: .*$", re.MULTILINE)
    replacement = f"{key}: {value}"
    if pattern.search(content):
        return pattern.sub(replacement, content, count=1)
    lines = content.splitlines()
    if after_key:
        for index, line in enumerate(lines):
            if line.startswith(f"{after_key}: "):
                lines.insert(index + 1, replacement)
                return "\n".join(lines)
    lines.insert(1, replacement)
    return "\n".join(lines)


@dataclass(frozen=True)
class RoadmapDirs:
    root: Path
    current: Path
    longterm: Path
    archive: Path


def resolve_roadmap_dirs(root: Path) -> RoadmapDirs:
    root = root.resolve()
    current = root / "current"
    longterm = root / "longterm"
    archive = root / "archive"
    for path in (root, current, longterm, archive):
        if not path.exists() or not path.is_dir():
            raise ValueError(f"Required roadmap directory not found: {path}")
    return RoadmapDirs(root=root, current=current, longterm=longterm, archive=archive)


def list_phase_dirs(parent: Path) -> List[Path]:
    return sorted(path for path in parent.iterdir() if path.is_dir())


def active_phase_dir(roadmap_root: Path) -> Path:
    dirs = resolve_roadmap_dirs(roadmap_root)
    active = list_phase_dirs(dirs.current)
    if len(active) != 1:
        raise ValueError(
            f"`current/` must contain exactly one phase directory, found {len(active)}."
        )
    ensure_phase_dir(active[0])
    return active[0]


def find_phase_in_bucket(parent: Path, phase: str) -> Path:
    direct = parent / phase
    if direct.exists():
        ensure_phase_dir(direct)
        return direct
    normalized = phase
    if phase.isdigit():
        normalized = f"phase-{int(phase):02d}-"
    matches = []
    for path in list_phase_dirs(parent):
        if path.name == phase or path.name.startswith(normalized):
            matches.append(path)
    if not matches:
        raise ValueError(f"Could not find phase `{phase}` in {parent}")
    if len(matches) > 1:
        raise ValueError(
            f"Phase reference `{phase}` is ambiguous in {parent}: "
            + ", ".join(path.name for path in matches)
        )
    ensure_phase_dir(matches[0])
    return matches[0]
