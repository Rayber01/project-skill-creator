"""Tests for the validator, the scaffolder, the install script and the repo's own skills.

Run with:  python3 -m unittest discover -s tests -v
"""
import io
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "skills" / "project-skill-creator"
sys.path.insert(0, str(SKILL_DIR / "scripts"))

import init_skill  # noqa: E402
import validate_skill  # noqa: E402

GOOD_DESC = "Does something useful for the project. Use when the user asks for the useful thing."


def make_skill(root, name="demo-skill", description=GOOD_DESC, extra_fm="", body="# Demo\n\n1. Do it.\n", files=None):
    folder = Path(root) / name
    folder.mkdir(parents=True, exist_ok=True)
    fm = f"---\nname: {name}\ndescription: {description}\n{extra_fm}---\n\n{body}"
    (folder / "SKILL.md").write_text(fm, encoding="utf-8")
    for rel, content in (files or {}).items():
        target = folder / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    return folder


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def check(self, folder):
        errors, warnings, name = validate_skill.validate_skill(folder)
        return errors, warnings, name

    def test_valid_skill_passes(self):
        errors, warnings, name = self.check(make_skill(self.tmp))
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])
        self.assertEqual(name, "demo-skill")

    def test_name_must_match_folder(self):
        folder = make_skill(self.tmp)
        folder.rename(self.tmp / "other-name")
        errors, _, _ = self.check(self.tmp / "other-name")
        self.assertTrue(any("must match the folder name" in e for e in errors))

    def test_uppercase_name_rejected(self):
        errors, _, _ = self.check(make_skill(self.tmp, name="Demo-Skill"))
        self.assertTrue(any("lowercase" in e for e in errors))

    def test_name_too_long(self):
        errors, _, _ = self.check(make_skill(self.tmp, name="a" * 65))
        self.assertTrue(any("max 64" in e for e in errors))

    def test_missing_description(self):
        folder = self.tmp / "no-desc"
        folder.mkdir()
        (folder / "SKILL.md").write_text("---\nname: no-desc\n---\n\nBody\n", encoding="utf-8")
        errors, _, _ = self.check(folder)
        self.assertTrue(any("'description' is required" in e for e in errors))

    def test_description_too_long(self):
        errors, _, _ = self.check(make_skill(self.tmp, description="Use when " + "x" * 1100))
        self.assertTrue(any("max 1024" in e for e in errors))

    def test_block_scalar_description_rejected(self):
        folder = self.tmp / "block-skill"
        folder.mkdir()
        (folder / "SKILL.md").write_text(
            "---\nname: block-skill\ndescription: >\n  Does a thing.\n  Use when needed.\n---\n\nBody\n",
            encoding="utf-8",
        )
        errors, _, _ = self.check(folder)
        self.assertTrue(any("single-line" in e for e in errors))

    def test_multiline_plain_description_rejected(self):
        folder = self.tmp / "multi-skill"
        folder.mkdir()
        (folder / "SKILL.md").write_text(
            "---\nname: multi-skill\ndescription: Does a thing\n  and continues here. Use when needed.\n---\n\nBody\n",
            encoding="utf-8",
        )
        errors, _, _ = self.check(folder)
        self.assertTrue(any("single-line" in e for e in errors))

    def test_quoted_description_with_colon(self):
        desc = '"Does a thing: carefully. Use when the user asks for the thing."'
        errors, warnings, _ = self.check(make_skill(self.tmp, description=desc))
        self.assertEqual(errors, [])
        self.assertEqual(warnings, [])

    def test_missing_frontmatter(self):
        folder = self.tmp / "bare"
        folder.mkdir()
        (folder / "SKILL.md").write_text("# Just markdown\n", encoding="utf-8")
        errors, _, _ = self.check(folder)
        self.assertTrue(any("frontmatter" in e for e in errors))

    def test_wrong_case_filename(self):
        folder = self.tmp / "lower"
        folder.mkdir()
        (folder / "skill.md").write_text("---\nname: lower\ndescription: x\n---\nBody\n", encoding="utf-8")
        errors, _, _ = self.check(folder)
        self.assertTrue(any("exactly SKILL.md" in e for e in errors))

    def test_empty_body(self):
        errors, _, _ = self.check(make_skill(self.tmp, body="\n"))
        self.assertTrue(any("body is empty" in e for e in errors))

    def test_broken_link_detected(self):
        folder = make_skill(self.tmp, body="See `references/missing.md` for details.\n")
        errors, _, _ = self.check(folder)
        self.assertTrue(any("broken internal link: references/missing.md" in e for e in errors))

    def test_existing_link_ok_placeholder_and_fenced_ignored(self):
        body = (
            "Read `references/real.md` and [guide](references/real.md).\n"
            "Template: `references/<topic>.md`\n"
            "```\ncat references/not-checked-in-fences.md\n```\n"
        )
        folder = make_skill(self.tmp, body=body, files={"references/real.md": "# Real\n"})
        errors, _, _ = self.check(folder)
        self.assertEqual(errors, [])

    def test_link_escaping_folder_rejected(self):
        folder = make_skill(self.tmp, body="[x](../outside.md)\n")
        (self.tmp / "outside.md").write_text("hi", encoding="utf-8")
        errors, _, _ = self.check(folder)
        self.assertTrue(any("outside the skill folder" in e for e in errors))

    def test_secret_detected(self):
        fake = "gh" + "p_" + "A" * 36
        folder = make_skill(self.tmp, files={"scripts/run.sh": f"TOKEN={fake}\n"})
        errors, _, _ = self.check(folder)
        self.assertTrue(any("possible secret" in e for e in errors))

    def test_hyphenated_words_are_not_secrets(self):
        body = "Always ask-the-user-for-confirmation-before-deleting-anything.\n"
        errors, _, _ = self.check(make_skill(self.tmp, body=body))
        self.assertEqual(errors, [])

    def test_unknown_field_and_todo_warn(self):
        folder = make_skill(self.tmp, extra_fm="version: 1\n", body="TODO write this\n")
        errors, warnings, _ = self.check(folder)
        self.assertEqual(errors, [])
        self.assertTrue(any("unknown frontmatter field 'version'" in w for w in warnings))
        self.assertTrue(any("TODO" in w for w in warnings))

    def test_missing_trigger_warns(self):
        errors, warnings, _ = self.check(
            make_skill(self.tmp, description="Handles database migrations for the project in a careful way.")
        )
        self.assertEqual(errors, [])
        self.assertTrue(any("WHEN" in w for w in warnings))

    def test_metadata_map_is_fine(self):
        folder = make_skill(self.tmp, extra_fm='license: MIT\nmetadata:\n  version: "1.0"\n')
        errors, warnings, _ = self.check(folder)
        self.assertEqual((errors, warnings), ([], []))

    def test_cli_all_and_strict_and_duplicates(self):
        make_skill(self.tmp / "a", name="same-name")
        make_skill(self.tmp / "b", name="same-name")
        out = io.StringIO()
        with redirect_stdout(out):
            code = validate_skill.main(["--all", str(self.tmp)])
        self.assertEqual(code, 1)
        self.assertIn("duplicate skill name", out.getvalue())

        solo = self.tmp / "solo"
        make_skill(solo, extra_fm="version: 1\n")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(validate_skill.main([str(solo / "demo-skill")]), 0)
            self.assertEqual(validate_skill.main(["--strict", str(solo / "demo-skill")]), 1)


class InitSkillTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def test_scaffold_with_description_is_valid_modulo_todo(self):
        with redirect_stdout(io.StringIO()):
            code = init_skill.main(
                ["deploy-staging", "--description", "Deploys to staging: runs checks first. Use when asked to deploy.",
                 "--dest", str(self.tmp), "--resources", "scripts,references"]
            )
        self.assertEqual(code, 0)
        folder = self.tmp / "deploy-staging"
        self.assertTrue((folder / "scripts").is_dir())
        errors, warnings, name = validate_skill.validate_skill(folder)
        self.assertEqual(errors, [])
        self.assertEqual(name, "deploy-staging")
        self.assertTrue(any("TODO" in w for w in warnings))  # body placeholders remain by design

    def test_bad_name_and_existing_folder(self):
        with redirect_stdout(io.StringIO()):
            self.assertEqual(init_skill.main(["Bad_Name", "--dest", str(self.tmp)]), 1)
            self.assertEqual(init_skill.main(["ok-name", "--dest", str(self.tmp)]), 0)
            self.assertEqual(init_skill.main(["ok-name", "--dest", str(self.tmp)]), 1)
            self.assertEqual(init_skill.main(["ok-name", "--dest", str(self.tmp), "--force"]), 0)


@unittest.skipUnless(shutil.which("bash"), "bash not available")
class InstallScriptTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)

    def run_install(self, *args):
        return subprocess.run(
            ["bash", str(ROOT / "adapters" / "install.sh"), *args],
            capture_output=True, text=True, env={"PATH": "/usr/bin:/bin:/usr/local/bin", "HOME": str(self.tmp / "home")},
        )

    def test_project_install_copy_exists_force_and_link(self):
        proj = self.tmp / "proj"
        proj.mkdir()
        result = self.run_install("--agent", "opencode,agents,codex", "--project-dir", str(proj))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((proj / ".opencode/skills/project-skill-creator/SKILL.md").is_file())
        self.assertTrue((proj / ".agents/skills/project-skill-creator/SKILL.md").is_file())
        self.assertIn("same folder already handled", result.stdout)

        again = self.run_install("--agent", "opencode", "--project-dir", str(proj))
        self.assertIn("use --force", again.stdout)
        forced = self.run_install("--agent", "opencode", "--project-dir", str(proj), "--force", "--link")
        self.assertEqual(forced.returncode, 0, forced.stderr)
        self.assertTrue((proj / ".opencode/skills/project-skill-creator").is_symlink())

    def test_global_install_and_dry_run(self):
        result = self.run_install("--agent", "claude", "--scope", "global", "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("would install", result.stdout)
        self.assertFalse((self.tmp / "home").exists())

    def test_unknown_agent_fails(self):
        result = self.run_install("--agent", "nope", "--project-dir", str(self.tmp))
        self.assertNotEqual(result.returncode, 0)


class RepoContentTests(unittest.TestCase):
    def test_repo_skills_and_examples_pass_strict(self):
        for folder in ("skills", "examples"):
            for skill in validate_skill.find_skill_dirs(ROOT / folder):
                errors, warnings, _ = validate_skill.validate_skill(skill)
                self.assertEqual(errors, [], f"{skill}: {errors}")
                self.assertEqual(warnings, [], f"{skill}: {warnings}")

    def test_skill_md_stays_concise(self):
        lines = (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8").splitlines()
        self.assertLess(len(lines), 120)

    def test_required_repo_files_exist(self):
        for rel in ("README.md", "README.es.md", "LICENSE", "AGENTS.md", "CONTRIBUTING.md", "SECURITY.md",
                    "CHANGELOG.md", ".gitignore", ".github/workflows/validate.yml"):
            self.assertTrue((ROOT / rel).is_file(), rel)


if __name__ == "__main__":
    unittest.main()
