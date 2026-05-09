"""
Core automation logic for PullShark.
"""

import time

from github import Github, GithubException
from github.Repository import Repository

from pullshark.config import Config
from pullshark.utils import (
    generate_random_string,
    merge_with_retry,
    wait_for_mergeability,
)


class PullSharkBot:
    """Automates PR creation and merging for the Pull Shark achievement."""

    BRANCH_PREFIX = "auto-pr-"

    def __init__(self, config: Config) -> None:
        self.config = config
        self._github: Github | None = None
        self._repo: Repository | None = None

    # -- Properties -----------------------------------------------------------

    @property
    def github(self) -> Github:
        if self._github is None:
            self._github = Github(self.config.github_token)
        return self._github

    @property
    def repo(self) -> Repository:
        if self._repo is None:
            self._repo = self.github.get_user().get_repo(self.config.repo_name)
        return self._repo

    # -- Public API -----------------------------------------------------------

    def run(self) -> int:
        """Execute the full automation loop.

        Returns:
            Number of successfully merged pull requests.
        """
        cfg = self.config
        successful = 0

        self._print_header()

        if cfg.dry_run:
            print("🔍 DRY RUN — no branches, commits, or PRs will be created.\n")

        for i in range(cfg.num_prs):
            print(f"\n--- 📦 PR #{i + 1} of {cfg.num_prs} ---")

            if cfg.dry_run:
                self._dry_run_preview(i + 1)
                successful += 1
                continue

            branch_name = self._create_branch()
            if not branch_name:
                break

            self._make_commit(branch_name)

            pr = self._open_pull_request(i + 1, branch_name)
            if pr is None:
                break

            print("  ⏳ Waiting for GitHub to calculate mergeability...")
            if not wait_for_mergeability(pr):
                print("  ❌ PR not mergeable after waiting. Stopping.")
                break

            if merge_with_retry(pr, cfg.max_retries, cfg.delay_seconds, cfg.merge_method):
                print(f"  🎉 Merged PR #{pr.number}")
                successful += 1
            else:
                print("  ❌ All merge attempts exhausted. Stopping.")
                break

            if i < cfg.num_prs - 1:
                print(f"  ⏸️  Pausing {cfg.delay_seconds}s for GitHub to process...")
                time.sleep(cfg.delay_seconds)

        self._print_summary(successful)
        return successful

    def clean(self, dry_run: bool = False) -> int:
        """Delete all auto-created branches (auto-pr-*) from the repo.

        Returns:
            Number of branches deleted (or that would be deleted in dry-run).
        """
        prefix = self.BRANCH_PREFIX
        deleted = 0

        print(f"\n🧹 Scanning for '{prefix}*' branches in {self.config.repo_name}...\n")

        for branch in self.repo.get_branches():
            if branch.name.startswith(prefix):
                if dry_run:
                    print(f"  🔍 Would delete: {branch.name}")
                else:
                    try:
                        ref = self.repo.get_git_ref(f"heads/{branch.name}")
                        ref.delete()
                        print(f"  🗑️  Deleted: {branch.name}")
                    except GithubException as e:
                        print(f"  ❌ Failed to delete {branch.name}: {e}")
                        continue
                deleted += 1

        if deleted == 0:
            print("  ✨ No auto-pr branches found. Repo is clean!")
        else:
            action = "would be deleted" if dry_run else "deleted"
            print(f"\n🏁 {deleted} branch(es) {action}.")

        return deleted

    def check_rate_limit(self) -> dict:
        """Check GitHub API rate limit status.

        Returns:
            Dict with rate limit info.
        """
        rate = self.github.get_rate_limit()
        core = rate.core
        return {
            "remaining": core.remaining,
            "limit": core.limit,
            "reset": core.reset.strftime("%H:%M:%S"),
            "enough_for_run": core.remaining >= self.config.num_prs * 4,
        }

    # -- Internals ------------------------------------------------------------

    def _print_header(self) -> None:
        cfg = self.config
        mode = " [DRY RUN]" if cfg.dry_run else ""
        print(f"\nConfiguration: user='{cfg.github_username}' repo='{cfg.repo_name}'{mode}")
        print(f"Base branch: {cfg.base_branch}")
        print(f"Will create {cfg.num_prs} PR(s) with {cfg.delay_seconds}s delay.")
        print(f"Merge method: {cfg.merge_method}\n")

    def _dry_run_preview(self, index: int) -> None:
        """Preview what a PR would look like without creating anything."""
        branch_name = f"{self.BRANCH_PREFIX}{generate_random_string(6)}-{int(time.time())}"
        print(f"  📋 Would create branch: {branch_name}")
        print(f"  📝 Would commit to: README.md")
        print(f"  🔗 Would open PR #{index}: Auto-PR {generate_random_string(4)} #{index}")
        print(f"  🎉 Would merge via: {self.config.merge_method}")

    def _create_branch(self) -> str | None:
        """Create a new branch from the latest base commit. Returns branch name or None."""
        cfg = self.config
        base = self.repo.get_branch(cfg.base_branch)
        sha = base.commit.sha
        print(f"  Latest {cfg.base_branch} commit: {sha[:7]}")

        branch_name = f"{self.BRANCH_PREFIX}{generate_random_string(6)}-{int(time.time())}"
        try:
            self.repo.create_git_ref(f"refs/heads/{branch_name}", sha)
            print(f"  ✅ Created branch: {branch_name}")
            return branch_name
        except GithubException as e:
            print(f"  ❌ Failed to create branch: {e}")
            return None

    def _make_commit(self, branch_name: str) -> None:
        """Append a small change to README.md on the given branch."""
        try:
            contents = self.repo.get_contents("README.md", ref=branch_name)
            new_content = (
                f"{contents.decoded_content.decode()}\n"
                f"- 🤖 Auto-update by PullShark: {generate_random_string()}"
            )
            self.repo.update_file(
                contents.path,
                f"Automated update in {branch_name}",
                new_content,
                contents.sha,
                branch=branch_name,
            )
            print("  📝 Updated README.md")
        except GithubException:
            self.repo.create_file(
                "README.md",
                f"Create README in {branch_name}",
                f"# {self.config.repo_name}\n\nAuto-generated: {generate_random_string()}\n\n---\n🦈 PR Automation By [Shinei Nouzen](https://github.com/Shineii86/PullShark)",
                branch=branch_name,
            )
            print("  📄 Created README.md")

    def _open_pull_request(self, index: int, branch_name: str):
        """Create a pull request. Returns PullRequest or None."""
        try:
            pr = self.repo.create_pull(
                title=f"Auto-PR {generate_random_string(4)} #{index}",
                body=(
                    "🤖 Automated pull request for the Pull Shark achievement.\n\n"
                    "---\n🦈 PR Automation By [Shinei Nouzen](https://github.com/Shineii86)"
                ),
                head=branch_name,
                base=self.config.base_branch,
            )
            print(f"  🔗 Created PR: {pr.html_url}")
            return pr
        except GithubException as e:
            print(f"  ❌ Failed to create PR: {e}")
            return None

    def _print_summary(self, successful: int) -> None:
        total = self.config.num_prs
        mode = " (dry run)" if self.config.dry_run else ""
        print(f"\n🏁 Finished. {successful} out of {total} pull requests {'would be' if self.config.dry_run else ''} merged{mode}.")
        if not self.config.dry_run:
            if successful >= 2:
                print("🦈 Congratulations! You've met the requirements for Pull Shark!")
            else:
                print("⚠️  You need at least 2 merged PRs for the achievement.")
