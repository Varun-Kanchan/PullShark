"""
Configuration defaults and validation for PullShark.
"""

from dataclasses import dataclass


@dataclass
class Config:
    """PullShark configuration with sensible defaults."""

    github_username: str = ""
    github_token: str = ""
    repo_name: str = ""
    num_prs: int = 4
    base_branch: str = "main"
    delay_seconds: int = 10
    max_retries: int = 3
    dry_run: bool = False
    merge_method: str = "merge"
    branch_prefix: str = "auto-pr"
    log_file: str = ""
    output_file: str = ""

    def validate(self) -> list[str]:
        """Return a list of validation errors (empty = valid)."""
        errors: list[str] = []
        if not self.github_username:
            errors.append("GITHUB_USERNAME is required.")
        if not self.github_token:
            errors.append("GITHUB_TOKEN is required.")
        if not self.repo_name:
            errors.append("REPO_NAME is required.")
        if self.num_prs < 1:
            errors.append("NUM_PRS must be at least 1.")
        if self.delay_seconds < 0:
            errors.append("DELAY_SECONDS cannot be negative.")
        if self.max_retries < 1:
            errors.append("MAX_RETRIES must be at least 1.")
        if self.merge_method not in ("merge", "squash", "rebase"):
            errors.append("MERGE_METHOD must be one of: merge, squash, rebase.")
        if not self.branch_prefix:
            errors.append("BRANCH_PREFIX cannot be empty.")
        return errors
