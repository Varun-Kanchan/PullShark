"""
Command-line interface for PullShark.

Usage:
    pullshark run --token ghp_xxx --repo myrepo
    pullshark run --token ghp_xxx --repo myrepo --dry-run --log run.log --output report.json
    pullshark clean --token ghp_xxx --repo myrepo
"""

import argparse
import logging
import sys

from pullshark.config import Config
from pullshark.core import PullSharkBot


def _setup_logging(log_file: str = "") -> None:
    """Configure logging for the pullshark package."""
    logger = logging.getLogger("pullshark")
    logger.setLevel(logging.DEBUG)

    # Console handler — only warnings and above to stdout
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.WARNING)
    console.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(console)

    # File handler — everything if a log file is specified
    if log_file:
        fh = logging.FileHandler(log_file, mode="a", encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        )
        logger.addHandler(fh)


def _add_common_args(parser: argparse.ArgumentParser) -> None:
    """Add arguments shared by all subcommands."""
    parser.add_argument("-t", "--token", required=True, help="GitHub Personal Access Token (with repo scope).")
    parser.add_argument("-r", "--repo", required=True, help="Target repository name.")
    parser.add_argument("-u", "--username", required=True, help="Your GitHub username.")


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser with subcommands."""
    parser = argparse.ArgumentParser(
        prog="pullshark",
        description="🦈 GitHub Pull Shark Achievement Automator — create and merge PRs automatically.",
    )
    sub = parser.add_subparsers(dest="command", help="Command to run")

    # --- run ---
    run_parser = sub.add_parser("run", help="Create and merge pull requests.")
    _add_common_args(run_parser)
    run_parser.add_argument("-n", "--prs", type=int, default=4, help="Number of PRs to create (default: 4).")
    run_parser.add_argument("-b", "--branch", default="main", help="Base branch to target (default: main).")
    run_parser.add_argument("-d", "--delay", type=int, default=10, help="Delay in seconds between PRs (default: 10).")
    run_parser.add_argument("--max-retries", type=int, default=3, help="Maximum merge retry attempts (default: 3).")
    run_parser.add_argument("--merge-method", choices=["merge", "squash", "rebase"], default="merge", help="Merge strategy (default: merge).")
    run_parser.add_argument("--prefix", default="auto-pr", help="Branch name prefix (default: auto-pr).")
    run_parser.add_argument("--dry-run", action="store_true", help="Preview what would happen without making changes.")
    run_parser.add_argument("--check-rate", action="store_true", help="Check API rate limit before running.")
    run_parser.add_argument("--log", default="", metavar="FILE", help="Save detailed logs to a file.")
    run_parser.add_argument("--output", default="", metavar="FILE", help="Save run report as JSON.")

    # --- clean ---
    clean_parser = sub.add_parser("clean", help="Delete auto-created branches from the repo.")
    _add_common_args(clean_parser)
    clean_parser.add_argument("--prefix", default="auto-pr", help="Branch prefix to clean (default: auto-pr).")
    clean_parser.add_argument("--dry-run", action="store_true", help="Show branches that would be deleted without deleting them.")
    clean_parser.add_argument("--log", default="", metavar="FILE", help="Save detailed logs to a file.")

    return parser


def _run(args: argparse.Namespace) -> None:
    """Handle the 'run' command."""
    _setup_logging(args.log)
    logger = logging.getLogger("pullshark")
    logger.info("Starting PullShark run command")

    config = Config(
        github_username=args.username,
        github_token=args.token,
        repo_name=args.repo,
        num_prs=args.prs,
        base_branch=args.branch,
        delay_seconds=args.delay,
        max_retries=args.max_retries,
        dry_run=args.dry_run,
        merge_method=args.merge_method,
        branch_prefix=args.prefix,
        log_file=args.log,
        output_file=args.output,
    )

    errors = config.validate()
    if errors:
        for err in errors:
            print(f"❌ {err}", file=sys.stderr)
        sys.exit(1)

    bot = PullSharkBot(config)

    if args.check_rate:
        info = bot.check_rate_limit()
        print(f"📊 API Rate Limit: {info['remaining']}/{info['limit']} remaining (resets {info['reset']})")
        if not info["enough_for_run"]:
            print(f"⚠️  May not have enough calls for {config.num_prs} PRs. Consider waiting.\n")
        else:
            print("✅ Enough API calls available.\n")

    successful = bot.run()
    logger.info("Run complete: %d/%d merged", successful, config.num_prs)
    sys.exit(0 if successful >= 2 else 1)


def _clean(args: argparse.Namespace) -> None:
    """Handle the 'clean' command."""
    _setup_logging(args.log)

    config = Config(
        github_username=args.username,
        github_token=args.token,
        repo_name=args.repo,
        branch_prefix=args.prefix,
    )

    bot = PullSharkBot(config)
    bot.clean(dry_run=args.dry_run)


def main(argv: list[str] | None = None) -> None:
    """CLI entry point."""
    parser = build_parser()

    if argv is None:
        argv = sys.argv[1:]

    # Default to 'run' if no subcommand given
    if len(argv) > 0 and argv[0] not in ("run", "clean", "--help", "-h"):
        argv = ["run"] + argv

    args = parser.parse_args(argv)

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    if args.command == "run":
        _run(args)
    elif args.command == "clean":
        _clean(args)


if __name__ == "__main__":
    main()
