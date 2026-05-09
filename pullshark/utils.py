"""
Utility helpers for PullShark.
"""

import json
import logging
import random
import string
import time
from datetime import datetime, timezone

from github import GithubException
from github.PullRequest import PullRequest

logger = logging.getLogger("pullshark")


def generate_random_string(length: int = 8) -> str:
    """Generate a random lowercase string for branch names and commit messages."""
    return "".join(random.choices(string.ascii_lowercase, k=length))


def wait_for_mergeability(pr: PullRequest, max_wait: int = 30) -> bool:
    """Poll GitHub until the PR is mergeable or timeout is reached.

    Args:
        pr: The PullRequest object to poll.
        max_wait: Maximum seconds to wait.

    Returns:
        True if the PR is mergeable, False on timeout.
    """
    waited = 0
    while waited < max_wait:
        pr.update()
        if pr.mergeable is not False:  # True or None (still calculating)
            return True
        time.sleep(3)
        waited += 3
    return False


def merge_with_retry(
    pr: PullRequest,
    max_retries: int = 3,
    delay_seconds: int = 10,
    merge_method: str = "merge",
) -> bool:
    """Attempt to merge a PR with retry logic.

    Args:
        pr: The PullRequest to merge.
        max_retries: Number of attempts before giving up.
        delay_seconds: Wait time between retries.
        merge_method: One of 'merge', 'squash', 'rebase'.

    Returns:
        True if merge succeeded, False otherwise.
    """
    for attempt in range(1, max_retries + 1):
        try:
            pr.merge(merge_method=merge_method)
            return True
        except GithubException as e:
            logger.warning("Merge attempt %d/%d failed: %s", attempt, max_retries, e)
            if attempt < max_retries:
                logger.info("Waiting %ds before retry...", delay_seconds)
                time.sleep(delay_seconds)
                pr.update()
    return False


def build_run_report(results: list[dict], config) -> dict:
    """Build a structured JSON report of the run.

    Args:
        results: List of per-PR result dicts.
        config: The Config object used for the run.

    Returns:
        Report dict ready for JSON serialization.
    """
    successful = sum(1 for r in results if r.get("merged"))
    return {
        "version": "2.3.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "config": {
            "username": config.github_username,
            "repo": config.repo_name,
            "base_branch": config.base_branch,
            "num_prs": config.num_prs,
            "merge_method": config.merge_method,
            "branch_prefix": config.branch_prefix,
            "delay_seconds": config.delay_seconds,
            "max_retries": config.max_retries,
        },
        "summary": {
            "total": config.num_prs,
            "successful": successful,
            "failed": config.num_prs - successful,
            "pull_shark_tier": _get_tier(successful),
        },
        "pull_requests": results,
    }


def _get_tier(count: int) -> str:
    if count >= 1024:
        return "Gold"
    if count >= 128:
        return "Silver"
    if count >= 16:
        return "Bronze"
    if count >= 2:
        return "Default"
    return "None"


def save_report(report: dict, filepath: str) -> None:
    """Save a run report to a JSON file.

    Args:
        report: The report dict from build_run_report.
        filepath: Path to write the JSON file.
    """
    with open(filepath, "w") as f:
        json.dump(report, f, indent=2)
    logger.info("Report saved to %s", filepath)
