---
name: cbeams-git-commit-messages
description: Write clear, consistent Git commit messages following Chris Beams' seven rules.
version: 1.0.0
tags:
  - git
  - commits
  - writing
  - conventions
---

# Purpose

Help the user write, revise, or review Git commit messages that are easy to scan, consistent across a repo, and informative in history.

# When to use

Use this skill whenever the user:
- asks for a commit message,
- pastes a diff / summary and asks what to commit,
- asks you to improve a commit message,
- asks you to review whether a commit message is "good".

# Instructions

When producing a commit message:

1) Subject line rules
- Output a single subject line first.
- Use the imperative mood (a command) - e.g. "Add", "Fix", "Refactor", "Remove", "Update".
- Capitalise the first character.
- Do not end with a full stop.
- Aim for 50 characters or fewer.
- Treat 72 characters as a hard ceiling - if it will exceed 72, rewrite.
- Only use ASCII characters in the subject and body.

2) Body rules
- Only include a body if it adds value.
- Separate subject and body with a single blank line.
- Wrap body lines at 72 characters.
- Explain what changed and why it changed.
- Avoid explaining how it changed (the diff already shows how).
- Use short paragraphs separated by blank lines when there are multiple ideas.

3) Optional footer
- If the user provides an issue / ticket reference, include it at the end as a footer
  line (or lines), after a blank line.
- Prefer forms like:
  - "Refs: #123"
  - "Resolves: #123"
  - "Fixes: #123"
- Do not invent issue references.

# Output format

Always output:
- The subject line on the first line.
- Then the body (if any), starting after one blank line.
- No surrounding quotation marks.
- No Markdown formatting.

If the user provides insufficient context (no summary of changes), ask for:
- a one-two sentence summary of what changed, and why,
or
- the diff / list of files changed.

# Quality checks (do before finalising)

- Subject <= 50 characters where possible; never > 72.
- Subject is imperative, capitalised, and has no trailing full stop.
- If there is a body: wrapped at 72 characters, explains what + why, not how.
