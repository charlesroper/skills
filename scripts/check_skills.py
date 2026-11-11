#!/usr/bin/env python3
"""Repository skill validator and CI guardrail.

Verifies:
1. Frontmatter check: every skill directory has valid YAML frontmatter with
   `name` matching folder and non-empty `description` (optional boolean
   `disable-model-invocation`).
2. Markdown link check: every relative link resolves to an existing file/anchor.
3. README registration check: every skill directory is registered in root README.md.
4. Authored typography check: authored Markdown files (excluding upstream-synced
   reference volumes) contain 0 unspaced em-dashes, 0 curly quotes, and 0 Unicode arrows.
   Spaced en-dashes (` – `) are explicitly permitted.
"""

import os
import re
import sys
from pathlib import Path

FORBIDDEN_CHARS = {
    "—": "unspaced em-dash",
    "“": "curly quote",
    "”": "curly quote",
    "‘": "curly quote",
    "’": "curly quote",
    "→": "Unicode arrow",
    "←": "Unicode arrow",
}


LINK_PATTERN = re.compile(
    r"!?\[([^\]]*)\]\((?:<([^>]+)>|([^)\s]+)(?:\s+[\"'][^\"']*[\"'])?)\)"
)


def parse_frontmatter(content: str) -> tuple[dict[str, object] | None, str | None]:
    """Parse YAML frontmatter delimited by --- from the start of content."""
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, "Missing opening frontmatter delimiter '---'"

    end_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break

    if end_idx is None:
        return None, "Missing closing frontmatter delimiter '---'"

    fm_lines = lines[1:end_idx]
    data: dict[str, object] = {}
    current_key: str | None = None
    multiline_val: list[str] = []
    multiline_mode: str | None = None

    for line in fm_lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        if (line.startswith("  ") or line.startswith("\t")) and current_key:
            multiline_val.append(stripped)
            continue

        if current_key and multiline_mode:
            if multiline_mode in (">", ">-"):
                data[current_key] = " ".join(multiline_val).strip()
            elif multiline_mode in ("|", "|-"):
                data[current_key] = "\n".join(multiline_val).strip()
            else:
                data[current_key] = " ".join(multiline_val).strip()
            current_key = None
            multiline_val = []
            multiline_mode = None

        if ":" in line:
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip()
            if v in (">", ">-", "|", "|-"):
                current_key = k
                multiline_mode = v
                multiline_val = []
            else:
                if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
                    v = v[1:-1]
                elif ": " in v:
                    return None, f"Unquoted ': ' in frontmatter value for '{k}' causes YAML parse error"
                data[k] = v
                current_key = k
                multiline_mode = None

    if current_key and multiline_mode:
        if multiline_mode in (">", ">-"):
            data[current_key] = " ".join(multiline_val).strip()
        else:
            data[current_key] = "\n".join(multiline_val).strip()

    return data, None


def check_skill_frontmatter(skill_dir: Path) -> list[str]:
    """Validate YAML frontmatter in a skill's SKILL.md."""
    violations: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return [f"{skill_dir}: missing SKILL.md"]

    try:
        content = skill_md.read_text(encoding="utf-8")
    except Exception as exc:
        return [f"{skill_md}: failed to read file: {exc}"]

    data, err = parse_frontmatter(content)
    if err:
        return [f"{skill_md}: invalid frontmatter: {err}"]
    if data is None:
        return [f"{skill_md}: frontmatter could not be parsed"]

    # Name check
    name = data.get("name")
    if not name or not isinstance(name, str) or not name.strip():
        violations.append(f"{skill_md}: frontmatter missing non-empty 'name'")
    elif name.strip() != skill_dir.name:
        violations.append(
            f"{skill_md}: frontmatter 'name' '{name}' does not match directory name '{skill_dir.name}'"
        )

    # Description check
    desc = data.get("description")
    if not desc or not isinstance(desc, str) or not desc.strip():
        violations.append(f"{skill_md}: frontmatter missing non-empty 'description'")

    # Optional disable-model-invocation check
    if "disable-model-invocation" in data:
        val = data["disable-model-invocation"]
        if isinstance(val, bool):
            pass
        elif isinstance(val, str) and val.lower() in ("true", "false", "yes", "no"):
            pass
        else:
            violations.append(
                f"{skill_md}: frontmatter 'disable-model-invocation' must be a boolean, got '{val}'"
            )

    return violations


def extract_anchors(file_path: Path) -> set[str]:
    """Extract heading anchor slugs and explicit HTML anchors from a Markdown file."""
    if not file_path.is_file():
        return set()

    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception:
        return set()

    anchors: set[str] = set()
    slug_counts: dict[str, int] = {}

    for line in content.splitlines():
        # Match markdown headings
        match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if match:
            heading_text = match.group(2).strip()
            # Check for inline custom anchor like {#my-anchor}
            custom_match = re.search(r"\{#([^}]+)\}", heading_text)
            if custom_match:
                anchors.add(custom_match.group(1).lower())
                heading_text = re.sub(r"\{#[^}]+\}", "", heading_text).strip()

            # Strip markdown formatting
            cleaned = re.sub(r"[*_`]", "", heading_text)
            cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", cleaned)
            # Slugify: lowercase, remove non-alphanumeric/hyphen/space, replace whitespace with hyphen
            slug = cleaned.lower()
            slug = re.sub(r"[^\w\s-]", "", slug)
            slug = re.sub(r"[-\s]+", "-", slug).strip("-")

            if slug:
                if slug in slug_counts:
                    slug_counts[slug] += 1
                    anchors.add(f"{slug}-{slug_counts[slug]}")
                else:
                    slug_counts[slug] = 0
                    anchors.add(slug)

        # Match HTML anchors: <a name="..."> or <a id="..."> or general id="..."
        for html_match in re.finditer(r'<a\s+[^>]*(?:name|id)=["\']([^"\']+)["\']', line, re.IGNORECASE):
            anchors.add(html_match.group(1).lower())
        for id_match in re.finditer(r'\bid=["\']([^"\']+)["\']', line, re.IGNORECASE):
            anchors.add(id_match.group(1).lower())

    return anchors


def check_markdown_links(file_path: Path, repo_root: Path) -> list[str]:
    """Check that all relative Markdown links in file_path resolve to valid targets/anchors."""
    violations: list[str] = []
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as exc:
        return [f"{file_path}: failed to read file: {exc}"]

    lines = content.splitlines()
    in_code_block = False

    for line_idx, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # Strip inline code spans before extracting links
        line_clean = re.sub(r"`[^`\n]+`", "", line)

        # Match markdown links [text](target) and images ![text](target)
        for link_match in LINK_PATTERN.finditer(line_clean):
            raw_target = link_match.group(2) or link_match.group(3)
            if not raw_target:
                continue
            raw_target = raw_target.strip()

            # Ignore external protocols / schemes (http:, https:, mailto:, ftp:, etc.)
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", raw_target):
                continue
            # Ignore root-relative web paths
            if raw_target.startswith("/"):
                continue

            path_part, _, anchor = raw_target.partition("#")
            path_part = path_part.strip()
            anchor = anchor.strip()

            target_file: Path
            if not path_part:
                target_file = file_path
            else:
                target_file = (file_path.parent / path_part).resolve()
                if not target_file.exists():
                    rel_source = file_path.relative_to(repo_root)
                    violations.append(
                        f"{rel_source}:{line_idx}: broken relative link '{raw_target}' (target file '{path_part}' not found)"
                    )
                    continue

            if anchor and target_file.is_file():
                anchors = extract_anchors(target_file)
                if anchor.lower() not in anchors:
                    rel_source = file_path.relative_to(repo_root)
                    violations.append(
                        f"{rel_source}:{line_idx}: broken relative link '{raw_target}' (anchor '#{anchor}' not found in '{target_file.name}')"
                    )

    return violations


def is_exempt_from_typography(rel_posix_path: str) -> bool:
    """Check if file is an upstream-synced reference volume exempt from typography rules."""
    if rel_posix_path.endswith("references/tropes.md") or "/references/tropes.md" in rel_posix_path:
        return True
    if "references/guardian-style-guide-" in rel_posix_path:
        return True
    return False


def check_typography(file_path: Path, repo_root: Path) -> list[str]:
    """Validate authored typography rules in file_path."""
    rel_path = file_path.relative_to(repo_root).as_posix()
    if is_exempt_from_typography(rel_path):
        return []

    violations: list[str] = []
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as exc:
        return [f"{rel_path}: failed to read file: {exc}"]

    lines = content.splitlines()
    in_code_block = False

    for line_idx, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # Strip inline code spans
        prose_line = re.sub(r"`[^`\n]+`", "", line)

        for char, desc in FORBIDDEN_CHARS.items():
            if char in prose_line:
                violations.append(
                    f"{rel_path}:{line_idx}: contains forbidden {desc} '{char}'"
                )

    return violations


def check_readme_registration(repo_root: Path, skill_names: set[str]) -> list[str]:
    """Ensure every skill directory is registered in root README.md."""
    violations: list[str] = []
    readme_path = repo_root / "README.md"
    if not readme_path.is_file():
        return [f"{readme_path}: root README.md not found"]

    try:
        content = readme_path.read_text(encoding="utf-8")
    except Exception as exc:
        return [f"{readme_path}: failed to read README.md: {exc}"]

    # Look for skills section
    skills_section = content
    match = re.search(r"^##\s+Skills[^\n]*\n(.*?)(?=\n##|\Z)", content, flags=re.DOTALL | re.MULTILINE | re.IGNORECASE)
    if match:
        skills_section = match.group(1)

    for skill_name in sorted(skill_names):
        # Match skill name in backticks, quotes, brackets, or word boundaries
        pattern = rf"(?:^|[`'\"\[\s]|\b){re.escape(skill_name)}(?:[`'\"\]\s]|\b|$)"
        if not re.search(pattern, skills_section):
            violations.append(
                f"Skill '{skill_name}' is not registered in root README.md skills list"
            )

    # Check that skills listed in README also exist as directories with SKILL.md
    readme_skills = set(re.findall(r"^[*-]\s+`?([a-zA-Z0-9_-]+)`?:", skills_section, re.MULTILINE))
    for r_skill in sorted(readme_skills):
        skill_dir = repo_root / r_skill
        if not (skill_dir / "SKILL.md").is_file():
            violations.append(
                f"README lists skill '{r_skill}', but '{r_skill}/SKILL.md' does not exist"
            )

    return violations


def check_repository(repo_path: str | Path) -> list[str]:
    """Validate repository skills, links, registration, and typography.
    
    Returns a list of violation diagnostics (empty list if valid).
    """
    root = Path(repo_path).resolve()
    if not root.is_dir():
        return [f"Repository path '{repo_path}' is not a directory"]

    violations: list[str] = []

    # 1. Discover skill directories (top-level directories with SKILL.md)
    skill_names: set[str] = set()
    for item in root.iterdir():
        if item.is_dir() and not item.name.startswith("."):
            skill_md = item / "SKILL.md"
            if skill_md.is_file():
                skill_names.add(item.name)
                violations.extend(check_skill_frontmatter(item))

    # 2. Check README registration
    violations.extend(check_readme_registration(root, skill_names))

    # 3. Check relative links and typography across Markdown files
    for dirpath, dirnames, filenames in os.walk(root):
        # Exclude hidden directories like .git
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for filename in filenames:
            if filename.endswith(".md"):
                file_path = Path(dirpath) / filename
                violations.extend(check_markdown_links(file_path, root))
                violations.extend(check_typography(file_path, root))

    return violations


def main() -> int:
    """CLI entrypoint for checking repository skills."""
    repo_arg = sys.argv[1] if len(sys.argv) > 1 else None
    repo_path = Path(repo_arg).resolve() if repo_arg else Path(__file__).resolve().parent.parent

    violations = check_repository(repo_path)
    if violations:
        print(f"Validation failed with {len(violations)} violation(s):", file=sys.stderr)
        for v in violations:
            print(f"  - {v}", file=sys.stderr)
        return 1

    print("All skills and documentation are valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
