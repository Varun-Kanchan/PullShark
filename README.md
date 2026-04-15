<div align="center">

[![Pull Shark Automator Banner](https://raw.githubusercontent.com/Shineii86/PullShark/refs/heads/main/images/PullShark.png)](https://github.com/Shineii86/PullShark)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Shineii86/PullShark/blob/main/notebooks/PullShark.ipynb)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[![GitHub Stars](https://img.shields.io/github/stars/Shineii86/PullShark?style=for-the-badge)](https://github.com/Shineii86/PullShark/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/Shineii86/PullShark?style=for-the-badge)](https://github.com/Shineii86/PullShark/fork)

A **fully automated** Python script that runs in **Google Colab** to create and merge multiple pull requests in your GitHub repository — helping you earn the coveted **Pull Shark** achievement.

</div>

---

## 📖 Table of Contents

- [What is Pull Shark?](#-what-is-pull-shark)
- [Why Use This Method?](#-why-use-this-method)
- [Prerequisites](#-prerequisites)
- [Step-by-Step Guide](#-step-by-step-guide)
- [Customization](#-customization)
- [How It Works (Technical Overview)](#-how-it-works-technical-overview)
- [Troubleshooting](#-troubleshooting)
- [Credits & Acknowledgments](#-credits--acknowledgments)
- [License & Disclaimer](#-license--disclaimer)

---

## 🎯 What is Pull Shark?

**Pull Shark** is a GitHub achievement awarded when you have **at least 2 pull requests merged** into any repository. It's one of the most popular achievements and a fun way to show off your open-source contributions.

This script automates the creation and merging of pull requests, so you can unlock the achievement in **under 5 minutes** — entirely from your browser.


| Base | Bronze | Silver | Gold |
| :--: | :----: | :----: | :--: |
| [![Base](https://github.com/Shineii86/PullShark/blob/main/images/pull-shark-default.png)](https://github.com/Shineii86/PullShark) | [![Bronze](https://github.com/Shineii86/PullShark/blob/main/images/pull-shark-bronze.png)](https://github.com/Shineii86/PullShark) | [![Sliver](https://github.com/Shineii86/PullShark/blob/main/images/pull-shark-silver.png)](https://github.com/Shineii86/PullShark) | [![Gold](https://github.com/Shineii86/PullShark/blob/main/images/pull-shark-gold.png)](https://github.com/Shineii86/PullShark) |


---

## ✅ Why Use This Method?

| Feature                      | Benefit                                                                 |
|------------------------------|-------------------------------------------------------------------------|
| ☁️ **No PC Required**         | Runs entirely in Google Colab (cloud‑based). Works on any device with a browser. |
| 🔁 **Fully Automated**        | Creates branches, commits changes, opens PRs, and merges them automatically. |
| 🛡️ **Robust**                 | Handles GitHub's mergeability checks and branch‑update delays gracefully. |
| ⚙️ **Customizable**           | Choose how many PRs to create, which repo to use, and more.              |
| 📦 **Minimal Dependencies**   | Only uses the official `PyGithub` library.                               |

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
5. Click **Generate token** and **copy the token immediately** — you won’t see it again.

---

## 📥 **How to Deploy**

### 1️⃣ **One‑Click Colab**

<a href="https://colab.research.google.com/github/Shineii86/LeechBot/blob/main/notebooks/PullShark.ipynb">
  <img src="https://user-images.githubusercontent.com/125879861/255389999-a0d261cf-893a-46a7-9a3d-2bb52811b997.png" alt="Open In Colab" width="200px">
</a>

### 2️⃣ Configure Your Credentials

In the script, replace the placeholders:

| Variable            | Example Value           |
|---------------------|-------------------------|
| `GITHUB_USERNAME`   | `"Shineii86"`           |
| `GITHUB_TOKEN`      | `"ghp_abc123..."`       |
| `REPO_NAME`         | `"PullShark"`           |
| `NUM_PRS`           | `4` (or any number ≥2)  |

### 3️⃣ Run the Script

Click the **▶️ Run** button on the left side of the cell or press `Shift + Enter`. The script will install dependencies and begin creating and merging pull requests.

You'll see real‑time output like:

```
--- 📦 Creating PR #1 of 4 ---
Latest main commit: a1b2c3d
✅ Created branch: auto-pr-xyz123-1234567890
📝 Updated README.md
🔗 Created PR: https://github.com/Shineii86/PullShark/pull/178
⏳ Waiting for GitHub to calculate mergeability...
🎉 Merged PR #178
⏸️ Pausing 10 seconds...
...
🏁 Finished. Successfully merged 4 out of 4 pull requests.
🦈 Congratulations! You've met the requirements for Pull Shark!
```

### 4️⃣ Verify the Achievement

1. Go to your GitHub profile (`https://github.com/YOUR_USERNAME`).
2. Look for the **Pull Shark** badge in the achievements section.  
   *Note: It may take a few minutes for GitHub to update.*

---

## ⚙️ Customization

### Number of Pull Requests

Change the `NUM_PRS` variable to any integer (minimum `2` for the achievement).  
```python
NUM_PRS = 5   # Creates 5 merged PRs
```

### Target Repository

Use any repository you own or have write access to.  
```python
REPO_NAME = "my-awesome-project"
```

### File Modified

By default, the script updates or creates `README.md`. To change the file:

- Locate the line `repo.get_contents("README.md", ...)` and replace `"README.md"` with any filename (e.g., `"CHANGELOG.md"`).

### Delay Between PRs

The script includes a 10‑second pause after each merge. You can adjust this by modifying `time.sleep(10)` to a different value (in seconds).

---

## 🔬 How It Works (Technical Overview)

The script performs the following steps for **each** pull request:

1. **Fetch the latest commit SHA** from the `main` branch to ensure we branch from the most up‑to‑date state.  
2. **Create a new branch** with a unique name (e.g., `auto-pr-abc123-1234567890`).  
3. **Make a commit** on that branch — either by appending a line to `README.md` or creating it if it doesn’t exist.  
4. **Open a pull request** from the new branch to `main`.  
5. **Wait for GitHub’s mergeability check** (polling the PR status every 3 seconds).  
6. **Merge the pull request** using the “merge” method (no squash, no rebase).  
7. **Pause for 10 seconds** to let GitHub fully update the `main` branch before starting the next iteration.

This approach avoids common pitfalls like:
- **405 Not Mergeable** errors caused by stale branch references.
- **Race conditions** when GitHub’s backend hasn’t finished processing a merge.

---

## 🆘 Troubleshooting

| Issue                                           | Solution                                                                                     |
|-------------------------------------------------|----------------------------------------------------------------------------------------------|
| `github.GithubException.BadCredentialsException` | Your Personal Access Token is incorrect or expired. Generate a new one and update the script. |
| `Pull Request is not mergeable: 405`            | Ensure **Allow auto‑merge** is enabled in the repository settings (Settings → General → Pull Requests). |
| The script hangs at "Waiting for mergeability"  | The PR may have a conflict. Delete the branch manually and re‑run the script.                 |
| `RateLimitExceededException`                    | GitHub API rate limit hit. Wait an hour or use a token with higher limits (unlikely for 4 PRs). |
| No achievement after successful runs             | Wait a few minutes and refresh your profile. Achievement updates are not always instant.      |


---

## 📄 License & Disclaimer

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

> [!WARNING]
> This script is intended for educational purposes and to help users unlock a harmless GitHub achievement. Please use responsibly and do not abuse automation to spam repositories. The author is not responsible for any consequences arising from misuse of this tool.

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
