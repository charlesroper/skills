"""Unit tests for repository skill validator (scripts/check_skills.py)."""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

# Add scripts directory to path for importing check_skills
SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

try:
    from check_skills import check_repository
except ImportError:
    check_repository = None


def make_valid_repo_tree(repo_dir: str) -> None:
    """Populate repo_dir with a minimal valid skills repository."""
    # Root README.md listing the skill
    readme = Path(repo_dir) / "README.md"
    readme.write_text(
        "# Repository Skills\n\n"
        "## Skills in this repo\n\n"
        "- `alpha-skill`: Description for alpha skill.\n",
        encoding="utf-8",
    )

    # Root AGENTS.md
    agents = Path(repo_dir) / "AGENTS.md"
    agents.write_text("# Agents Guidelines\n\nSee [Alpha Skill](alpha-skill/SKILL.md).\n", encoding="utf-8")

    # docs/adr/0001-test.md
    adr_dir = Path(repo_dir) / "docs" / "adr"
    adr_dir.mkdir(parents=True, exist_ok=True)
    adr = adr_dir / "0001-test.md"
    adr.write_text("# ADR 0001\n\nText using spaced en-dash – permitted.\n", encoding="utf-8")

    # Skill directory
    skill_dir = Path(repo_dir) / "alpha-skill"
    skill_dir.mkdir(parents=True, exist_ok=True)

    skill_md = skill_dir / "SKILL.md"
    skill_md.write_text(
        "---\n"
        "name: alpha-skill\n"
        "description: Description for alpha skill.\n"
        "disable-model-invocation: true\n"
        "---\n\n"
        "# Alpha Skill\n\n"
        "## Overview\n\n"
        "Description of alpha skill using – spaced en-dashes – and [relative link](references/guide.md#section-one).\n",
        encoding="utf-8",
    )

    # Reference directory with guide and exempt files
    ref_dir = skill_dir / "references"
    ref_dir.mkdir(parents=True, exist_ok=True)

    guide_md = ref_dir / "guide.md"
    guide_md.write_text(
        "# Reference Guide\n\n"
        "## Section One\n\n"
        "Details in section one. Code block permitted forbidden chars:\n\n"
        "```text\n"
        "Code block can have “curly quotes”, em—dash, and arrows → ←\n"
        "```\n\n"
        "Inline code `foo—bar` and `“quoted”` permitted.\n",
        encoding="utf-8",
    )

    # Upstream-synced exempt files
    tropes_md = ref_dir / "tropes.md"
    tropes_md.write_text(
        "# Tropes Catalogue\n\n"
        "This file has em-dashes — and curly quotes “hello” and arrows →.\n",
        encoding="utf-8",
    )

    guardian_ref = ref_dir / "guardian-style-guide-a-f.md"
    guardian_ref.write_text(
        "# Guardian Style Guide A-F\n\n"
        "Has em-dashes — and “curly quotes” and → arrows.\n",
        encoding="utf-8",
    )


class TestSkillValidator(unittest.TestCase):
    """Test suite for repository skill validator checks."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_path = self.temp_dir.name
        if check_repository is None:
            self.fail("check_skills module or check_repository function could not be imported")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_valid_repository_passes_with_zero_violations(self):
        """A properly formatted repository produces zero violations."""
        make_valid_repo_tree(self.repo_path)
        violations = check_repository(self.repo_path)
        self.assertEqual(violations, [])

    def test_frontmatter_missing(self):
        """SKILL.md without YAML frontmatter is flagged."""
        make_valid_repo_tree(self.repo_path)
        skill_md = Path(self.repo_path) / "alpha-skill" / "SKILL.md"
        skill_md.write_text("# Alpha Skill\n\nMissing frontmatter.\n", encoding="utf-8")

        violations = check_repository(self.repo_path)
        self.assertTrue(any("frontmatter" in v.lower() for v in violations), violations)

    def test_frontmatter_name_mismatch(self):
        """Frontmatter name not matching directory name is flagged."""
        make_valid_repo_tree(self.repo_path)
        skill_md = Path(self.repo_path) / "alpha-skill" / "SKILL.md"
        skill_md.write_text(
            "---\nname: beta-skill\ndescription: Test description.\n---\n\n# Alpha Skill\n",
            encoding="utf-8",
        )

        violations = check_repository(self.repo_path)
        self.assertTrue(any("name" in v.lower() and "match" in v.lower() for v in violations), violations)

    def test_frontmatter_missing_name(self):
        """Frontmatter without a name field is flagged."""
        make_valid_repo_tree(self.repo_path)
        skill_md = Path(self.repo_path) / "alpha-skill" / "SKILL.md"
        skill_md.write_text(
            "---\ndescription: Test description.\n---\n\n# Alpha Skill\n",
            encoding="utf-8",
        )

        violations = check_repository(self.repo_path)
        self.assertTrue(any("name" in v.lower() for v in violations), violations)

    def test_frontmatter_missing_or_empty_description(self):
        """Frontmatter with empty description is flagged."""
        make_valid_repo_tree(self.repo_path)
        skill_md = Path(self.repo_path) / "alpha-skill" / "SKILL.md"
        skill_md.write_text(
            "---\nname: alpha-skill\ndescription: ''\n---\n\n# Alpha Skill\n",
            encoding="utf-8",
        )

        violations = check_repository(self.repo_path)
        self.assertTrue(any("description" in v.lower() for v in violations), violations)

    def test_frontmatter_invalid_disable_model_invocation(self):
        """disable-model-invocation must be a boolean when present."""
        make_valid_repo_tree(self.repo_path)
        skill_md = Path(self.repo_path) / "alpha-skill" / "SKILL.md"
        skill_md.write_text(
            "---\n"
            "name: alpha-skill\n"
            "description: Valid description.\n"
            "disable-model-invocation: maybe\n"
            "---\n\n# Alpha Skill\n",
            encoding="utf-8",
        )

        violations = check_repository(self.repo_path)
        self.assertTrue(
            any("disable-model-invocation" in v.lower() and "boolean" in v.lower() for v in violations),
            violations,
        )

    def test_frontmatter_valid_boolean_disable_model_invocation(self):
        """disable-model-invocation with boolean true/false is valid."""
        make_valid_repo_tree(self.repo_path)
        skill_md = Path(self.repo_path) / "alpha-skill" / "SKILL.md"
        skill_md.write_text(
            "---\n"
            "name: alpha-skill\n"
            "description: Valid description.\n"
            "disable-model-invocation: false\n"
            "---\n\n# Alpha Skill\n",
            encoding="utf-8",
        )

        violations = check_repository(self.repo_path)
        self.assertEqual(violations, [])

    def test_relative_link_missing_target_file(self):
        """Relative link to nonexistent target file is flagged."""
        make_valid_repo_tree(self.repo_path)
        skill_md = Path(self.repo_path) / "alpha-skill" / "SKILL.md"
        skill_md.write_text(
            "---\n"
            "name: alpha-skill\n"
            "description: Valid description.\n"
            "---\n\n"
            "# Alpha Skill\n\n"
            "Link to [nonexistent file](references/missing.md).\n",
            encoding="utf-8",
        )

        violations = check_repository(self.repo_path)
        self.assertTrue(any("missing.md" in v for v in violations), violations)

    def test_relative_link_missing_anchor(self):
        """Relative link with nonexistent anchor in existing target file is flagged."""
        make_valid_repo_tree(self.repo_path)
        skill_md = Path(self.repo_path) / "alpha-skill" / "SKILL.md"
        skill_md.write_text(
            "---\n"
            "name: alpha-skill\n"
            "description: Valid description.\n"
            "---\n\n"
            "# Alpha Skill\n\n"
            "Link to [missing anchor](references/guide.md#nonexistent-heading).\n",
            encoding="utf-8",
        )

        violations = check_repository(self.repo_path)
        self.assertTrue(any("nonexistent-heading" in v for v in violations), violations)

    def test_relative_link_same_file_anchor(self):
        """Relative link to anchor within the same file is validated."""
        make_valid_repo_tree(self.repo_path)
        skill_md = Path(self.repo_path) / "alpha-skill" / "SKILL.md"
        skill_md.write_text(
            "---\n"
            "name: alpha-skill\n"
            "description: Valid description.\n"
            "---\n\n"
            "# Alpha Skill\n\n"
            "See [Details](#detailed-section).\n\n"
            "## Detailed Section\n\n"
            "Content here.\n",
            encoding="utf-8",
        )

        violations = check_repository(self.repo_path)
        self.assertEqual(violations, [])

    def test_relative_link_ignores_external_and_root_relative(self):
        """External links and root-relative web URLs are ignored."""
        make_valid_repo_tree(self.repo_path)
        skill_md = Path(self.repo_path) / "alpha-skill" / "SKILL.md"
        skill_md.write_text(
            "---\n"
            "name: alpha-skill\n"
            "description: Valid description.\n"
            "---\n\n"
            "# Alpha Skill\n\n"
            "External: [Google](https://google.com), [Mail](mailto:user@example.com)\n"
            "Root-relative: [Billing Settings](/settings/billing)\n",
            encoding="utf-8",
        )

        violations = check_repository(self.repo_path)
        self.assertEqual(violations, [])

    def test_readme_unregistered_skill(self):
        """Skill directory not listed in root README.md is flagged."""
        make_valid_repo_tree(self.repo_path)
        # Add a second skill directory not in README
        beta_dir = Path(self.repo_path) / "beta-skill"
        beta_dir.mkdir(parents=True, exist_ok=True)
        (beta_dir / "SKILL.md").write_text(
            "---\nname: beta-skill\ndescription: Beta skill description.\n---\n# Beta Skill\n",
            encoding="utf-8",
        )

        violations = check_repository(self.repo_path)
        self.assertTrue(any("beta-skill" in v and "README.md" in v for v in violations), violations)

    def test_readme_unquoted_skill_matches(self):
        """Unquoted skill names in README.md match correctly without regex boundary errors."""
        make_valid_repo_tree(self.repo_path)
        readme = Path(self.repo_path) / "README.md"
        readme.write_text(
            "# Repository Skills\n\n"
            "## Skills in this repo\n\n"
            "- alpha-skill: Description without backticks.\n",
            encoding="utf-8",
        )

        violations = check_repository(self.repo_path)
        self.assertEqual(violations, [])

    def test_readme_lists_missing_skill_dir_flagged(self):
        """README listing a skill whose directory/SKILL.md does not exist is flagged."""
        make_valid_repo_tree(self.repo_path)
        readme = Path(self.repo_path) / "README.md"
        readme.write_text(
            "# Repository Skills\n\n"
            "## Skills in this repo\n\n"
            "- `alpha-skill`: Description for alpha skill.\n"
            "- `ghost-skill`: Description for non-existent skill.\n",
            encoding="utf-8",
        )

        violations = check_repository(self.repo_path)
        self.assertTrue(any("ghost-skill" in v for v in violations), violations)

    def test_typography_unspaced_em_dash_in_prose(self):
        """Authored markdown containing unspaced em-dash in prose is flagged."""
        make_valid_repo_tree(self.repo_path)
        skill_md = Path(self.repo_path) / "alpha-skill" / "SKILL.md"
        skill_md.write_text(
            "---\n"
            "name: alpha-skill\n"
            "description: Valid description.\n"
            "---\n\n"
            "# Alpha Skill\n\n"
            "This sentence contains an unspaced—em-dash in prose.\n",
            encoding="utf-8",
        )

        violations = check_repository(self.repo_path)
        self.assertTrue(any("em-dash" in v.lower() for v in violations), violations)

    def test_typography_curly_quotes_in_prose(self):
        """Authored markdown containing curly quotes in prose is flagged."""
        make_valid_repo_tree(self.repo_path)
        skill_md = Path(self.repo_path) / "alpha-skill" / "SKILL.md"
        skill_md.write_text(
            "---\n"
            "name: alpha-skill\n"
            "description: Valid description.\n"
            "---\n\n"
            "# Alpha Skill\n\n"
            "This sentence has “double curly quotes” and ‘single curly quotes’.\n",
            encoding="utf-8",
        )

        violations = check_repository(self.repo_path)
        self.assertTrue(any("curly quote" in v.lower() for v in violations), violations)

    def test_typography_unicode_arrows_in_prose(self):
        """Authored markdown containing Unicode arrows in prose is flagged."""
        make_valid_repo_tree(self.repo_path)
        skill_md = Path(self.repo_path) / "alpha-skill" / "SKILL.md"
        skill_md.write_text(
            "---\n"
            "name: alpha-skill\n"
            "description: Valid description.\n"
            "---\n\n"
            "# Alpha Skill\n\n"
            "From here → to there and back ←.\n",
            encoding="utf-8",
        )

        violations = check_repository(self.repo_path)
        self.assertTrue(any("arrow" in v.lower() for v in violations), violations)

    def test_typography_spaced_en_dash_and_number_ranges_allowed(self):
        """Spaced en-dashes and number ranges with en-dashes are permitted."""
        make_valid_repo_tree(self.repo_path)
        skill_md = Path(self.repo_path) / "alpha-skill" / "SKILL.md"
        skill_md.write_text(
            "---\n"
            "name: alpha-skill\n"
            "description: Valid description.\n"
            "---\n\n"
            "# Alpha Skill\n\n"
            "Spaced en-dash – valid pause – and number range 10–20 are allowed.\n",
            encoding="utf-8",
        )

        violations = check_repository(self.repo_path)
        self.assertEqual(violations, [])

    def test_typography_exemptions_for_upstream_reference_volumes(self):
        """Upstream-synced reference volumes are exempt from typography rules."""
        make_valid_repo_tree(self.repo_path)
        tropes = Path(self.repo_path) / "alpha-skill" / "references" / "tropes.md"
        tropes.write_text(
            "Tropes catalogue with — em-dash, “quotes”, and → arrow.\n",
            encoding="utf-8",
        )
        guardian = Path(self.repo_path) / "alpha-skill" / "references" / "guardian-style-guide-m-r.md"
        guardian.write_text(
            "Guardian volume with — em-dash, “quotes”, and → arrow.\n",
            encoding="utf-8",
        )

        violations = check_repository(self.repo_path)
        self.assertEqual(violations, [])

    def test_frontmatter_unquoted_colon_flagged(self):
        """Unquoted colon inside frontmatter scalar is flagged as syntax hazard."""
        make_valid_repo_tree(self.repo_path)
        skill_md = Path(self.repo_path) / "alpha-skill" / "SKILL.md"
        skill_md.write_text(
            "---\n"
            "name: alpha-skill\n"
            "description: Write text across: Key1 and Key2 without quotes.\n"
            "---\n\n"
            "# Alpha Skill\n",
            encoding="utf-8",
        )
        violations = check_repository(self.repo_path)
        self.assertTrue(any("Unquoted ': '" in v for v in violations), violations)

    def test_cli_execution_exit_codes(self):
        """CLI returns exit code 0 on valid repository and 1 on invalid repository."""
        check_script = SCRIPTS_DIR / "check_skills.py"
        make_valid_repo_tree(self.repo_path)

        # Valid repository run
        result_valid = subprocess.run(
            [sys.executable, str(check_script), self.repo_path],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result_valid.returncode, 0, result_valid.stderr)

        # Invalid repository run (break link)
        (Path(self.repo_path) / "alpha-skill" / "SKILL.md").write_text(
            "---\nname: alpha-skill\ndescription: Test\n---\n\n[Broken](nonexistent.md)\n",
            encoding="utf-8",
        )
        result_invalid = subprocess.run(
            [sys.executable, str(check_script), self.repo_path],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result_invalid.returncode, 1)
        self.assertIn("nonexistent.md", result_invalid.stdout + result_invalid.stderr)


if __name__ == "__main__":
    unittest.main()
