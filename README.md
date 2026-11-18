# AI skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A collection of [agent skills](https://agentskills.io/) for writing, editing and workflow governance.

## Installation

### Global installation (all projects)

- Install all skills globally:

  ```bash
  npx skills add -g charlesroper/skills
  ```

- To install one skill, use `--skill`:

  ```bash
  npx skills add -g charlesroper/skills --skill ste-80
  ```

### Project installation (single repository)

From the target repository root:

1. Install the skills into the repository:

   ```bash
   npx skills add charlesroper/skills
   ```

2. Configure the writing framework in `AGENTS.md`:

   ```text
   /setup-writing-framework
   ```

## Skills in this repo

- `on-writing-well`: Context-aware writing and editing across four surfaces: longform prose, technical docs and READMEs, web and content design, and UX and microcopy. Grounded in William Zinsser's *On Writing Well* and modern content design practice, with a catalogue of AI writing tropes to avoid.
- `ste-80`: Write and edit operational software documentation, runbooks, CLI flag specifications, API guides and troubleshooting steps. Implements 80% of ASD-STE100 (Simplified Technical English).
- `cbeams-git-commit-messages`: Git commit message guidelines based on Chris Beams' seven rules.
- `maintainable-css`: Apply Adam Silver's MaintainableCSS methodology to plan, refactor and review CSS and markup.
- `guardian-style-guide`: Copy-edit, proofread or write text to adhere to the Guardian and Observer style guide while preserving authorial voice, structure and argument.
- `project-narrative`: Write and maintain `NARRATIVE.md`, the evidence-linked story of a project for humans and agents.
- `setup-writing-framework`: Scaffold the two-stage Editorial Pipeline in a project's `AGENTS.md` or `CLAUDE.md`. It routes Stage 1 drafting to `on-writing-well`, `ste-80`, `project-narrative` or `cbeams-git-commit-messages`, then runs `guardian-style-guide` for Stage 2 sub-editing.

## Structure

```text
skills/
  cbeams-git-commit-messages/
    SKILL.md
  guardian-style-guide/
    SKILL.md
    references/
      guardian-style-guide-a-f.md
      guardian-style-guide-g-l.md
      guardian-style-guide-m-r.md
      guardian-style-guide-s-z.md
  maintainable-css/
    SKILL.md
    references/
      maintainable-css-manual.md
  on-writing-well/
    SKILL.md
    update_tropes.py
    references/
      longform-prose.md
      technical-docs.md
      tropes.md
      ux-microcopy.md
      web-content-design.md
  project-narrative/
    SKILL.md
  setup-writing-framework/
    SKILL.md
  ste-80/
    SKILL.md
```
