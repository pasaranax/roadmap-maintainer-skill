#!/usr/bin/env python3

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

from roadmap_common import ensure_supported_python, today_iso, write_text


HUMAN_BRIEF_HEADING = "# Human-authored project brief. Agent editing is forbidden."


def render_human_brief(brief_text: Optional[str]) -> str:
    if brief_text is None or not brief_text.strip():
        return HUMAN_BRIEF_HEADING
    return "{0}\n\n{1}".format(HUMAN_BRIEF_HEADING, brief_text.rstrip("\n"))


def render_index(today: str, repo_root: str, human_brief_rel: str, brief_captured: bool) -> str:
    current_status = (
        "bootstrap_pending_initial_roadmap" if brief_captured else "bootstrap_pending_human_brief"
    )
    return """# Roadmap Index

Last updated: {0}
Current phase path: unset
Current slice path: unset
Current phase: unset
Current status: {3}

## Read Order

1. Read [`HUMAN_BRIEF.md`]({1}/{2}) first.
2. If `HUMAN_BRIEF.md` contains only the bootstrap heading, ask the user for the project description before creating any real phases.
3. Read [`ARCHITECTURE.md`]({1}/doc/roadmap/ARCHITECTURE.md) when architecture, stack, boundaries, or deployment shape matter.
4. Read [`DECISIONS.md`]({1}/doc/roadmap/DECISIONS.md) when stable product or delivery rules matter.
5. Read [`QUALITY_GATES.md`]({1}/doc/roadmap/QUALITY_GATES.md) when phase closeout rules are needed.
6. Read [`TRACEABILITY.md`]({1}/doc/roadmap/TRACEABILITY.md) when mapping roadmap coverage back to the human brief.

## File Roles

- `current/`: the future home of the active phase after the real roadmap is derived.
- `longterm/`: the future home of queued phases after the real roadmap is derived.
- `archive/`: the future home of completed phases.
- `ARCHITECTURE.md`: durable architecture and system-shape reference inside the roadmap tree.
- `DECISIONS.md`: stable product, architecture, and delivery decisions.
- `QUALITY_GATES.md`: reusable closeout checks.
- `TRACEABILITY.md`: mapping from the human brief to roadmap phases.

## Maintenance Rules

- Do not invent real phases before `HUMAN_BRIEF.md` contains actual human-authored project content.
- Replace this bootstrap index after the first real roadmap is derived.
- Keep the user's text literal in `HUMAN_BRIEF.md`.
""".format(today, repo_root, human_brief_rel, current_status)


def render_architecture(today: str) -> str:
    return """# Architecture Reference

Last updated: {0}

## Product Overview

- Replace this bootstrap placeholder after the human brief is captured.

## Core Constraints

- Replace this bootstrap placeholder after the human brief is captured.

## System Shape

- Replace this bootstrap placeholder after the human brief is captured.

## Technology Stack

- Replace this bootstrap placeholder after the human brief is captured.

## Module Boundaries

- Replace this bootstrap placeholder after the human brief is captured.

## Deployment Contours

- Replace this bootstrap placeholder after the human brief is captured.
""".format(today)


def render_decisions(today: str) -> str:
    return """# Stable Decisions

Last updated: {0}

## Product Scope

- Replace this bootstrap placeholder after the human brief is captured.

## System Architecture

- Replace this bootstrap placeholder after the human brief is captured.

## Delivery Rules

- Keep `doc/HUMAN_BRIEF.md` literal and human-authored.
- Replace this bootstrap placeholder after the human brief is captured.
""".format(today)


def render_quality_gates(today: str) -> str:
    return """# Phase Quality Gates

Last updated: {0}

## Required Checks For Every Completed Phase

1. Replace this bootstrap placeholder after the human brief is captured.

## Project Commands

1. Replace this bootstrap placeholder after the human brief is captured.

## Recording Rules

- Summarize the check results in archived `00-phase.md` under `## Verification`.

## Skip Rules

- Record every skipped check together with the reason and residual risk.
""".format(today)


def render_traceability(today: str, repo_root: str, human_brief_rel: str) -> str:
    return """# Roadmap Traceability

Last updated: {0}
Source document: [`HUMAN_BRIEF.md`]({1}/{2})

## Coverage Rules

- Map roadmap phases back to the human brief.
- Do not invent roadmap coverage before the human brief exists.

## Phase Mapping

- Replace this bootstrap placeholder after the real roadmap is derived.

## Stakeholder Alignment Notes

- Replace this bootstrap placeholder after the real roadmap is derived.

## Roadmap-Only Refinements

- Replace this bootstrap placeholder after the real roadmap is derived.

## Divergences

- Replace this bootstrap placeholder after the real roadmap is derived.
""".format(today, repo_root, human_brief_rel)


def write_if_absent(path: Path, content: str) -> None:
    if path.exists():
        raise SystemExit("Path already exists: {0}".format(path))
    write_text(path, content)


def load_brief_text(args: argparse.Namespace) -> Optional[str]:
    if args.brief_text is not None and args.brief_stdin:
        raise SystemExit("Use either --brief-text or --brief-stdin, not both.")
    if args.brief_text is not None:
        return args.brief_text
    if args.brief_stdin:
        return sys.stdin.read()
    return None


def main() -> int:
    ensure_supported_python()
    parser = argparse.ArgumentParser(
        description="Initialize roadmap bootstrap files without inventing real phases."
    )
    parser.add_argument("--doc-root", default="doc", help="Documentation root directory")
    parser.add_argument(
        "--human-brief-path",
        dest="human_brief_path",
        default=None,
        help="Optional override for the human brief file path relative to the repository root",
    )
    parser.add_argument(
        "--brief-text",
        dest="brief_text",
        default=None,
        help="Literal human brief text to save verbatim",
    )
    parser.add_argument(
        "--brief-stdin",
        dest="brief_stdin",
        action="store_true",
        help="Read the literal human brief text from stdin",
    )
    args = parser.parse_args()

    repo_root = Path.cwd()
    doc_root = (repo_root / args.doc_root).resolve()
    roadmap_root = doc_root / "roadmap"
    human_brief_path = (
        (repo_root / args.human_brief_path).resolve()
        if args.human_brief_path
        else (doc_root / "HUMAN_BRIEF.md").resolve()
    )
    brief_text = load_brief_text(args)
    brief_captured = bool(brief_text and brief_text.strip())
    today = today_iso()
    repo_root_posix = repo_root.as_posix()

    doc_root.mkdir(parents=True, exist_ok=True)
    roadmap_root.mkdir(parents=True, exist_ok=True)
    human_brief_path.parent.mkdir(parents=True, exist_ok=True)
    (roadmap_root / "current").mkdir(parents=True, exist_ok=True)
    (roadmap_root / "longterm").mkdir(parents=True, exist_ok=True)
    (roadmap_root / "archive").mkdir(parents=True, exist_ok=True)

    human_brief_rel = human_brief_path.relative_to(repo_root).as_posix()

    write_if_absent(human_brief_path, render_human_brief(brief_text))
    write_if_absent(
        roadmap_root / "INDEX.md",
        render_index(today, repo_root_posix, human_brief_rel, brief_captured),
    )
    write_if_absent(roadmap_root / "ARCHITECTURE.md", render_architecture(today))
    write_if_absent(roadmap_root / "DECISIONS.md", render_decisions(today))
    write_if_absent(roadmap_root / "QUALITY_GATES.md", render_quality_gates(today))
    write_if_absent(
        roadmap_root / "TRACEABILITY.md",
        render_traceability(today, repo_root_posix, human_brief_rel),
    )

    print("Initialized roadmap bootstrap under {0}".format(roadmap_root))
    print("Human brief file: {0}".format(human_brief_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
