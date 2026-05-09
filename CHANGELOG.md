# Changelog

All notable changes to this project will be documented in this file.

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
