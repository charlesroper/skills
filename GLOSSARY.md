# Writing and workflow skills

A collection of modular agent skills that govern how autonomous agents write, edit, structure, and maintain prose, documentation, and project records.

## Language

**Surface**:
The medium and reading environment where a piece of writing lives (`Longform Prose`, `Technical Docs & READMEs`, `Web & Content Design`, or `UX & Microcopy`), which dictates whether a reader reads linearly, scans for tasks, or interacts with UI controls.
_Avoid_: Mode, genre, channel, document type

**Reader Job**:
The concrete question, decision, or task a reader brings to a piece of writing.
_Avoid_: User intent, target audience, goal

**Universal Core**:
The baseline Zinsser and anti-trope writing rules in `on-writing-well/SKILL.md` (humanity, unity, clutter removal, active verbs, concrete nouns, payload-first, and trope avoidance) that apply across every Surface before surface-specific layout and structural rules fire.
_Avoid_: Base rules, global defaults

**Concept Grounding**:
Ensuring every concept or domain term is either brought by the reader as an established prerequisite or explicitly introduced in an earlier block before a later sentence leans on it.
_Avoid_: Term definition, prerequisite check

**Bite, Snack, Meal**:
Layered content structure for screen foraging where the heading and opening line deliver the immediate answer (bite), scannable subheadings and lists provide key details (snack), and body sections hold full depth (meal).
_Avoid_: Progressive summary, three-tier layout

**STE-80**:
An 80% implementation of the ASD-STE100 Simplified Technical English standard for high-stress operational and machine-adjacent documentation that enforces strict syntax caps (20 words for instructions, 25 words for descriptions, one action per numbered step, active imperatives, banned `-ing` forms, and immediate `WARNING:` blocks) while permitting modern technical terms.
_Avoid_: Full ASD-STE100, simplified English, caveman mode

**Editorial Pipeline**:
The two-stage writing workflow where Stage 1 drafts and structures content (`on-writing-well`, `ste-80`, `project-narrative`, or `cbeams-git-commit-messages`) and Stage 2 applies the Sub-Editor Gate (`guardian-style-guide` and `tropes`).
_Avoid_: Writing chain, post-processing pass

**Sub-Editor Gate**:
Stage 2 of the Editorial Pipeline, which enforces house spelling, typography (such as spaced en-dashes ` – ` over em-dashes `—`), capitalisation, number formatting, and trope removal while preserving the draft's structure and argument.
_Avoid_: Linter pass, style filter
