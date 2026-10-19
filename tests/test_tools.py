"""Regression tests for observable scaffold and static-validator behavior."""
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("lint_skill", ROOT / "scripts/lint_skill.py")
lint = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lint)


class ToolsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.skill = self.base / "sample"
        self.skill.mkdir()
        self.write("SKILL.md", "---\nname: sample\ndescription: Sample capability\n---\n# Sample\n")

    def write(self, name, text):
        path = self.skill / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def check(self):
        return lint.lint_skill(self.skill)

    def scaffold(self, name="new-skill", desc="Description: with colon\nand newline"):
        return subprocess.run([sys.executable, "-B", str(ROOT / "scripts/scaffold_skill.py"),
                               "--name", name, "--desc", desc,
                               "--target-dir", str(self.base / name)], capture_output=True, text=True)

    def test_minimal_skill_is_valid(self):
        self.assertEqual(self.check(), [])

    def test_scaffold_only_creates_entry_and_roundtrips_description(self):
        self.assertEqual(self.scaffold().returncode, 0)
        out = self.base / "new-skill"
        self.assertEqual([x.name for x in out.iterdir()], ["SKILL.md"])
        fm = lint.parse_frontmatter((out / "SKILL.md").read_text())
        self.assertEqual(fm["description"], "Description: with colon\nand newline")
        self.assertTrue(any("骨架标记" in e for e in lint.lint_skill(out)))

    def test_existing_directory_is_preserved_without_prompt(self):
        before = (self.skill / "SKILL.md").read_bytes()
        self.assertNotEqual(self.scaffold("sample").returncode, 0)
        self.assertEqual(before, (self.skill / "SKILL.md").read_bytes())

    def test_invalid_name_creates_nothing(self):
        self.assertNotEqual(self.scaffold("Bad_Name").returncode, 0)
        self.assertFalse((self.base / "Bad_Name").exists())

    def test_malformed_yaml_fails(self):
        self.write("SKILL.md", "---\nname: sample\ndescription: [unclosed\n---\n")
        self.assertTrue(any("YAML" in e for e in self.check()))

    def test_folded_yaml_works(self):
        self.write("SKILL.md", "---\nname: sample\ndescription: >-\n  Useful capability\n  for a real task\n---\n")
        self.assertEqual(self.check(), [])

    def test_name_mismatch_fails(self):
        self.write("SKILL.md", "---\nname: wrong\ndescription: useful\n---\n")
        self.assertTrue(any("目录名" in e for e in self.check()))

    def test_sibling_file_cannot_satisfy_local_reference(self):
        sibling = self.base / "sibling/references/missing.md"
        sibling.parent.mkdir(parents=True)
        sibling.write_text("not local")
        with (self.skill / "SKILL.md").open("a") as out:
            out.write("Read [guide](references/missing.md).\n")
        self.assertTrue(any("missing.md" in e for e in self.check()))

    def test_explicit_external_skill_path_is_not_treated_as_local(self):
        with (self.skill / "SKILL.md").open("a") as out:
            out.write("Use `other-skill/scripts/action.py` when installed.\n")
        self.assertEqual(self.check(), [])

    def test_missing_code_example_is_flagged_without_claiming_it_exists(self):
        with (self.skill / "SKILL.md").open("a") as out:
            out.write("For example, `assets/example.png`.\n")
        warnings = []
        self.assertEqual(lint.lint_skill(self.skill, warnings), [])
        self.assertTrue(any("assets/example.png" in w for w in warnings))

    def test_relative_markdown_links_resolve_from_document(self):
        self.write("references/guide.md", "Read [detail](detail.md).")
        self.write("references/detail.md", "A detail.")
        self.assertEqual(self.check(), [])
        (self.skill / "references/detail.md").unlink()
        self.assertTrue(any("detail.md" in e for e in self.check()))

    def test_python_is_never_executed_even_with_guard(self):
        marker = self.base / "marker"
        self.write("scripts/probe.py", "from pathlib import Path\nPath(" + repr(str(marker))
                   + ").write_text('executed')\nif __name__ == '__main__':\n    pass\n")
        self.assertEqual(self.check(), [])
        self.assertFalse(marker.exists())
        self.assertFalse(list(self.skill.rglob("*.pyc")))

    def test_nested_python_syntax_is_checked(self):
        self.write("helpers/nested/bad.py", "def broken(\n")
        self.assertTrue(any("bad.py" in e for e in self.check()))

    def test_archived_code_is_excluded(self):
        self.write("archive/old.py", "def broken(\n")
        self.assertEqual(self.check(), [])

    def test_bad_eval_shapes_report_errors_without_crashing(self):
        for blob in [None, 1, True, "text", [], [None], {"evals": [1]}, {"evals": [{"id": []}]}]:
            with self.subTest(blob=blob):
                self.write("evals/evals.json", json.dumps(blob))
                self.assertTrue(self.check())

    def test_eval_routes_are_domain_specific(self):
        self.write("evals/evals.json", json.dumps({"evals": [{"id": "one", "prompt": "Do task",
                   "route_expected": "audio-repair", "expectations": ["Output plays correctly"]}]}))
        self.assertEqual(self.check(), [])

    def test_skill_root_relative_eval_files_are_supported(self):
        self.write("evals/evals.json", json.dumps([{"id": "one", "prompt": "Do task",
                   "must_do": ["Result"], "files": ["SKILL.md"]}]))
        self.assertEqual(self.check(), [])

    def test_route_only_is_not_acceptance_criteria(self):
        self.write("evals/evals.json", json.dumps([{"id": "one", "prompt": "Do task", "route_expected": "create"}]))
        self.assertTrue(any("判据" in e for e in self.check()))

    def test_duplicate_ids_and_missing_fixtures_fail(self):
        case = {"id": "one", "prompt": "Do task", "must_do": ["Result"], "files": ["fixtures/missing.md"]}
        self.write("evals/evals.json", json.dumps([case, case]))
        errors = self.check()
        self.assertTrue(any("重复" in e for e in errors))
        self.assertTrue(any("样本不存在" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
