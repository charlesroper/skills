# Changelog

All notable changes to this repository are documented in this file.

## Unreleased

### Added

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

- `on-writing-well`: Replace unicode arrows in the examples with plain prose,
  matching the tropes guidance now included in the skill.
