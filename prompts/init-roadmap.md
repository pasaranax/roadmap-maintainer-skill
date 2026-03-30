# Initialize Roadmap From Brief

Use this prompt once after roadmap bootstrap, after `doc/HUMAN_BRIEF.md` already exists with real user-authored content, and before the first real phase is created.

## Objective

Turn the literal human brief plus the current repository state into:

- a production-grade `doc/roadmap/ARCHITECTURE.md`
- synchronized roadmap support files
- the first real active phase under `doc/roadmap/current/`
- queued future phases under `doc/roadmap/longterm/`
- a short recommendation list of extra skills for the Agent, tools, and MCP integrations that would improve autonomous delivery

## Inputs

- `doc/HUMAN_BRIEF.md`
- repository codebase and configuration
- bootstrap files under `doc/roadmap/`

## Hard Rules

1. Treat `doc/HUMAN_BRIEF.md` as the literal source of truth. Do not edit it, paraphrase it, or silently normalize it.
2. Inspect the repository before making architectural claims.
3. Use search to learn the domain, platform constraints, relevant APIs, current best practices, and realistic implementation options.
4. When choosing technologies, languages, frameworks, or integrations, prefer official documentation and primary sources.
5. Do not invent certainty where the brief is incomplete. Encode unknowns as early discovery, validation, or spike phases and slices.
6. Keep the resulting roadmap detailed enough that `ARCHITECTURE.md` plus the phases can replace a separate design document.

## Research Requirements

1. Inspect the repository structure, stack, and existing implementation.
2. Search for domain facts that matter for the product idea:
   - domain platform constraints
   - data-source and integration limitations
   - integration surfaces and auth models
   - UI or browser-testing implications
   - deployment, cost, and observability constraints
3. Use the research to suggest strong approaches that fit the brief rather than only restating the brief.
4. Choose technologies and languages pragmatically:
   - favor tools that fit the repo if the existing choices are defensible
   - otherwise explain why a different stack or component is justified

## Architecture Expectations

Write `doc/roadmap/ARCHITECTURE.md` at professional design-doc depth. It should cover, when relevant:

- product shape and operational goals
- system context and major subsystems
- module boundaries and extension seams
- domain model and key entities
- data flow, ingestion, storage, scheduling, and realtime paths
- extension or plugin architecture when relevant
- safety, control, and failure-boundary architecture when relevant
- UI architecture and user-flow verification approach when relevant
- testing and verification strategy
- deployment topology and runtime environments
- secrets, security, cost, and observability considerations

Favor modern professional engineering practices:

- modular architecture with explicit boundaries
- clean interfaces and dependency direction
- OOP where it improves extensibility and clarity
- established design patterns where they reduce coupling or regression risk
- testable seams, replaceable adapters, and isolated side effects
- structures that can be expanded for a long time without rewriting unrelated code

Do not add pattern jargon for its own sake. Use patterns only when they make the architecture safer or easier to extend.

## Roadmap Expectations

Rewrite the bootstrap files so they become project-specific:

- `doc/roadmap/INDEX.md`
- `doc/roadmap/ARCHITECTURE.md`
- `doc/roadmap/DECISIONS.md`
- `doc/roadmap/QUALITY_GATES.md`
- `doc/roadmap/TRACEABILITY.md`

Then create the first real roadmap:

- exactly one active phase in `doc/roadmap/current/`
- future phases in `doc/roadmap/longterm/`
- at least one slice per phase
- one slice equals one task, one checklist, one verification loop, one commit boundary

Break development into phases based on the completeness of the brief:

- if the brief is complete, create direct execution phases
- if important facts are missing or risky, create explicit discovery or validation phases first
- keep phases chronologically ordered and technically coherent

## Tooling Recommendations

Think ahead about autonomous delivery. Produce a concise recommendation list for the user covering:

- extra skills worth installing for the Agent
- tools required for verification, browser work, or automation
- MCP servers that would materially improve implementation speed or confidence

Recommend only tools that are justified by the roadmap and repository. Do not auto-install them here; propose them to the user.

## Repository Trigger Rule

After the first real roadmap is created:

- if `AGENTS.md` exists in the repository root, write the trigger rule there
- otherwise, if `CLAUDE.md` exists in the repository root, write it there
- if both exist, prefer `AGENTS.md` and do not duplicate the rule
- do not create a new instruction file only for this purpose

Use this wording or an equivalent short rule:

- `For any user request that is more than a short answer or micro-edit and is substantial enough to deserve its own roadmap slice, use $roadmap-maintainer before implementation.`

## User-Facing Follow-Up

After the roadmap files are created, write a short user-facing summary in chat with:

- the roadmap structure as a tree that uses only headings or titles, without implementation details, checklists, or deep explanations
- the concrete next steps you and the user will take

Those next steps must be explicit and should include one or both of:

- requests to the user, such as installing recommended skills for the Agent, tools, or MCP integrations, or answering unresolved questions
- the heading-level content of the first slice in the current phase, so the user can see what work starts next

## Output Standard

The result should not read like vague brainstorming. It should read like an executable architecture package and implementation plan prepared by a strong senior engineer for long-term extension with low regression risk.
