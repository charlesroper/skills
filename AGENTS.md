# Agent guidelines

## Writing framework

Two-stage Editorial Pipeline for authored documentation, copy and commit messages:

### Stage 1: Drafting

Route drafting to the active specialist skill based on document type and reader job:
- `on-writing-well`: Human-centred prose, conceptual overviews, developer guides, README introductions, web content design and interface microcopy.
- `ste-80`: Operational software documentation, runbooks, deployment procedures, CLI flag and command specifications, API guides and troubleshooting steps.
- `project-narrative`: Evidence-linked project narrative and historical milestone posts (`NARRATIVE.md`).
- `cbeams-git-commit-messages`: Git commit subject lines and bodies.

### Stage 2: Sub-Editor Gate

Run all drafted prose, documentation and copy through `guardian-style-guide` before delivery:
- Enforce British English spelling (`-ise`, `-our`), down-style capitalisation and Guardian house style.
- Validate typography and punctuation: double quotation marks for speech, straight quotes in Markdown, zero unspaced em-dashes. Spaced en-dashes (` – `) are explicitly permitted for parenthetical pauses.
- Run trope check against AI writing clichés and brochure adjectives.
- Preserve authorial voice, structural design and verbatim quotations.

## Agent skills

### Issue tracker

Issues and specs live in GitHub Issues. See `docs/agents/issue-tracker.md`.

### Triage labels

Five canonical triage roles mapped 1:1 to GitHub labels. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context layout (`GLOSSARY.md` + `docs/adr/`). See `docs/agents/domain.md`.
