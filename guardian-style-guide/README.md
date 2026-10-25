# Guardian Style Guide Skill

An agent skill and reference library for copy-editing text to *The Guardian and Observer Style Guide* while preserving your original voice, structure, and argument.

## Why use this skill

Standard language models often default to American English conventions or generic corporate phrasing. This skill directs agents to:
- **Enforce British English spelling:** Use `-ise`, `-our`, `-re`, and doubled `l` forms (`organise`, `colour`, `centre`, `travelled`).
- **Apply down-style capitalisation:** Lowercase `government`, `cabinet`, political party nouns (`Labour party`), and job titles (`prime minister`).
- **Format punctuation to house style:** Use spaced en-dashes (`–`) for parenthetical pauses, strip serial/Oxford commas in simple lists, and use double quotes with British nesting.
- **Default to neutral attribution:** Replace editorialising tags (`insisted`, `warned`, `admitted`) with neutral `said`.
- **Search unabridged references offline:** Check obscure proper nouns, diplomatic titles, and foreign placenames across all 26 letters without overflowing token limits.

## Skill structure

- `SKILL.md`: The skill definition, copy-editing workflow, and core house mechanics.
- `references/`: The unabridged style guide split into four volumes (`a-f`, `g-l`, `m-r`, `s-z`).
- `guardian_style_guide.py`: Python script to re-fetch and rebuild reference volumes from `theguardian.com`.
- `pyproject.toml`: Tool dependencies managed with `uv`.

## Install the skill

### In Antigravity workspaces
Copy this skill directory into your project's `.agents/skills/` folder:

```bash
cp -r path/to/skills/guardian-style-guide /path/to/project/.agents/skills/
```

Or clone just this skill using Git sparse checkout:

```bash
git clone --depth 1 --filter=blob:none --sparse https://github.com/charlesroper/skills.git .agents/skills/guardian-style-guide
cd .agents/skills/guardian-style-guide && git sparse-checkout set guardian-style-guide
```

### In other agent environments (Claude Code, Cursor, Codex)
Add this directory to your workspace and configure your agent to read `SKILL.md` when editing or reviewing copy.

## Sub-edit text with an agent

Prompt your agent to edit a draft:

> "Sub-edit this draft into Guardian style and provide a changelog of corrections."

The agent applies core house mechanics, consults `references/` for edge cases, and returns the revised copy followed by a bulleted changelog.

## Update reference data from the Guardian

To refresh the local reference files with the latest entries from the Guardian website:

1. Install [uv](https://docs.astral.sh/uv/) if you do not have it installed.
2. Run the update script to download all four volumes:

```bash
uv run guardian_style_guide.py
```

To test a single letter:

```bash
uv run guardian_style_guide.py --letters z
```

3. Run the offline parser verification suite:

```bash
uv run guardian_style_guide.py --selftest
```

## License

The skill definition and Python tooling are licensed under the MIT License. The style guide contents remain the intellectual property of Guardian News & Media Limited.
