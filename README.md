<div align="center">

[![Pull Shark Automator Banner](https://raw.githubusercontent.com/Shineii86/PullShark/refs/heads/main/images/PullShark.png)](https://github.com/Shineii86/PullShark)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shineii86/PullShark/blob/main/notebooks/PullShark.ipynb)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![GitHub Stars](https://img.shields.io/github/stars/Shineii86/PullShark?style=for-the-badge)](https://github.com/Shineii86/PullShark/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/Shineii86/PullShark?style=for-the-badge)](https://github.com/Shineii86/PullShark/fork)

A **fully automated** Python tool that creates and merges multiple pull requests in your GitHub repository — helping you earn the coveted **Pull Shark** achievement. Runs in **Google Colab** or directly from your **terminal**.

</div>

---

> [!WARNING]
> **This script creates real pull requests on your GitHub account.**
> - Never share your **Personal Access Token** – treat it like a password.
> - Use a **dedicated repository** to avoid cluttering important projects.
> - GitHub may rate‑limit excessive API calls; the built‑in delay helps prevent this.

---

## 📖 Table of Contents

- [What is Pull Shark?](#-what-is-pull-shark)
- [Features](#-features)
- [Prerequisites](#-prerequisites)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
  - [Google Colab](#1️⃣-google-colab)
  - [Command Line (CLI)](#2️⃣-command-line-cli)
  - [As a Python Package](#3️⃣-as-a-python-package)
- [Configuration Options](#-configuration-options)
- [How It Works](#-how-it-works-technical-overview)
- [Merge Methods](#-merge-methods)
- [Troubleshooting](#-troubleshooting)
- [Changelog](#-changelog)
- [License & Disclaimer](#-license--disclaimer)

---

## 🎯 What is Pull Shark?

**Pull Shark** is a GitHub achievement awarded when you have **at least 2 pull requests merged** into any repository. It's one of the most popular achievements and a fun way to show off your open-source contributions.

This script automates the creation and merging of pull requests, so you can unlock the achievement in **under 5 minutes** — from your browser or terminal.

| Base | Bronze | Silver | Gold |
| :--: | :----: | :----: | :--: |
| [![Base](https://github.com/Shineii86/PullShark/blob/main/images/pull-shark-default.png)](https://github.com/Shineii86/PullShark) | [![Bronze](https://github.com/Shineii86/PullShark/blob/main/images/pull-shark-bronze.png)](https://github.com/Shineii86/PullShark) | [![Silver](https://github.com/Shineii86/PullShark/blob/main/images/pull-shark-silver.png)](https://github.com/Shineii86/PullShark) | [![Gold](https://github.com/Shineii86/PullShark/blob/main/images/pull-shark-gold.png)](https://github.com/Shineii86/PullShark) |


> To earn the "**Pull Shark**" achievement on GitHub, you need to have your pull requests (PRs) merged. The badge has four tiers, each requiring a specific number of merged PRs.

### 🦈 Pull Shark Achievement Tiers

| Tier | Badge Name | Required Merged Pull Requests |
| :--- | :--- | :--- |
| 1 | **Default / x1** | **2** merged PRs |
| 2 | **Bronze / x2** | **16** merged PRs |
| 3 | **Silver / x3** | **128** merged PRs |
| 4 | **Gold / x4** | **1024** merged PRs |

> [!IMPORTANT]
> Only merged PRs count toward this achievement. PRs that are closed without being merged do not contribute to your progress.

---

## ✨ Features

| Feature | Description |
|:--------|:------------|
| ☁️ **Google Colab** | One-click notebook with 5-step guided flow — no install needed |
| 🖥️ **CLI** | Full terminal interface with `run` and `clean` subcommands |
| 🔍 **Dry Run** | Preview branches, commits, and PRs without making any changes |
| 🧹 **Branch Cleanup** | Bulk-delete all `auto-pr-*` branches after a run |
| 📊 **Rate Limit Check** | View your API quota before starting — prevents mid-run failures |
| 🔀 **Merge Strategies** | Choose between `merge`, `squash`, or `rebase` methods |
| 🔄 **Retry Logic** | Automatically retries failed merges with configurable attempts |
| 📦 **Python Package** | Import into your own scripts for custom workflows |
| 🐍 **`python -m`** | Run as `python -m pullshark` without installing |
| ✅ **Validation** | Catches config errors before making any API calls |

---

## 🧰 Prerequisites

Before you begin, make sure you have:

1. **A GitHub account** — obviously 😄  
2. **A repository** where you have **write access** (you can create a new one just for this).  
3. **A GitHub Personal Access Token (Classic)** with `repo` scope.

### 🔐 How to Get a Personal Access Token

1. Go to **Settings** → **Developer settings** → **Personal access tokens** → **Tokens (classic)**.
2. Click **Generate new token (classic)**.
3. Give it a name (e.g., `Pull Shark Bot`).
4. Under **Select scopes**, check **`repo`** (this grants full control of private repositories as well).
5. Click **Generate token** and **copy the token immediately** — you won't see it again.

---

## 📁 Project Structure

```
PullShark/
├── pullshark/              # Python package
│   ├── __init__.py         # Package init & version
│   ├── __main__.py         # python -m pullshark support
│   ├── config.py           # Configuration dataclass with validation
│   ├── core.py             # PullSharkBot — main automation logic
│   ├── utils.py            # Helpers (random strings, mergeability, retries)
│   └── cli.py              # Command-line interface (run & clean subcommands)
├── notebooks/
│   └── PullShark.ipynb     # Google Colab notebook (5-step guided flow)
├── images/                 # Achievement badge images
├── pyproject.toml          # Modern Python packaging config
├── requirements.txt        # Dependencies
├── CHANGELOG.md            # Version history
├── LICENSE                 # MIT License
└── README.md               # This file
```

---

## 📥 Installation

### From Source (Recommended)

```bash
git clone https://github.com/Shineii86/PullShark.git
cd PullShark
pip install -e .
```

This installs the `pullshark` CLI command and makes the package importable.

### Dependencies Only

```bash
pip install PyGithub>=2.1.0
```

---

## 🚀 Usage

### 1️⃣ Google Colab

<a href="https://colab.research.google.com/github/Shineii86/PullShark/blob/main/notebooks/PullShark.ipynb">
  <img src="https://user-images.githubusercontent.com/125879861/255389999-a0d261cf-893a-46a7-9a3d-2bb52811b997.png" alt="Open In Colab" width="200px">
</a>

The notebook walks you through **5 steps**:

| Step | Name | What it does |
|:----:|:-----|:-------------|
| 1 | 📦 **Install & Load** | Installs PyGithub and loads the package |
| 2 | 🔌 **Test Connection** | Validates token, repo access, write permissions, API rate limit, and existing branches |
| 3 | 🔍 **Dry Run** | Preview what the bot will do — no changes made |
| 4 | 🚀 **Run for Real** | Create and merge PRs with full configuration |
| 5 | 🧹 **Cleanup** | Delete all `auto-pr-*` branches (with dry-run safety) |

> 💡 **Tip:** Start with Step 3 (Dry Run) to preview before committing to a real run.

### 2️⃣ Command Line (CLI)

After installing with `pip install -e .`, use the `pullshark` command:

```bash
# Create and merge PRs
pullshark run --token ghp_xxx --username YourUsername --repo YourRepo --prs 4

# Preview what would happen (no changes made)
pullshark run --token ghp_xxx --username YourUsername --repo YourRepo --dry-run

# Check API quota first
pullshark run --token ghp_xxx --username YourUsername --repo YourRepo --check-rate

# Use squash merge instead of regular merge
pullshark run --token ghp_xxx --username YourUsername --repo YourRepo --merge-method squash

# Clean up auto-created branches
pullshark clean --token ghp_xxx --username YourUsername --repo YourRepo

# Preview cleanup without deleting
pullshark clean --token ghp_xxx --username YourUsername --repo YourRepo --dry-run

# Run without installing
python -m pullshark run --token ghp_xxx --username YourUsername --repo YourRepo
```

> 💡 The `run` subcommand is optional — `pullshark --token ... --repo ...` still works as a shortcut.

#### CLI Arguments — `run`

| Flag | Short | Required | Default | Description |
|------|-------|:--------:|---------|-------------|
| `--token` | `-t` | ✅ | — | GitHub Personal Access Token |
| `--username` | `-u` | ✅ | — | Your GitHub username |
| `--repo` | `-r` | ✅ | — | Target repository name |
| `--prs` | `-n` | | `4` | Number of PRs to create |
| `--branch` | `-b` | | `main` | Base branch to target |
| `--delay` | `-d` | | `10` | Delay (seconds) between PRs |
| `--max-retries` | | | `3` | Max merge retry attempts |
| `--merge-method` | | | `merge` | Merge strategy: `merge`, `squash`, `rebase` |
| `--dry-run` | | | off | Preview mode — no changes made |
| `--check-rate` | | | off | Show API quota before running |

#### CLI Arguments — `clean`

| Flag | Short | Required | Description |
|------|-------|:--------:|-------------|
| `--token` | `-t` | ✅ | GitHub Personal Access Token |
| `--username` | `-u` | ✅ | Your GitHub username |
| `--repo` | `-r` | ✅ | Target repository name |
| `--dry-run` | | | Show branches that would be deleted without deleting |

#### CLI Output Example

```
Configuration: user='Shineii86' repo='PullShark'
Base branch: main
Will create 4 PR(s) with 10s delay.
Merge method: merge

--- 📦 PR #1 of 4 ---
  Latest main commit: a1b2c3d
  ✅ Created branch: auto-pr-xyz123-1234567890
  📝 Updated README.md
  🔗 Created PR: https://github.com/Shineii86/PullShark/pull/178
  ⏳ Waiting for GitHub to calculate mergeability...
  🎉 Merged PR #178
  ⏸️  Pausing 10s for GitHub to process...

🏁 Finished. 4 out of 4 pull requests merged.
🦈 Congratulations! You've met the requirements for Pull Shark!
```

### 3️⃣ As a Python Package

Import the bot into your own scripts for custom workflows:

```python
from pullshark.config import Config
from pullshark.core import PullSharkBot

config = Config(
    github_username="YourUsername",
    github_token="ghp_xxx",
    repo_name="YourRepo",
    num_prs=6,
    delay_seconds=15,
    merge_method="squash",  # or "merge", "rebase"
)

bot = PullSharkBot(config)
merged = bot.run()
print(f"Merged {merged} PRs")

# Clean up branches when done
bot.clean()
```

---

## ⚙️ Configuration Options

| Parameter | Default | Description |
|:----------|:--------|:------------|
| `num_prs` | `4` | Total number of pull requests to create and merge. Minimum `2` for the badge. |
| `base_branch` | `"main"` | Target branch for PRs (e.g., `master`, `develop`). |
| `delay_seconds` | `10` | Wait time (in seconds) between PRs and between merge retries. |
| `max_retries` | `3` | Number of times to retry a failed merge before stopping. |
| `merge_method` | `"merge"` | Merge strategy: `"merge"`, `"squash"`, or `"rebase"`. |
| `dry_run` | `False` | If `True`, previews actions without making changes. |

### Advanced Customization

- **File Modified**: By default, the script updates or creates `README.md`. To change this, edit `_make_commit()` in `pullshark/core.py`.
- **Repository**: Use any repo you own or have write access to — just update the repo name.

---

## 🔬 How It Works (Technical Overview)

The script performs the following steps for **each** pull request:

1. **Fetch the latest commit SHA** from the specified base branch to ensure we branch from the most up‑to‑date state.  
2. **Create a new branch** with a unique name (e.g., `auto-pr-abc123-1234567890`).  
3. **Make a commit** on that branch — either appending a line to `README.md` or creating it if it doesn't exist.  
4. **Open a pull request** from the new branch to the base branch.  
5. **Wait for GitHub's mergeability check** (polling the PR status every 3 seconds).  
6. **Merge the pull request** using the configured merge method.  
7. **Pause for `DELAY_SECONDS`** to let GitHub fully update the base branch before starting the next iteration.

**Retry Logic**: If a merge fails (e.g., due to a temporary GitHub hiccup), the script will wait `DELAY_SECONDS` and retry up to `MAX_RETRIES` times before giving up.

**Rate Limit Check**: With `--check-rate`, the bot inspects your remaining API quota before starting. Each PR cycle uses ~4 API calls, so the bot estimates whether you have enough.

---

## 🔀 Merge Methods

PullShark supports three merge strategies. Choose based on your preference:

| Method | Flag | What It Does | History |
|:-------|:-----|:-------------|:--------|
| **Merge** | `--merge-method merge` | Creates a merge commit joining the branch to base | Preserves all commits |
| **Squash** | `--merge-method squash` | Combines all branch commits into a single commit | Clean, linear history |
| **Rebase** | `--merge-method rebase` | Replays branch commits on top of base | Linear, no merge commit |

> 💡 For Pull Shark achievement purposes, all three methods count equally. Use `squash` for cleaner history.

---

## 🆘 Troubleshooting

| Issue | Solution |
|:------|:---------|
| `BadCredentialsException` | Token is wrong or expired. Generate a new one with `repo` scope. |
| `405 Not mergeable` | Enable **Allow auto-merge** in repo Settings → General → Pull Requests. |
| Hangs at "Waiting for mergeability" | PR may have a conflict. Delete the branch manually and retry. |
| `RateLimitExceededException` | Wait an hour or increase `DELAY_SECONDS`. Use `--check-rate` to check beforehand. |
| No badge after success | Wait a few minutes and refresh your profile. Achievement updates are not always instant. |
| Leftover branches | Run `pullshark clean` to delete all `auto-pr-*` branches. |

---

## 📋 Changelog

See [CHANGELOG.md](CHANGELOG.md) for a full history of changes.

---

## 📄 License & Disclaimer

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

> [!WARNING]
> **This script is intended for educational purposes and to help users unlock a harmless GitHub achievement**. Please use responsibly and do not abuse automation to spam repositories. The author is not responsible for any consequences arising from misuse of this tool.

---

### 🔗 Quick Links

- [Google Colab](https://colab.research.google.com/)
- [GitHub Personal Access Tokens](https://github.com/settings/tokens)    
- [Pull Shark Achievement Details](https://github.com/Schweinepriester/github-profile-achievements#pull-shark-)

---

## 💕 Loved My Work?

🚨 [Follow me on GitHub](https://github.com/Shineii86)

⭐ [Give a star to this project](https://github.com/Shineii86/PullShark)

<div align="center">

<a href="https://github.com/Shineii86/PullShark">
<img src="https://github.com/Shineii86/AniPay/blob/main/Source/Banner6.png" alt="Banner">
</a>
  
  *For inquiries or collaborations*
     
[![Telegram Badge](https://img.shields.io/badge/-Telegram-2CA5E0?style=flat&logo=Telegram&logoColor=white)](https://telegram.me/Shineii86 "Contact on Telegram")
[![Instagram Badge](https://img.shields.io/badge/-Instagram-C13584?style=flat&logo=Instagram&logoColor=white)](https://instagram.com/ikx7.a "Follow on Instagram")
[![Pinterest Badge](https://img.shields.io/badge/-Pinterest-E60023?style=flat&logo=Pinterest&logoColor=white)](https://pinterest.com/ikx7a "Follow on Pinterest")
[![Gmail Badge](https://img.shields.io/badge/-Gmail-D14836?style=flat&logo=Gmail&logoColor=white)](mailto:ikx7a@hotmail.com "Send an Email")

  <sup><b>Copyright © 2026 <a href="https://telegram.me/Shineii86">Shinei Nouzen</a> All Rights Reserved</b></sup>

![Last Commit](https://img.shields.io/github/last-commit/Shineii86/PullShark?style=for-the-badge)

</div>
