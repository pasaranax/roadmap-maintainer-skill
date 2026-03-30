#!/usr/bin/env python3

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from roadmap_common import (
    PHASE_FILE_NAME,
    ensure_supported_python,
    find_phase_in_bucket,
    list_phase_dirs,
    resolve_roadmap_dirs,
    set_metadata_value,
    today_iso,
    write_text,
)


def main() -> int:
    ensure_supported_python()
    parser = argparse.ArgumentParser(description="Move a phase folder from longterm/ to current/.")
    parser.add_argument("--roadmap-root", default="doc/roadmap", help="Roadmap root directory")
    parser.add_argument("--phase", required=True, help="Phase folder name or phase number")
    args = parser.parse_args()

    dirs = resolve_roadmap_dirs(Path(args.roadmap_root))
    current_phases = list_phase_dirs(dirs.current)
    if current_phases:
        raise SystemExit(
            "`current/` is not empty. Archive or move the active phase before promoting another one."
        )

    phase_dir = find_phase_in_bucket(dirs.longterm, args.phase)
    target_dir = dirs.current / phase_dir.name
    shutil.move(str(phase_dir), str(target_dir))

    phase_file = target_dir / PHASE_FILE_NAME
    content = phase_file.read_text(encoding="utf-8")
    content = set_metadata_value(content, "Last updated", today_iso())
    content = set_metadata_value(content, "Status", "active")
    write_text(phase_file, content)

    print(target_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
