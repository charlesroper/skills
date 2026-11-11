# Changelog

All notable changes to this repository are documented in this file.

## Unreleased

### Added

- `setup-writing-framework`: Add interactive scaffolding skill to configure
  the two-stage Editorial Pipeline in repository `AGENTS.md` or `CLAUDE.md`
  files, routing Stage 1 drafting (`on-writing-well`, `ste-80`,
  `project-narrative`, `cbeams-git-commit-messages`) and Stage 2 sub-editing
  (`guardian-style-guide`).

- `ste-80`: Add standalone skill for operational software documentation, runbooks,
  CLI specs, API guides and troubleshooting steps using an 80% implementation
  of ASD-STE100 (Simplified Technical English).
- `on-writing-well`: Add context-aware routing across four writing Surfaces with
  disclosed reference playbooks (`references/longform-prose.md`,
  `references/technical-docs.md`, `references/web-content-design.md` and
  `references/ux-microcopy.md`) blending William Zinsser's *On Writing Well* with
  *Content Design* (Sarah Winters), *Letting Go of the Words* (Janice Redish),
  *Strategic Writing for UX* (Torrey Podmajersky), *Writing Is Designing*
  (Michael J. Metts and Andy Welfle) and *Microcopy: The Complete Guide*
  (Kinneret Yifrah).
- `project-narrative`: Add skill for writing and maintaining evidence-linked
  project narratives (NARRATIVE.md) in human and agent-friendly blog post format.
- `on-writing-well`: Add the 49-pattern AI writing tropes catalogue from
  tropes.fyi as `references/tropes.md`, with a summary checklist in `SKILL.md`.
- `on-writing-well`: Add `update_tropes.py`, a standard-library script that
  reports upstream catalogue changes and refreshes the local copy on request.
  It runs on Windows, macOS and Linux.
- Workflows: Add scheduled weekly GitHub Action to sync Guardian reference
  volumes and open pull requests for upstream changes.
- Workflows: Add scheduled weekly GitHub Action to sync the tropes.fyi
  catalogue and open a pull request for upstream changes. A failed run opens a
  "Tropes sync failed" issue, unless one is already open.
- `guardian-style-guide`: Add Guardian and Observer style guide skill with four
  reference volumes and maintenance sync script.
- `maintainable-css`: Add skill and update `README.md` to include the new
  `maintainable-css` entry and repository structure diagram (see PR #2).

### Changed

- Repository instructions: Wire the two-stage Editorial Pipeline (`## Writing framework`)
  into `AGENTS.md`, routing Stage 1 drafting across `on-writing-well`, `ste-80`,
  `project-narrative`, and `cbeams-git-commit-messages` through the `guardian-style-guide`
  Stage 2 Sub-Editor Gate while preserving existing agent guidelines.

- `cbeams-git-commit-messages`: Structure into an ordered 5-step procedure with
  checkable completion criteria and deduplicate instructions, output formatting
  and quality checks into a unified reference checklist.
- `guardian-style-guide`: Document role in the Editorial Pipeline as the Stage 2
  Sub-Editor Gate, add checkable completion criteria to every copy-editing step,
  and clarify preservation of spaced en-dashes (` – `) over unspaced em-dashes
  (`—`).
- `on-writing-well`: Refactor `SKILL.md` using `writing-for-agents` principles
  (explicit 4-step procedure with completion criteria, context intake prompt when
  Surface or Reader Job is ambiguous, Universal Core Zinsser mechanics and
  progressive disclosure to `references/*.md`).
- `on-writing-well`: Replace unicode arrows in the examples with plain prose,
  matching the tropes guidance now included in the skill.
- `project-narrative`: Replace duplicated inline summaries of tropes and
  Guardian style rules in `## Style` with clean context pointers to
  `on-writing-well` and `guardian-style-guide` as single sources of truth.
