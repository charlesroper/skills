# AI Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Small collection of [agent skills](https://agentskills.io/) used to improve writing and workflow quality.

## Skills in this repo

- `on-writing-well`: Context-aware writing and editing across four Surfaces (`Longform Prose`, `Technical Docs & READMEs`, `Web & Content Design` and `UX & Microcopy`), grounded in William Zinsser's *On Writing Well* and modern UX/content design books, with a catalogue of AI writing tropes to avoid.
- `cbeams-git-commit-messages`: Commit message guidance based on Chris Beams'
  seven rules.
- `maintainable-css`: Apply Adam Silver's MaintainableCSS methodology to plan, refactor, and review CSS and markup.
- `guardian-style-guide`: Copy-edit, proofread or write text to adhere to the Guardian and Observer style guide while preserving the author's original voice, structure and argument.
- `project-narrative`: Write and maintain NARRATIVE.md, the evidence-linked story of a project for humans and agents.

## Structure

```text
skills/
  on-writing-well/
    SKILL.md
    update_tropes.py
    references/
      longform-prose.md
      technical-docs.md
      tropes.md
      ux-microcopy.md
      web-content-design.md
  cbeams-git-commit-messages/
    SKILL.md
  maintainable-css/
    SKILL.md
    references/
      maintainable-css-manual.md
  guardian-style-guide/
    SKILL.md
    references/
      guardian-style-guide-a-f.md
      guardian-style-guide-g-l.md
      guardian-style-guide-m-r.md
      guardian-style-guide-s-z.md
  project-narrative/
    SKILL.md
```

Each skill is defined in its own `SKILL.md`.
