# 🕵️‍♂️ TryHackMe Streak Automation

This project automates **TryHackMe** activity to maintain your daily streak and log profile progress.  
It can be run **locally** or via **GitHub Actions**, with notifications sent to **Telegram**, **Discord**, and **Slack**.

---

## ✨ Features
- 🔄 Resets the **tutorial room** automatically.
- 🚀 Submits a predefined flag (`flag{connection_verified}`).
- 📊 Fetches profile stats (username, level, rank, streak, awards, rooms completed).
- 📝 Saves results into `streak.txt`.
- 📢 Sends updates to Telegram, Discord, and Slack when run via GitHub Actions.

---

## ⚙️ Requirements
- Python 3.8+
- [Playwright](https://playwright.dev/python/)
- `requests`
- `beautifulsoup4`

Install dependencies:
```bash
pip install -r requirements.txt
playwright install chromium
```

---

## 🔑 Setup (Local Usage)

1. **Generate Cookies**
   - Run the cookie grabber script:
     ```bash
     python cookies.py
     ```
   - A Chromium browser will open → log in to TryHackMe manually (within 2 minutes).
   - After login, cookies are saved to:
     ```
     cookies/tryhackme_cookies.txt
     ```
     This file contains your cookies as a **base64 string**.
   - ⚠️ **Important:** TryHackMe cookies typically expire after **7 days**.  
     You will need to regenerate and update them **weekly** to keep the bot working.

2. **Set your TryHackMe User ID**
   - Get your **public user ID** from your TryHackMe profile URL which will be in your TryHackMe badge.  
     Example: `https://tryhackme.com/p/your_user_id`
   - Export it as an environment variable:
     ```bash
     export TRYHACKME_USER_ID=your_user_id
     ```
     (On Windows PowerShell: `setx TRYHACKME_USER_ID "your_user_id"`)

3. **Run the main script**
   ```bash
   python thm.py
   ```

---

## ⚡ GitHub Actions Automation

This repo includes a workflow (`.github/workflows/tryhackme.yml`) that:
- Runs **daily at midnight UTC** (via cron).
- Resets the tutorial room, submits the flag, fetches stats.
- Sends notifications to **Telegram, Discord, and Slack**.

### 🔐 Required Secrets
Add these in **Repo → Settings → Secrets and variables → Actions**:

- `COOKIES_PKL` → Content of `cookies/tryhackme_cookies.txt` (base64 string).
- `TRYHACKME_USER_ID` → Your public TryHackMe user ID.
- `TELEGRAM_BOT_TOKEN` → Telegram bot API token.
- `TELEGRAM_CHAT_ID` → Your Telegram chat/group ID.
- `DISCORD_WEBHOOK_URL` → Discord webhook URL.
- `SLACK_WEBHOOK_URL` → Slack webhook URL.

### ⚠️ Cookie Refresh
Since cookies expire every ~7 days:
1. Run `python get_cookies.py` locally again.
2. Copy the new base64 string from `cookies/tryhackme_cookies.txt`.
3. Update the `COOKIES_PKL` secret in GitHub.

### ▶️ Manual Run
You can also trigger the workflow manually from **Actions tab → Daily TryHackMe Automation → Run workflow**.

---

## 📂 Example Output (`streak.txt`)
```
👤 Username: Zephyr1
 ⚡ Level: [0xF]
🏆 Rank: 2146
🔥 Streak: 154 days
🎖️ Awards: 38
🚪 Rooms Completed: 380
✅ Done!
```

---

## 📌 Notes
- Local runs are useful for testing/debugging.  
- GitHub Actions ensures your streak is safe even if your computer is offline.  
- Cookies must be **regenerated weekly** to keep the automation working.  
- Notifications keep you updated in real-time across platforms.

---

🚀 **Stay consistent, keep your streak alive, and track your progress effortlessly!**
