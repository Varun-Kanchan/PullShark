# Changelog

All notable changes to this project will be documented in this file.

---

## [2.4.0] — 2026-05-09

### Added
- PyPI auto-publish workflow (`.github/workflows/publish.yml`) — tag a release `v*` and it publishes automatically.
- Pre-commit hooks (`.pre-commit-config.yaml`) — ruff lint/format, trailing whitespace, YAML/JSON checks, pytest.
- Dependabot config (`.github/dependabot.yml`) — weekly dependency and GitHub Actions updates.
- Colab Step 3 auto-fills credentials from Step 2.
- Colab Step 4 auto-fills credentials and merge method from Step 3.

### Changed
- Users can now `pip install pullshark` from PyPI after first tagged release.

---

## [2.3.0] — 2026-05-09

### Added
- Unit test suite (`tests/test_pullshark.py`) with pytest — 30+ tests covering config, utils, CLI, and project files.
- GitHub Actions CI workflow (`.github/workflows/ci.yml`) — runs tests across Python 3.9–3.12, lints with ruff, validates notebook JSON.
- `CONTRIBUTING.md` with development setup, workflow, and PR guidelines.
- `--log FILE` flag to save detailed debug logs to a file.
- `--output FILE` flag to save a structured JSON report of each run.
- `--prefix` flag to customize branch name prefix (default: `auto-pr`).
- `PullSharkBot.check_rate_limit()` returns API quota info before running.
- Dark mode support in Colab notebook via CSS `@media` queries.
- Fine-grained token instructions in notebook footer.
- `[dev]` optional dependencies in `pyproject.toml` (pytest, pytest-cov, ruff).
- pytest and ruff configuration in `pyproject.toml`.

### Changed
- `core.py` now uses Python `logging` module instead of bare `print` for debug output.
- `utils.py` expanded with `build_run_report()`, `save_report()`, and `_get_tier()` helpers.
- Notebook uses CSS classes (`.ps-alert`, `.ps-card`) for consistent dark/light styling.

---

## [2.2.0] — 2026-05-09

### Added
- `--dry-run` mode: preview branches, commits, and PRs without touching GitHub.
- `pullshark clean` command: bulk-delete all `auto-pr-*` branches from a repo.
- `--check-rate` flag: display GitHub API quota before starting a run.
- `--merge-method` option: choose between `merge`, `squash`, or `rebase` strategies.
- `python -m pullshark` support via `__main__.py`.
- `PullSharkBot.clean()` method for programmatic branch cleanup.
- `PullSharkBot.check_rate_limit()` method to inspect API quota.

### Changed
- CLI now uses subcommands (`pullshark run`, `pullshark clean`). Old flat args still work as a shortcut for `run`.

### Improved
- Redesigned Colab notebook with 5-step flow: Install → Test → Dry Run → Run → Cleanup.
- Step 2 now checks API rate limit and existing auto-pr branches.
- Step 3 is a new dry-run preview cell for first-time users.
- Step 4 adds merge method dropdown and rate limit pre-check toggle.
- Step 5 is a new branch cleanup cell with dry-run safety toggle.
- Added merge methods explainer to footer.

---

## [2.1.0] — 2026-05-09

### Added
- Connection test cell in Colab notebook to validate credentials before running.
- Pre-flight configuration summary with estimated completion time.
- Results summary card showing merged count, Pull Shark tier, and elapsed time.
- Slider controls for PR count, delay, and retry parameters.
- Styled HTML notifications (success, warning, error) throughout the notebook.
- Collapsible troubleshooting and token setup sections in footer.

### Improved
- Redesigned Colab notebook with better visual hierarchy and grouped form sections.
- Form fields organized into Credentials, Repository, and Automation Settings groups.

---

## [2.0.0] — 2026-05-09

### Added
- Modular Python package structure (`pullshark/`) with separate modules for config, core, utils, and CLI.
- `pyproject.toml` for modern Python packaging and `pip install` support.
- `requirements.txt` for explicit dependency declaration.
- `.gitignore` to exclude Python, Jupyter, IDE, and OS artifacts.
- CLI entry point (`pullshark` command) for running from terminal without Colab.
- `Config` dataclass with validation logic (`pullshark/config.py`).
- `PullSharkBot` class encapsulating the full automation workflow (`pullshark/core.py`).
- Standalone utility functions: `generate_random_string`, `wait_for_mergeability`, `merge_with_retry` (`pullshark/utils.py`).
- Type hints throughout the codebase.

### Changed
- Refactored Colab notebook to be a thin wrapper that imports from the `pullshark` package instead of containing all logic inline.
- Improved error handling with early exits and descriptive messages.
- Updated README.md with project structure, CLI usage, Python package usage, and installation instructions.

---

## [1.0.0] — 2026-01-01

### Added
- Initial release.
- Google Colab notebook for automated PR creation and merging.
- README with full documentation, troubleshooting, and achievement tier reference.
- MIT License.
