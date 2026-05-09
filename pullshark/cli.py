"""
Command-line interface for PullShark.

Usage:
    pullshark --token ghp_xxx --repo myrepo
    pullshark --token ghp_xxx --repo myrepo --prs 6 --delay 15
"""

import argparse
import sys

from pullshark.config import Config
from pullshark.core import PullSharkBot


def parse_args(argv: list[str] | None = None) -> Config:
    """Parse CLI arguments into a Config object."""
    parser = argparse.ArgumentParser(
        prog="pullshark",
        description="🦈 GitHub Pull Shark Achievement Automator — create and merge PRs automatically.",
    )
    parser.add_argument(
        "-t", "--token",
        required=True,
        help="GitHub Personal Access Token (with repo scope).",
    )
    parser.add_argument(
        "-r", "--repo",
        required=True,
        help="Target repository name (must exist under your account).",
    )
    parser.add_argument(
        "-u", "--username",
        required=True,
        help="Your GitHub username.",
    )
    parser.add_argument(
        "-n", "--prs",
        type=int,
        default=4,
        help="Number of PRs to create (default: 4, min 2 for achievement).",
    )
    parser.add_argument(
        "-b", "--branch",
        default="main",
        help="Base branch to target (default: main).",
    )
    parser.add_argument(
        "-d", "--delay",
        type=int,
        default=10,
        help="Delay in seconds between PRs (default: 10).",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=3,
        help="Maximum merge retry attempts (default: 3).",
    )

    args = parser.parse_args(argv)

    return Config(
        github_username=args.username,
        github_token=args.token,
        repo_name=args.repo,
        num_prs=args.prs,
        base_branch=args.branch,
        delay_seconds=args.delay,
        max_retries=args.max_retries,
    )


def main(argv: list[str] | None = None) -> None:
    """CLI entry point."""
    config = parse_args(argv)

    errors = config.validate()
    if errors:
        for err in errors:
            print(f"❌ {err}", file=sys.stderr)
        sys.exit(1)

    bot = PullSharkBot(config)
    successful = bot.run()
    sys.exit(0 if successful >= 2 else 1)


if __name__ == "__main__":
    main()
