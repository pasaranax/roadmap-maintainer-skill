# Roadmap Structure

## Required Directory Tree

```text
doc/
  HUMAN_BRIEF.md
  roadmap/
    INDEX.md
    ARCHITECTURE.md
    DECISIONS.md
    QUALITY_GATES.md
    TRACEABILITY.md
    current/
    longterm/
    archive/
```

During bootstrap, `current/`, `longterm/`, and `archive/` may be empty.

## Bootstrap Order

1. If `doc/HUMAN_BRIEF.md` is missing or still contains only the bootstrap heading, ask the user for the project description first.
2. Run `init_roadmap.py` only after that step, or run it with the user's literal text through `--brief-text` or `--brief-stdin`.
3. Do not invent real phases yet.
4. Derive the real roadmap only after `doc/HUMAN_BRIEF.md` contains real human content.

## Files Created By `init_roadmap.py`

- `doc/HUMAN_BRIEF.md`
- `doc/roadmap/INDEX.md`
- `doc/roadmap/ARCHITECTURE.md`
- `doc/roadmap/DECISIONS.md`
- `doc/roadmap/QUALITY_GATES.md`
- `doc/roadmap/TRACEABILITY.md`
- `doc/roadmap/current/`
- `doc/roadmap/longterm/`
- `doc/roadmap/archive/`

## `HUMAN_BRIEF.md` Rule

`HUMAN_BRIEF.md` must start with one heading that says the text is human-authored and the Agent must not edit it.

If the user already described the project, append that text verbatim under the heading.

## After Bootstrap

Replace the placeholders with:

- a real `INDEX.md`
- a real `ARCHITECTURE.md`
- a real `DECISIONS.md`
- a real `QUALITY_GATES.md`
- a real `TRACEABILITY.md`
- one active phase under `current/`
- future queued phases under `longterm/`

Use `prompts/init-roadmap.md` once while producing that first real architecture and roadmap.

Then add one short trigger rule to `AGENTS.md` when it exists, otherwise to `CLAUDE.md`. Prefer `AGENTS.md` when both exist.

## Phase File Skeleton

```markdown
# Phase N — Title

Last updated: YYYY-MM-DD
Status: active|blocked|queued|complete

## Objective

## Why This Phase Exists

## Exit Criteria

## Constraints

## Slice Queue

- [ ] [01-slice-slug.md](01-slice-slug.md)

## Progress Summary

## Phase Completion Summary
```

## Slice File Skeleton

```markdown
# Slice NN — Title

Last updated: YYYY-MM-DD
Phase: Phase N — Title
Status: pending|active|blocked|done
Commit: `Commit message`

## Goal

## Checklist

- [ ] Concrete completion condition

## Work Loop

1. Re-read `00-phase.md` and this slice.
2. Implement the smallest safe change for the next unchecked item.
3. Run focused verification immediately.
4. Fix the blocking defect first if verification fails.
5. Record concrete evidence and only then mark the item done.
6. Repeat until the checklist is complete, then create the commit.

## Verification Target

## Verification Notes

## Follow-On Notes
```

## Python Compatibility

- Prefer `python3`.
- Support Python 3.8+.
- Use only the standard library.
- If no compatible interpreter exists, install one only when the package-manager command is obvious and low-risk; otherwise ask the user to install Python 3.8+.
