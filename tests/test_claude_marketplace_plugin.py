"""Validation suite for the Claude Web Marketplace and MiroFish plugin."""

from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE_JSON = REPO_ROOT / ".claude-plugin" / "marketplace.json"
PLUGIN_ROOT = REPO_ROOT / "plugins" / "mirofish"
PLUGIN_JSON = PLUGIN_ROOT / ".claude-plugin" / "plugin.json"

RESERVED_MARKETPLACE_NAMES = {
    "claude-code-marketplace",
    "claude-code-plugins",
    "claude-plugins-official",
    "anthropic-marketplace",
    "anthropic-plugins",
    "agent-skills",
    "anthropic-agent-skills",
    "life-sciences",
    "knowledge-work-plugins",
    "claude-for-legal",
    "claude-for-financial-services",
    "financial-services-plugins",
    "first-party-plugins",
    "claude-tag-plugins",
    "claude-community",
    "claude-plugins-community",
    "healthcare",
    "anthropic-plugin-directory",
    "claude-plugin-directory",
    "inline",
    "builtin",
    "skills-dir",
    "synced",
    "claude-plugin-test",
    "npm",
    "pip",
    "uv",
    "cargo",
    "github",
    "gh",
}

ALLOWED_PLUGIN_MANIFEST_KEYS = {
    "$schema",
    "name",
    "displayName",
    "version",
    "description",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
    "defaultEnabled",
    "dependencies",
    "metadata",
    "skills",
    "commands",
    "agents",
    "hooks",
    "mcpServers",
    "lspServers",
    "outputStyles",
    "experimental",
    "userConfig",
    "channels",
}


def parse_simple_frontmatter(text: str) -> dict[str, str]:
    assert text.startswith("---\n"), "SKILL.md must begin with YAML frontmatter delimiter '---'"
    end_idx = text.find("\n---\n", 4)
    assert end_idx != -1, "SKILL.md must close YAML frontmatter with '---'"
    raw = text[4:end_idx]
    parsed: dict[str, str] = {}
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        assert ":" in line, f"Invalid frontmatter line: {line}"
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        assert not val.startswith("["), f"Frontmatter field '{key}' must not be a list"
        if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
            val = val[1:-1]
        parsed[key] = val
    return parsed


class TestClaudeMarketplacePlugin(unittest.TestCase):
    def test_marketplace_manifest_is_valid(self) -> None:
        self.assertTrue(MARKETPLACE_JSON.is_file(), "Missing .claude-plugin/marketplace.json")
        data = json.loads(MARKETPLACE_JSON.read_text(encoding="utf-8"))

        name = data.get("name", "")
        self.assertRegex(name, r"^[a-z0-9][a-z0-9._-]*[a-z0-9]$")
        self.assertNotIn("..", name)
        self.assertNotIn(name.lower(), RESERVED_MARKETPLACE_NAMES)
        self.assertFalse(name.lower().startswith("claudeai-"))
        self.assertNotEqual(name.lower(), "osa822630-droid-mirofish")

        self.assertTrue(isinstance(data.get("description"), str) and data["description"].strip())
        owner = data.get("owner", {})
        self.assertTrue(isinstance(owner.get("name"), str) and owner["name"].strip())

        plugins = data.get("plugins", [])
        self.assertGreaterEqual(len(plugins), 1)
        entry = plugins[0]
        self.assertEqual(entry["name"], "mirofish")
        self.assertEqual(entry["source"], "./plugins/mirofish")
        self.assertNotIn("..", entry["source"])
        self.assertNotIn("\\", entry["source"])
        # Avoid duplicate version warning when plugin.json declares version
        self.assertNotIn("version", entry)

    def test_plugin_manifest_and_directory_hygiene(self) -> None:
        dot_dir_files = list((PLUGIN_ROOT / ".claude-plugin").iterdir())
        self.assertEqual(
            [p.name for p in dot_dir_files],
            ["plugin.json"],
            "Only plugin.json may reside inside plugins/mirofish/.claude-plugin/",
        )

        manifest = json.loads(PLUGIN_JSON.read_text(encoding="utf-8"))
        unknown_keys = set(manifest.keys()) - ALLOWED_PLUGIN_MANIFEST_KEYS
        self.assertEqual(unknown_keys, set(), f"Unrecognized plugin.json keys: {unknown_keys}")

        self.assertRegex(manifest["name"], r"^[a-z0-9][a-z0-9-]{0,62}[a-z0-9]$")
        self.assertEqual(manifest["name"], "mirofish")
        self.assertTrue(manifest.get("version"))
        self.assertTrue(manifest.get("description"))
        self.assertTrue(manifest.get("author", {}).get("name"))
        self.assertTrue(manifest.get("license"))

        # Claude Web compatibility: no top-level bin/, no lockfiles, no symlinks, <= 256 KiB per file
        self.assertFalse((PLUGIN_ROOT / "bin").exists(), "Top-level bin/ blocks claude.ai installation")
        for forbidden in ("package-lock.json", "uv.lock", "bun.lock", "bun.lockb", ".DS_Store", "Thumbs.db"):
            self.assertEqual(list(PLUGIN_ROOT.rglob(forbidden)), [])

        all_files = [p for p in PLUGIN_ROOT.rglob("*") if p.is_file() or p.is_symlink()]
        self.assertLessEqual(len(all_files), 512)
        for path in all_files:
            self.assertFalse(path.is_symlink(), f"Symlink not allowed in plugin: {path}")
            self.assertLess(path.stat().st_size, 256 * 1024, f"File exceeds 256 KiB: {path}")
            text = path.read_text(encoding="utf-8")
            for env_secret in ("$GITHUB_TOKEN", "$OPENAI_API_KEY", "$ANTHROPIC_API_KEY", "$LLM_API_KEY", "$ZEP_API_KEY"):
                self.assertNotIn(env_secret, text, f"Env credential reference {env_secret} in {path}")

        # README word count outside code blocks >= 40
        readme = (PLUGIN_ROOT / "README.md").read_text(encoding="utf-8")
        stripped = re.sub(r"```.*?```", " ", readme, flags=re.DOTALL)
        words = re.findall(r"[A-Za-z]{2,}", stripped)
        self.assertGreaterEqual(len(words), 40)
        self.assertTrue((PLUGIN_ROOT / "LICENSE").is_file())

    def test_all_skills_conform_to_agent_skills_spec(self) -> None:
        skills_dir = PLUGIN_ROOT / "skills"
        skill_folders = sorted(p for p in skills_dir.iterdir() if p.is_dir())
        self.assertEqual(
            [p.name for p in skill_folders],
            ["build-graph", "inject-variable", "interview-agents", "simulate", "visualize-world"],
        )

        for folder in skill_folders:
            skill_md = folder / "SKILL.md"
            self.assertTrue(skill_md.is_file(), f"Missing SKILL.md in {folder}")
            content = skill_md.read_text(encoding="utf-8")
            self.assertLess(len(content.splitlines()), 500, f"SKILL.md exceeds 500 lines in {folder}")

            fm = parse_simple_frontmatter(content)
            self.assertEqual(fm.get("name"), folder.name)
            self.assertRegex(fm["name"], r"^[a-z0-9-]{1,64}$")
            desc = fm.get("description", "")
            self.assertGreater(len(desc), 20)
            self.assertLessEqual(len(desc), 1024)

            for rel_ref in re.findall(r"(?:references|assets|scripts)/[A-Za-z0-9._-]+", content):
                self.assertTrue((folder / rel_ref).is_file(), f"Missing referenced file {rel_ref} in {folder}")

    def test_swarm_engine_self_test_runs_deterministically(self) -> None:
        engine = PLUGIN_ROOT / "skills" / "simulate" / "scripts" / "swarm_engine.py"
        proc = subprocess.run(
            [sys.executable, str(engine), "--self-test"],
            check=True,
            capture_output=True,
            text=True,
        )
        output = json.loads(proc.stdout)
        self.assertEqual(output["swarm_size"], 120)
        self.assertEqual(len(output["timeline"]), 12)
        self.assertIn("counterfactual_comparison", output)
        deltas = output["counterfactual_comparison"]["deltas"]
        self.assertGreater(deltas["mean_stance_delta"], 0.1)
        self.assertLess(deltas["opposing_share_delta"], -0.3)


if __name__ == "__main__":
    unittest.main()
