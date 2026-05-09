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
- [Why Use This Method?](#-why-use-this-method)
- [Prerequisites](#-prerequisites)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
  - [Google Colab](#1️⃣-google-colab)
  - [Command Line (CLI)](#2️⃣-command-line-cli)
  - [As a Python Package](#3️⃣-as-a-python-package)
- [Configuration Options](#-configuration-options)
- [How It Works](#-how-it-works-technical-overview)
- [Troubleshooting](#-troubleshooting)
- [Changelog](#-changelog)
- [Credits & Acknowledgments](#-credits--acknowledgments)
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

The specific requirements for each tier are:

| Tier | Badge Name | Required Merged Pull Requests |
| :--- | :--- | :--- |
| 1 | **Default / x1** | **2** merged PRs |
| 2 | **Bronze / x2** | **16** merged PRs |
| 3 | **Silver / x3** | **128** merged PRs |
| 4 | **Gold / x4** | **1024** merged PRs |

> [!IMPORTANT]
> Only merged PRs count toward this achievement. PRs that are closed without being merged do not contribute to your progress.

---

## ✅ Why Use This Method?

| Feature                      | Benefit                                                                 |
|------------------------------|-------------------------------------------------------------------------|
| ☁️ **No PC Required**         | Runs entirely in Google Colab (cloud‑based). Works on any device with a browser. |
| 🖥️ **CLI Support**            | Run directly from your terminal — no browser needed.                     |
| 🔁 **Fully Automated**        | Creates branches, commits changes, opens PRs, and merges them automatically. |
| 🛡️ **Robust**                 | Handles GitHub's mergeability checks and branch‑update delays gracefully. |
| ⚙️ **Customizable**           | Choose how many PRs to create, target branch, delay, and retry count.    |
| 📦 **Modular Package**        | Clean Python package — import into your own scripts or use the CLI.      |

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
│   ├── config.py           # Configuration dataclass with validation
│   ├── core.py             # PullSharkBot — main automation logic
│   ├── utils.py            # Helpers (random strings, mergeability, retries)
│   └── cli.py              # Command-line interface entry point
├── notebooks/
│   └── PullShark.ipynb     # Google Colab notebook (thin wrapper)
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

Open the notebook, fill in the configuration form fields, and click **Runtime → Run all** (`Ctrl+F9`).

### 2️⃣ Command Line (CLI)

After installing with `pip install -e .`, use the `pullshark` command directly:

```bash
pullshark \
  --token ghp_your_token_here \
  --username YourUsername \
  --repo YourRepo \
  --prs 4 \
  --branch main \
  --delay 10 \
  --max-retries 3
```

#### CLI Arguments

| Flag | Short | Required | Default | Description |
|------|-------|:--------:|---------|-------------|
| `--token` | `-t` | ✅ | — | GitHub Personal Access Token |
| `--username` | `-u` | ✅ | — | Your GitHub username |
| `--repo` | `-r` | ✅ | — | Target repository name |
| `--prs` | `-n` | | `4` | Number of PRs to create |
| `--branch` | `-b` | | `main` | Base branch to target |
| `--delay` | `-d` | | `10` | Delay (seconds) between PRs |
| `--max-retries` | | | `3` | Max merge retry attempts |

#### CLI Output Example

```
Configuration: user='Shineii86' repo='PullShark'
Base branch: main
Will create 4 PR(s) with 10s delay.

--- 📦 Creating PR #1 of 4 ---
  Latest main commit: a1b2c3d
  ✅ Created branch: auto-pr-xyz123-1234567890
  📝 Updated README.md
  🔗 Created PR: https://github.com/Shineii86/PullShark/pull/178
  ⏳ Waiting for GitHub to calculate mergeability...
  🎉 Merged PR #178
  ⏸️  Pausing 10s for GitHub to process...

🏁 Finished. Successfully merged 4 out of 4 pull requests.
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
)

bot = PullSharkBot(config)
merged = bot.run()
print(f"Merged {merged} PRs")
```

---

## ⚙️ Configuration Options

| Parameter        | Default  | Description                                                                 |
|------------------|----------|-----------------------------------------------------------------------------|
| `num_prs`        | `4`      | Total number of pull requests to create and merge. Minimum `2` for the badge.|
| `base_branch`    | `"main"` | Target branch for PRs (e.g., `master`, `develop`).                           |
| `delay_seconds`  | `10`     | Wait time (in seconds) between PRs and between merge retries.                |
| `max_retries`    | `3`      | Number of times to retry a failed merge before stopping.                     |

### Advanced Customization

- **File Modified**: By default, the script updates or creates `README.md`. To change this, edit `_make_commit()` in `pullshark/core.py`.
- **Repository**: Use any repo you own or have write access to — just update the repo name.

---

## 🔬 How It Works (Technical Overview)

The script performs the following steps for **each** pull request:

1. **Fetch the latest commit SHA** from the specified `BASE_BRANCH` to ensure we branch from the most up‑to‑date state.  
2. **Create a new branch** with a unique name (e.g., `auto-pr-abc123-1234567890`).  
3. **Make a commit** on that branch — either appending a line to `README.md` or creating it if it doesn't exist.  
4. **Open a pull request** from the new branch to `BASE_BRANCH`.  
5. **Wait for GitHub's mergeability check** (polling the PR status every 3 seconds).  
6. **Merge the pull request** using the "merge" method (no squash, no rebase).  
7. **Pause for `DELAY_SECONDS`** to let GitHub fully update the base branch before starting the next iteration.

**Retry Logic**: If a merge fails (e.g., due to a temporary GitHub hiccup), the script will wait `DELAY_SECONDS` and retry up to `MAX_RETRIES` times before giving up.

This robust approach avoids:
- **405 Not Mergeable** errors caused by stale branch references.
- **Race conditions** when GitHub's backend hasn't finished processing a merge.

---

## 🆘 Troubleshooting

| Issue                                             | Solution                                                                                     |
|---------------------------------------------------|----------------------------------------------------------------------------------------------|
| `github.GithubException.BadCredentialsException`  | Your Personal Access Token is incorrect or expired. Generate a new one and update the form.   |
| `Pull Request is not mergeable: 405`              | Enable **Allow auto‑merge** in repo Settings → General → Pull Requests.                       |
| The script hangs at "Waiting for mergeability"    | The PR may have a conflict. Delete the branch manually and re‑run the script.                 |
| `RateLimitExceededException`                      | GitHub API rate limit hit. Wait an hour or increase `DELAY_SECONDS`.                          |
| No achievement after successful runs              | Wait a few minutes and refresh your profile. Achievement updates are not always instant.      |

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
