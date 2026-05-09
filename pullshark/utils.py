"""
Utility helpers for PullShark.
"""

import random
import string
import time

from github import GithubException
from github.PullRequest import PullRequest


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
) -> bool:
    """Attempt to merge a PR with retry logic.

    Args:
        pr: The PullRequest to merge.
        max_retries: Number of attempts before giving up.
        delay_seconds: Wait time between retries.

    Returns:
        True if merge succeeded, False otherwise.
    """
    for attempt in range(1, max_retries + 1):
        try:
            pr.merge(merge_method="merge")
            return True
        except GithubException as e:
            print(f"  ❌ Merge attempt {attempt}/{max_retries} failed: {e}")
            if attempt < max_retries:
                print(f"  ⏳ Waiting {delay_seconds}s before retry...")
                time.sleep(delay_seconds)
                pr.update()
    return False
