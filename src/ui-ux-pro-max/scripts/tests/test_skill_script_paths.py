"""Documented scripts ship with their skill and run outside the source checkout.

Sibling notation names another bundled skill; a runtime may resolve that skill
to a separate installation directory. The file check verifies the source bundle,
and the execution check exercises a relocated core skill from a project directory.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = next(
    parent for parent in Path(__file__).resolve().parents
    if (parent / "scripts" / "generate-catalog-summary.py").is_file()
)
SKILL_TREES = ("cli/assets/skills", ".claude/skills")
INVOCATION = re.compile(r'(?<![\w/.-])(?:python3?|node|bash)\s+"?([^\s"`\']+\.(?:py|cjs|js|mjs|sh))')


def shipped_invocations():
    for tree in SKILL_TREES:
        for skill_dir in sorted((REPO / tree).iterdir()):
            if not skill_dir.is_dir():
                continue
            for md in sorted(skill_dir.rglob("*.md")):
                for lineno, line in enumerate(md.read_text(encoding="utf-8").splitlines(), 1):
                    for match in INVOCATION.finditer(line):
                        yield skill_dir, md, lineno, match.group(1)


def resolve(skill_dir, path):
    """Return (target, None) for a skill-relative path, or (None, reason)."""
    if path.startswith("scripts/"):
        return skill_dir / path, None
    if path.startswith("../"):
        parts = path.split("/")
        if len(parts) > 3 and parts[2] == "scripts" and (skill_dir.parent / parts[1]).is_dir():
            return skill_dir.parent / parts[1] / "/".join(parts[2:]), None
        return None, "a sibling invocation must be ../<skill>/scripts/<file> and the sibling must ship"
    return None, "not skill-relative (expected scripts/<file> or ../<skill>/scripts/<file>)"


class SkillScriptPathsTest(unittest.TestCase):
    def test_every_shipped_markdown_invocation_resolves_from_the_skill_directory(self):
        problems, seen = [], 0
        for skill_dir, md, lineno, path in shipped_invocations():
            seen += 1
            target, reason = resolve(skill_dir, path)
            if reason is None and not target.is_file():
                reason = f"no such file: {target}"
            if reason:
                problems.append(f"{md.relative_to(REPO)}:{lineno}: {path} -- {reason}")
        # Guard against a silently broken extractor: the two trees carry well over
        # a hundred documented invocations between them.
        self.assertGreater(seen, 100, f"extractor found only {seen} invocations")
        self.assertEqual(problems, [], "\n" + "\n".join(problems))

    def test_core_search_runs_from_relocated_skill_with_project_cwd(self):
        with tempfile.TemporaryDirectory(prefix="skill runtime ") as temp:
            root = Path(temp)
            skill = root / "catalog" / "snapshot-123"
            project = root / "project with spaces"
            project.mkdir()
            source = REPO / ".claude" / "skills" / "ui-ux-pro-max"
            for folder in ("scripts", "data"):
                shutil.copytree(source / folder, skill / folder,
                                ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            env = {key: value for key, value in os.environ.items()
                   if not key.upper().startswith("CLAUDE_")}
            result = subprocess.run(
                [sys.executable, "-B", str(skill / "scripts" / "search.py"),
                 "keyboard focus modal", "--domain", "ux", "--json"],
                cwd=project, env=env, capture_output=True, text=True, encoding="utf-8",
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["domain"], "ux")
            self.assertTrue(payload["results"])
            self.assertEqual(list(project.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
