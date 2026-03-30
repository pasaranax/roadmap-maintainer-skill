---
name: roadmap-maintainer
description: Use for any non-trivial user request that deserves its own roadmap slice: feature work, bug fixes, refactors, investigations, integrations, migrations, or other multi-step tasks. Also use it to bootstrap or maintain `doc/roadmap/`, capture `doc/HUMAN_BRIEF.md`, derive the first roadmap, and manage phase and slice files. Skip only for short answers and micro-edits.
---

# Roadmap Maintainer

Use the roadmap as the single Agent-facing operating system for delivery. Keep the human brief literal in `doc/HUMAN_BRIEF.md`, keep durable architecture inside `doc/roadmap/ARCHITECTURE.md`, and execute work through folder-based phases plus one-task slice files.

## Python Prerequisite

- Prefer `python3`. Fall back to `python` only if it points to Python 3.8+.
- The bundled scripts use only the standard library and target Python 3.8+.
- If no compatible Python interpreter is available, first try an obvious local package-manager install only when the command is clear and low-risk for that machine. Otherwise ask the user to install Python 3.8+ and stop there.

## Bootstrap Order

When the user asks to create a roadmap, use this order strictly:

1. If `doc/HUMAN_BRIEF.md` does not exist, or exists but still contains only the bootstrap heading, ask the user for the project description first.
2. After the user provides the brief, run:
   - `python3 .codex/skills/roadmap-maintainer/scripts/init_roadmap.py --brief-stdin`
   - or `python3 .codex/skills/roadmap-maintainer/scripts/init_roadmap.py --brief-text "..."`
3. Save the user's brief into `doc/HUMAN_BRIEF.md` verbatim. Do not paraphrase, reorganize, or silently expand it.
4. Only after `doc/HUMAN_BRIEF.md` is present, inspect the repository and derive the first real roadmap from it.
5. Do not invent real project phases before the human brief exists.

## Repo Trigger Rule

After roadmap initialization is complete:

- If the repository root contains `AGENTS.md`, add a short trigger rule there.
- Otherwise, if the repository root contains `CLAUDE.md`, add the rule there.
- If both files exist, prefer `AGENTS.md` and do not duplicate the rule.
- Do not create a new instruction file only for this purpose.
- Use this wording or an equivalent short rule:
  - `For any user request that is more than a short answer or micro-edit and is substantial enough to deserve its own roadmap slice, use $roadmap-maintainer before implementation.`

## What `init_roadmap.py` Creates

`init_roadmap.py` creates only the bootstrap scaffold described in `references/roadmap-structure.md`.

It must not invent real implementation phases by itself.

## Default Read Set

For normal implementation work, read only:

1. `doc/HUMAN_BRIEF.md`
2. `doc/roadmap/INDEX.md`
3. the active phase file `doc/roadmap/current/<phase>/00-phase.md`
4. the first unfinished slice file in that phase

Read `doc/roadmap/ARCHITECTURE.md`, `DECISIONS.md`, `QUALITY_GATES.md`, `TRACEABILITY.md`, and narrow support files only when the current task needs them.

## File Roles

- `doc/HUMAN_BRIEF.md`: literal human-authored project brief, or literal user text saved by the Agent during roadmap bootstrap. Do not paraphrase it.
- `doc/roadmap/INDEX.md`: roadmap entry point and minimal navigation.
- `doc/roadmap/ARCHITECTURE.md`: durable architecture, stack, system shape, and deployment reference.
- `doc/roadmap/DECISIONS.md`: stable scope, architecture, and delivery rules that survive phase transitions.
- `doc/roadmap/QUALITY_GATES.md`: reusable verification rules for completed phases.
- `doc/roadmap/TRACEABILITY.md`: mapping from the human brief to roadmap phases, plus justified splits and divergences.
- `doc/roadmap/current/`: exactly one active phase directory after the real roadmap is derived.
- `doc/roadmap/longterm/`: future queued phase directories.
- `doc/roadmap/archive/`: completed phase directories.
- Narrow support files for stable topic-specific roadmap references.

## Derive The First Real Roadmap

After `doc/HUMAN_BRIEF.md` exists:

1. Inspect the repository.
2. Load and follow `prompts/init-roadmap.md` once.
3. Rewrite the bootstrap placeholders in:
   - `INDEX.md`
   - `ARCHITECTURE.md`
   - `DECISIONS.md`
   - `QUALITY_GATES.md`
   - `TRACEABILITY.md`
4. Create the first real active phase under `current/`.
5. Create future queued phases under `longterm/`.
6. Make the roadmap detailed enough that `ARCHITECTURE.md` plus the phases can replace a separate design document.

## Phase And Slice Rules

- Keep exactly one active phase folder in `current/` after the real roadmap is derived.
- Keep every phase folder ordered and self-contained:
  - `00-phase.md`
  - `01-...md`
  - `02-...md`
- Keep `00-phase.md` compact. It should hold only phase-level context:
  - objective
  - why the phase exists
  - exit criteria
  - constraints
  - slice queue
  - short progress summary
- Keep execution detail in slice files, not in the phase file.
- Keep every slice equal to one task, one checklist, one focused verification loop, and one commit boundary.

## Slice Execution Loop

For the active slice:

1. Re-read `00-phase.md` and the slice file.
2. Take the next unchecked checklist item.
3. Implement the smallest safe change that closes that item.
4. Run focused verification immediately.
5. If verification fails, fix the blocking defect first and rerun the same check.
6. Record concrete evidence in `## Verification Notes`.
7. Mark the checklist item done only after current evidence exists.
8. Repeat until every checklist item is done.
9. Create the slice commit immediately after the slice is fully complete.

## Transfer Rules

- Keep stakeholder intent in `doc/HUMAN_BRIEF.md`; do not duplicate it into roadmap files.
- Keep active work in `current/`.
- Keep future work in `longterm/`.
- Keep finished work in `archive/`.
- Move stable cross-phase rules into `DECISIONS.md`.
- Move durable system design into `ARCHITECTURE.md`.
- Move reusable closeout rules into `QUALITY_GATES.md`.
- Move requirement-to-phase mapping into `TRACEABILITY.md`.
- When a future phase becomes active, move its folder from `longterm/` to `current/`.
- When a phase completes, summarize the phase at a high level in archived `00-phase.md`, record the quality-gate results there, and then archive the whole phase folder.

## Scripts

- Initialize roadmap bootstrap files:
  - `python3 .codex/skills/roadmap-maintainer/scripts/init_roadmap.py`
- Initialize bootstrap and save the user brief literally:
  - `python3 .codex/skills/roadmap-maintainer/scripts/init_roadmap.py --brief-stdin`
  - `python3 .codex/skills/roadmap-maintainer/scripts/init_roadmap.py --brief-text "..."`
- Create a new phase folder with its first slice:
  - `python3 .codex/skills/roadmap-maintainer/scripts/create_phase.py --roadmap-root doc/roadmap --bucket longterm --phase-number 11 --title "Example Phase Title" --first-slice-title "Example first slice task"`
- Create the next ordered slice file:
  - `python3 .codex/skills/roadmap-maintainer/scripts/create_slice.py --phase-dir doc/roadmap/current/phase-11-example-phase-title --title "Example slice title"`
- Promote a queued phase:
  - `python3 .codex/skills/roadmap-maintainer/scripts/promote_phase.py --roadmap-root doc/roadmap --phase phase-12-example-queued-phase`
- Archive the active phase:
  - `python3 .codex/skills/roadmap-maintainer/scripts/archive_phase.py --roadmap-root doc/roadmap`

## Enforcement Rules

- Do not create parallel planning trees such as `.planning/`, `PLAN.md`, or `doc/ROADMAP.md`.
- Do not invent real phases before `doc/HUMAN_BRIEF.md` exists with actual human content.
- Do not leave more than one active phase under `current/` after bootstrap is replaced.
- Do not put active execution notes into `longterm/`.
- Do not archive by copy-pasting summaries while leaving the active phase in place. Move the whole phase folder.
- Do not paraphrase `doc/HUMAN_BRIEF.md`.
- Keep roadmap support files synchronized when roadmap structure or status changes.

## Reference

- Read `references/roadmap-structure.md` for exact bootstrap skeletons and support-file roles.
- Read `prompts/init-roadmap.md` only when turning the captured brief into the first real architecture and roadmap.
