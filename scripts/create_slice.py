#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

from roadmap_common import (
    PHASE_FILE_NAME,
    ensure_supported_python,
    ensure_phase_dir,
    next_slice_number,
    parse_heading_title,
    slugify,
    today_iso,
    write_text,
)


def render_slice_file(
    phase_title: str,
    slice_number: int,
    slice_title: str,
    status: str,
    goal: str,
    checklist: List[str],
    verification_target: str,
) -> str:
    checklist_lines = checklist or ["Replace with a concrete checklist item."]
    commit_title = slice_title
    return f"""# Slice {slice_number:02d} — {slice_title}

Last updated: {today_iso()}
Phase: {phase_title}
Status: {status}
Commit: `{commit_title}`

## Goal

{goal}

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

{verification_target}

## Verification Notes

- Pending.

## Follow-On Notes

- None.
"""


def main() -> int:
    ensure_supported_python()
    parser = argparse.ArgumentParser(description="Create the next ordered slice file inside a phase folder.")
    parser.add_argument("--phase-dir", required=True, help="Path to the phase directory")
    parser.add_argument("--title", required=True, help="Slice title")
    parser.add_argument("--goal", default="Replace with the slice goal.")
    parser.add_argument("--status", default="pending", choices=("pending", "active", "blocked", "done"))
    parser.add_argument("--checklist", action="append", default=[])
    parser.add_argument(
        "--verification-target",
        default="Replace with the concrete verification target for this slice.",
    )
    args = parser.parse_args()

    phase_dir = Path(args.phase_dir).resolve()
    ensure_phase_dir(phase_dir)
    phase_title = parse_heading_title(phase_dir / PHASE_FILE_NAME)
    slice_number = next_slice_number(phase_dir)
    slice_file = phase_dir / f"{slice_number:02d}-{slugify(args.title)}.md"
    if slice_file.exists():
        raise SystemExit(f"Slice file already exists: {slice_file}")

    write_text(
        slice_file,
        render_slice_file(
            phase_title=phase_title,
            slice_number=slice_number,
            slice_title=args.title,
            status=args.status,
            goal=args.goal,
            checklist=args.checklist,
            verification_target=args.verification_target,
        ),
    )
    print(slice_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
