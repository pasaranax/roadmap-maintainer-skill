#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

from roadmap_common import ensure_supported_python, slugify, today_iso, write_text


def render_phase_file(
    phase_number: int,
    title: str,
    status: str,
    objective: str,
    why: str,
    exit_criteria: List[str],
    constraints: List[str],
    first_slice_name: str,
) -> str:
    exit_lines = exit_criteria or ["Replace with the phase exit criteria."]
    constraint_lines = constraints or ["Replace with the active constraints for this phase."]
    return f"""# Phase {phase_number} — {title}

Last updated: {today_iso()}
Status: {status}

## Objective

{objective}

## Why This Phase Exists

{why}

## Exit Criteria

{chr(10).join(f"- {item}" for item in exit_lines)}

## Constraints

{chr(10).join(f"- {item}" for item in constraint_lines)}

## Slice Queue

- [ ] [{first_slice_name}]({first_slice_name})

## Progress Summary

- Not started.

## Phase Completion Summary

- Fill this section only when the phase is archived.
"""


def render_slice_file(
    phase_number: int,
    phase_title: str,
    slice_number: int,
    slice_title: str,
    slice_goal: str,
    checklist: List[str],
) -> str:
    checklist_lines = checklist or ["Replace with the first concrete checklist item."]
    commit_title = slice_title
    return f"""# Slice {slice_number:02d} — {slice_title}

Last updated: {today_iso()}
Phase: Phase {phase_number} — {phase_title}
Status: pending
Commit: `{commit_title}`

## Goal

{slice_goal}

## Checklist

{chr(10).join(f"- [ ] {item}" for item in checklist_lines)}

## Work Loop

1. Re-read `00-phase.md` and this slice; keep scope fixed to unchecked checklist items.
2. Implement the smallest safe change that closes the next unchecked item.
3. Run focused verification immediately after the change.
4. If verification fails, fix the blocking defect first and rerun the same check.
5. Record concrete evidence under `## Verification Notes` and mark the item done only after the result is current.
6. Repeat until every checklist item is complete, then create the commit shown above.

## Verification Target

Replace with the concrete verification target for this slice.

## Verification Notes

- Pending.

## Follow-On Notes

- None.
"""


def main() -> int:
    ensure_supported_python()
    parser = argparse.ArgumentParser(description="Create a roadmap phase folder with its first slice.")
    parser.add_argument("--roadmap-root", default="doc/roadmap", help="Roadmap root directory")
    parser.add_argument("--bucket", choices=("current", "longterm"), default="longterm")
    parser.add_argument("--phase-number", type=int, required=True)
    parser.add_argument("--title", required=True, help="Phase title without the leading phase number")
    parser.add_argument("--slug", help="Optional folder slug override")
    parser.add_argument("--status", help="Optional status override")
    parser.add_argument("--objective", default="Replace with the phase objective.")
    parser.add_argument("--why", default="Replace with the reason this phase exists now.")
    parser.add_argument("--exit-criterion", action="append", default=[])
    parser.add_argument("--constraint", action="append", default=[])
    parser.add_argument("--first-slice-title", required=True)
    parser.add_argument("--first-slice-goal", default="Replace with the goal of the first slice.")
    parser.add_argument("--first-slice-checklist", action="append", default=[])
    args = parser.parse_args()

    roadmap_root = Path(args.roadmap_root).resolve()
    bucket_dir = roadmap_root / args.bucket
    if not bucket_dir.exists():
        raise SystemExit(f"Bucket directory not found: {bucket_dir}")

    status = args.status or ("active" if args.bucket == "current" else "queued")
    slug = args.slug or slugify(args.title)
    phase_dir = bucket_dir / f"phase-{args.phase_number:02d}-{slug}"
    if phase_dir.exists():
        raise SystemExit(f"Phase directory already exists: {phase_dir}")

    phase_dir.mkdir(parents=True, exist_ok=False)
    slice_number = 1
    slice_file_name = f"{slice_number:02d}-{slugify(args.first_slice_title)}.md"
    write_text(
        phase_dir / "00-phase.md",
        render_phase_file(
            phase_number=args.phase_number,
            title=args.title,
            status=status,
            objective=args.objective,
            why=args.why,
            exit_criteria=args.exit_criterion,
            constraints=args.constraint,
            first_slice_name=slice_file_name,
        ),
    )
    write_text(
        phase_dir / slice_file_name,
        render_slice_file(
            phase_number=args.phase_number,
            phase_title=args.title,
            slice_number=slice_number,
            slice_title=args.first_slice_title,
            slice_goal=args.first_slice_goal,
            checklist=args.first_slice_checklist,
        ),
    )
    print(phase_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
