"""Automated tests exercising the Writing Framework across stages and surfaces."""

import re
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EXERCISE_DIR = Path(__file__).resolve().parent / "framework_exercise"


class TestWritingFrameworkExercise(unittest.TestCase):
    """Exercise and verify Stage 1 and Stage 2 writing framework outputs."""

    def test_ste80_runbook_sentence_ceilings_and_warnings(self):
        """Verify STE-80 runbook adheres to 20-word step and 25-word description ceilings."""
        runbook = EXERCISE_DIR / "sample_runbook_ste80.md"
        self.assertTrue(runbook.is_file(), f"Missing {runbook}")

        content = runbook.read_text(encoding="utf-8")
        lines = content.splitlines()

        in_code_block = False
        step_lines: list[str] = []
        prose_lines: list[str] = []
        warning_found = False

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block or not stripped:
                continue

            if stripped.startswith("WARNING:"):
                warning_found = True
                self.assertIn("before you promote", stripped)
                continue

            # Numbered step: 1. Do action
            step_match = re.match(r"^\d+\.\s+(.+)$", stripped)
            if step_match:
                step_lines.append(step_match.group(1))
            elif not stripped.startswith("#"):
                prose_lines.append(stripped)

        self.assertTrue(warning_found, "STE-80 runbook must contain a WARNING: block")
        self.assertGreater(len(step_lines), 0, "STE-80 runbook must contain numbered steps")

        # Check procedural step ceiling (<= 20 words per sentence) and no ambient filler
        for step in step_lines:
            word_count = len(step.split())
            self.assertLessEqual(
                word_count,
                20,
                f"STE-80 step exceeds 20 words ({word_count} words): '{step}'",
            )
            self.assertFalse(
                step.lower().startswith(("open a terminal", "press enter")),
                f"STE-80 step contains ambient operator filler: '{step}'",
            )

        # Verify ste-80/SKILL.md encodes sequences-vs-alternatives and precondition rules
        ste_skill = (REPO_ROOT / "ste-80" / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Numbers for sequences, bullets for alternatives", ste_skill)
        self.assertIn("Never number alternatives or single-action procedures", ste_skill)

        # Check descriptive prose ceiling (<= 25 words per sentence)
        for prose in prose_lines:
            for sentence in re.split(r"[.!?]+", prose):
                sentence = sentence.strip()
                if sentence:
                    word_count = len(sentence.split())
                    self.assertLessEqual(
                        word_count,
                        25,
                        f"STE-80 descriptive sentence exceeds 25 words ({word_count} words): '{sentence}'",
                    )

    def test_on_writing_well_technical_docs_surface_structure(self):
        """Verify Technical Docs sample follows Why -> What -> How and payload-first lead."""
        guide = EXERCISE_DIR / "sample_guide_on_writing_well.md"
        content = guide.read_text(encoding="utf-8")

        # Sentence one states what the tool is and what it does
        first_content_line = next(
            line.strip() for line in content.splitlines() if line.strip() and not line.startswith("#")
        )
        self.assertTrue(
            first_content_line.startswith("Cache worker synchronises redis cache keys"),
            "Technical doc must lead with the payload in sentence one",
        )

        # Headings structure
        self.assertIn("## Why use cache worker", content)
        self.assertIn("## What cache worker does", content)
        self.assertIn("## How to start cache worker", content)

    def test_on_writing_well_web_content_surface_job_story_and_layering(self):
        """Verify Web Content sample anchors to a user need (job story) and foraging structure."""
        web_sample = EXERCISE_DIR / "sample_web_content.md"
        content = web_sample.read_text(encoding="utf-8")

        self.assertIn("When I", content)
        self.assertIn("I want to", content)
        self.assertIn("so I can", content)
        self.assertIn("[Manage storage plan](/settings/storage)", content)

    def test_on_writing_well_ux_microcopy_patterns(self):
        """Verify UX Microcopy sample follows what + why + fix and Verb + Object controls."""
        ux_sample = EXERCISE_DIR / "sample_ux_microcopy.md"
        content = ux_sample.read_text(encoding="utf-8")

        # Error recovery: what happened, why, and how to fix
        self.assertIn("Cannot save deployment configuration (socket timeout after 30 seconds)", content)
        self.assertIn("Check network connection and retry the save operation", content)

        # Button verb-matching
        self.assertIn("Delete cluster", content)
        self.assertIn("Keep cluster", content)
        self.assertNotIn("OK", content)

    def test_on_writing_well_longform_prose_cadence_and_grounding(self):
        """Verify Longform Prose sample uses hook lead, consistent unity and no summary recaps."""
        prose_sample = EXERCISE_DIR / "sample_longform_prose.md"
        content = prose_sample.read_text(encoding="utf-8")

        # Hook lead without throat-clearing
        self.assertIn("At dawn on 18 October", content)

        # Consistent first person plural (we)
        self.assertIn("We began with", content)
        self.assertIn("We decided to", content)

        # Clean ending with spaced en-dash, no recap
        self.assertIn("local NVMe drives – a pattern known as write-ahead replication", content)
        self.assertNotIn("In conclusion", content)
        self.assertNotIn("To sum up", content)

    def test_stage2_sub_editor_gate_rules_across_all_samples(self):
        """Verify all sample files adhere to Stage 2 Sub-Editor Gate and trope rules."""
        sample_files = list(EXERCISE_DIR.glob("*.md"))
        self.assertGreaterEqual(len(sample_files), 5)

        banned_tropes = [
            "In conclusion",
            "To sum up",
            "In summary",
            "It is worth noting",
            "seamlessly",
            "robust",
            "cutting-edge",
        ]

        for sample_file in sample_files:
            text = sample_file.read_text(encoding="utf-8")
            # Typography check
            self.assertNotIn("—", text, f"{sample_file.name} contains unspaced em-dash")
            self.assertNotIn("“", text, f"{sample_file.name} contains opening double curly quote")
            self.assertNotIn("”", text, f"{sample_file.name} contains closing double curly quote")
            self.assertNotIn("‘", text, f"{sample_file.name} contains opening single curly quote")
            self.assertNotIn("’", text, f"{sample_file.name} contains closing single curly quote")
            self.assertNotIn("→", text, f"{sample_file.name} contains Unicode right arrow")
            self.assertNotIn("←", text, f"{sample_file.name} contains Unicode left arrow")

            for trope in banned_tropes:
                self.assertNotIn(trope, text, f"{sample_file.name} contains banned trope '{trope}'")

    def test_setup_writing_framework_scaffolding_behavior(self):
        """Verify setup-writing-framework scaffolding logic in an isolated test directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            target_agents = temp_path / "AGENTS.md"

            # Pre-existing AGENTS.md with other instructions
            target_agents.write_text(
                "# Existing Project Guidelines\n\n"
                "## Existing Section\n\n"
                "Keep these existing instructions intact.\n",
                encoding="utf-8",
            )

            framework_block = (
                "## Writing framework\n\n"
                "Two-stage Editorial Pipeline for authored documentation, copy and commit messages:\n\n"
                "### Stage 1: Drafting\n\n"
                "Route drafting to the active specialist skill based on Surface and Reader Job:\n"
                "- `on-writing-well`: Human-centred prose, conceptual overviews, developer guides, README introductions, web content design and interface microcopy.\n"
                "- `ste-80`: Operational software documentation, runbooks, deployment procedures, CLI flag and command specifications, API guides and troubleshooting steps.\n"
                "- `project-narrative`: Evidence-linked project narrative and historical milestone posts (`NARRATIVE.md`).\n"
                "- `cbeams-git-commit-messages`: Git commit subject lines and bodies.\n\n"
                "### Stage 2: Sub-Editor Gate\n\n"
                "Run all drafted prose, documentation and copy through `guardian-style-guide` before delivery (commit messages are exempt):\n"
                "- Enforce British English spelling (`-ise`, `-our`), down-style capitalisation and Guardian house style.\n"
                "- Validate typography and punctuation: double quotation marks for speech, straight quotes in Markdown, zero unspaced em-dashes. Spaced en-dashes (` – `) are explicitly permitted for parenthetical pauses.\n"
                "- Run trope check against AI writing clichés and brochure adjectives.\n"
                "- Preserve authorial voice, structural design and verbatim quotations.\n"
            )

            # Surgical insertion
            current_content = target_agents.read_text(encoding="utf-8")
            updated_content = f"{current_content}\n{framework_block}"
            target_agents.write_text(updated_content, encoding="utf-8")

            # Verify preservation of existing content and presence of framework
            result = target_agents.read_text(encoding="utf-8")
            self.assertIn("## Existing Section", result)
            self.assertIn("Keep these existing instructions intact.", result)
            self.assertIn("## Writing framework", result)
            self.assertIn("Stage 1: Drafting", result)
            self.assertIn("Stage 2: Sub-Editor Gate", result)


if __name__ == "__main__":
    unittest.main()
