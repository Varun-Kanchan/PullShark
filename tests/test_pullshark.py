"""
Tests for PullShark package.
"""

import json
import os
import tempfile

from pullshark import __version__
from pullshark.config import Config
from pullshark.core import PullSharkBot
from pullshark.utils import (
    _get_tier,
    build_run_report,
    generate_random_string,
    save_report,
)


# -- Version ------------------------------------------------------------------

def test_version_is_string():
    assert isinstance(__version__, str)
    assert "." in __version__


# -- Config -------------------------------------------------------------------

class TestConfig:
    def test_defaults(self):
        c = Config()
        assert c.num_prs == 4
        assert c.base_branch == "main"
        assert c.delay_seconds == 10
        assert c.max_retries == 3
        assert c.dry_run is False
        assert c.merge_method == "merge"
        assert c.branch_prefix == "auto-pr"
        assert c.log_file == ""
        assert c.output_file == ""

    def test_empty_config_has_errors(self):
        c = Config()
        errors = c.validate()
        assert len(errors) == 3
        assert any("GITHUB_USERNAME" in e for e in errors)
        assert any("GITHUB_TOKEN" in e for e in errors)
        assert any("REPO_NAME" in e for e in errors)

    def test_valid_config_passes(self):
        c = Config(github_username="u", github_token="t", repo_name="r")
        assert c.validate() == []

    def test_invalid_merge_method(self):
        c = Config(github_username="u", github_token="t", repo_name="r", merge_method="bad")
        errors = c.validate()
        assert any("MERGE_METHOD" in e for e in errors)

    def test_invalid_num_prs(self):
        c = Config(github_username="u", github_token="t", repo_name="r", num_prs=0)
        errors = c.validate()
        assert any("NUM_PRS" in e for e in errors)

    def test_invalid_delay(self):
        c = Config(github_username="u", github_token="t", repo_name="r", delay_seconds=-1)
        errors = c.validate()
        assert any("DELAY_SECONDS" in e for e in errors)

    def test_empty_branch_prefix(self):
        c = Config(github_username="u", github_token="t", repo_name="r", branch_prefix="")
        errors = c.validate()
        assert any("BRANCH_PREFIX" in e for e in errors)

    def test_valid_merge_methods(self):
        for method in ("merge", "squash", "rebase"):
            c = Config(github_username="u", github_token="t", repo_name="r", merge_method=method)
            assert c.validate() == [], f"merge_method='{method}' should be valid"


# -- Utils --------------------------------------------------------------------

class TestGenerateRandomString:
    def test_length(self):
        for length in (1, 4, 8, 16, 32):
            s = generate_random_string(length)
            assert len(s) == length

    def test_lowercase_only(self):
        s = generate_random_string(100)
        assert s.islower()
        assert s.isalpha()

    def test_uniqueness(self):
        strings = {generate_random_string(16) for _ in range(50)}
        assert len(strings) == 50  # all unique


class TestGetTier:
    def test_none(self):
        assert _get_tier(0) == "None"
        assert _get_tier(1) == "None"

    def test_default(self):
        assert _get_tier(2) == "Default"
        assert _get_tier(15) == "Default"

    def test_bronze(self):
        assert _get_tier(16) == "Bronze"
        assert _get_tier(127) == "Bronze"

    def test_silver(self):
        assert _get_tier(128) == "Silver"
        assert _get_tier(1023) == "Silver"

    def test_gold(self):
        assert _get_tier(1024) == "Gold"
        assert _get_tier(9999) == "Gold"


class TestBuildRunReport:
    def test_report_structure(self):
        config = Config(
            github_username="testuser",
            github_token="ghp_xxx",
            repo_name="testrepo",
            num_prs=4,
            merge_method="squash",
            branch_prefix="bot",
        )
        results = [
            {"index": 1, "merged": True, "branch": "bot-abc", "pr_number": 1, "pr_url": "https://github.com/test"},
            {"index": 2, "merged": True, "branch": "bot-def", "pr_number": 2, "pr_url": "https://github.com/test"},
            {"index": 3, "merged": False, "error": "Merge failed"},
        ]
        report = build_run_report(results, config)

        assert report["summary"]["total"] == 4
        assert report["summary"]["successful"] == 2
        assert report["summary"]["failed"] == 2
        assert report["summary"]["pull_shark_tier"] == "Default"
        assert report["config"]["username"] == "testuser"
        assert report["config"]["merge_method"] == "squash"
        assert report["config"]["branch_prefix"] == "bot"
        assert len(report["pull_requests"]) == 3
        assert "timestamp" in report
        assert "version" in report


class TestSaveReport:
    def test_saves_json(self):
        report = {"test": True, "nested": {"key": "value"}}
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            filepath = f.name

        try:
            save_report(report, filepath)
            with open(filepath) as f:
                loaded = json.load(f)
            assert loaded == report
        finally:
            os.unlink(filepath)


# -- PullSharkBot -------------------------------------------------------------

class TestPullSharkBot:
    def test_instantiation(self):
        c = Config(github_username="u", github_token="t", repo_name="r")
        bot = PullSharkBot(c)
        assert bot.config.github_username == "u"

    def test_has_clean_method(self):
        bot = PullSharkBot(Config())
        assert hasattr(bot, "clean")
        assert callable(bot.clean)

    def test_has_check_rate_limit(self):
        bot = PullSharkBot(Config())
        assert hasattr(bot, "check_rate_limit")
        assert callable(bot.check_rate_limit)

    def test_branch_prefix_from_config(self):
        c = Config(github_username="u", github_token="t", repo_name="r", branch_prefix="mybot")
        bot = PullSharkBot(c)
        assert bot.config.branch_prefix == "mybot"


# -- CLI ----------------------------------------------------------------------

class TestCLI:
    def test_build_parser(self):
        from pullshark.cli import build_parser
        parser = build_parser()
        assert parser is not None

    def test_run_subcommand_args(self):
        from pullshark.cli import build_parser
        parser = build_parser()
        args = parser.parse_args([
            "run", "-t", "ghp_x", "-u", "user", "-r", "repo",
            "--prs", "6", "--dry-run", "--merge-method", "squash",
            "--check-rate", "--prefix", "bot", "--log", "test.log", "--output", "out.json",
        ])
        assert args.command == "run"
        assert args.prs == 6
        assert args.dry_run is True
        assert args.merge_method == "squash"
        assert args.check_rate is True
        assert args.prefix == "bot"
        assert args.log == "test.log"
        assert args.output == "out.json"

    def test_clean_subcommand_args(self):
        from pullshark.cli import build_parser
        parser = build_parser()
        args = parser.parse_args([
            "clean", "-t", "ghp_x", "-u", "user", "-r", "repo",
            "--dry-run", "--prefix", "custom",
        ])
        assert args.command == "clean"
        assert args.dry_run is True
        assert args.prefix == "custom"

    def test_backward_compat_flat_args(self):
        from pullshark.cli import build_parser
        parser = build_parser()
        # Simulate flat args → should be prefixed with 'run'
        test_argv = ["--token", "x", "--username", "u", "--repo", "r"]
        if test_argv[0] not in ("run", "clean", "--help", "-h"):
            test_argv = ["run"] + test_argv
        args = parser.parse_args(test_argv)
        assert args.command == "run"


# -- Notebook -----------------------------------------------------------------

class TestNotebook:
    def test_valid_json(self):
        with open("notebooks/PullShark.ipynb") as f:
            nb = json.load(f)
        assert nb["nbformat"] == 4
        assert len(nb["cells"]) >= 8

    def test_has_all_steps(self):
        with open("notebooks/PullShark.ipynb") as f:
            nb = json.load(f)
        sources = ["".join(c["source"]) for c in nb["cells"] if c["cell_type"] == "code"]
        combined = " ".join(sources)
        assert "Step 1" in combined
        assert "Step 2" in combined
        assert "Step 3" in combined
        assert "Step 4" in combined
        assert "Step 5" in combined


# -- Files --------------------------------------------------------------------

class TestProjectFiles:
    def test_gitignore_exists(self):
        assert os.path.exists(".gitignore")

    def test_changelog_exists(self):
        assert os.path.exists("CHANGELOG.md")

    def test_changelog_versions(self):
        with open("CHANGELOG.md") as f:
            content = f.read()
        assert "## [2.4.5]" in content
        assert "## [2.4.4]" in content
        assert "## [2.4.3]" in content
        assert "## [2.4.2]" in content
        assert "## [2.4.1]" in content
        assert "## [2.4.0]" in content
        assert "## [2.3.0]" in content
        assert "## [2.2.0]" in content
        assert "## [2.1.0]" in content
        assert "## [2.0.0]" in content
        assert "## [1.0.0]" in content

    def test_pyproject_toml(self):
        assert os.path.exists("pyproject.toml")
        with open("pyproject.toml") as f:
            content = f.read()
        assert "[project]" in content
        assert "[project.scripts]" in content
        assert 'pullshark = "pullshark.cli:main"' in content

    def test_contributing_exists(self):
        assert os.path.exists("CONTRIBUTING.md")

    def test_ci_workflow_exists(self):
        assert os.path.exists(".github/workflows/ci.yml")
