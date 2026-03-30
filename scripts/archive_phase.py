#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from roadmap_common import (
    PHASE_FILE_NAME,
    active_phase_dir,
    ensure_supported_python,
    set_metadata_value,
    today_iso,
    write_text,
)


def main() -> int:
    ensure_supported_python()
    parser = argparse.ArgumentParser(description="Archive the current phase folder into archive/.")
    parser.add_argument("--roadmap-root", default="doc/roadmap", help="Roadmap root directory")
    parser.add_argument("--date", default=today_iso(), help="Archive date in YYYY-MM-DD format")
    args = parser.parse_args()

    roadmap_root = Path(args.roadmap_root).resolve()
    current_phase = active_phase_dir(roadmap_root)
    archive_dir = roadmap_root / "archive" / f"{args.date}-{current_phase.name}"
    if archive_dir.exists():
        raise SystemExit(f"Archive directory already exists: {archive_dir}")

    shutil.move(str(current_phase), str(archive_dir))
    phase_file = archive_dir / PHASE_FILE_NAME
    content = phase_file.read_text(encoding="utf-8")
    content = set_metadata_value(content, "Last updated", args.date)
    content = set_metadata_value(content, "Completed", args.date, after_key="Last updated")
    content = set_metadata_value(content, "Status", "complete")
    write_text(phase_file, content)

    print(archive_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
