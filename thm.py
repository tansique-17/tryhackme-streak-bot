import os
import requests
from bs4 import BeautifulSoup
import pickle
import time
from playwright.sync_api import sync_playwright

# === CONFIGURATION ===
COOKIE_FILE = "tryhackme_cookies.pkl"
ROOM_URL = "https://tryhackme.com/room/tutorial"
ANSWER = "flag{connection_verified}"
PROFILE_URL = "https://tryhackme.com/api/v2/badges/public-profile?userPublicId=1282671"

# === Handle Emoji-safe Logging ===
IS_GITHUB = os.environ.get("GITHUB_ACTIONS") == "true"

def log(msg):
    if IS_GITHUB:
        import re
        msg = re.sub(r'[^\x00-\x7F]+', '', msg)  # remove emojis
    print(msg)

# === Automate Room Reset & Flag Submission ===
def automate_tryhackme():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        log("🌐 Opening TryHackMe...")
        page.goto("https://tryhackme.com", wait_until="domcontentloaded", timeout=60000)

        log("🍪 Loading cookies...")
        try:
            with open(COOKIE_FILE, "rb") as f:
                cookies = pickle.load(f)
                context.add_cookies(cookies)
        except Exception as e:
            log(f"⚠️ Error loading cookies: {e}")

        log("🚪 Opening the tutorial room...")
        page.goto(ROOM_URL, timeout=60000)
        time.sleep(10)

        try:
            page.click("button:has-text('Options')")
            time.sleep(2)
            page.click("text=Reset Progress")
            time.sleep(2)
            page.click("button:has-text('Yes')")
            log("♻️ Room reset confirmed!")
            time.sleep(5)
        except Exception as e:
            log(f"⚠️ Could not reset room: {e}")

        try:
            input_field = page.locator("input[data-testid='answer-field']")
            input_field.wait_for(timeout=10000)
            input_field.click()
            input_field.fill(ANSWER)
            log("✏️ Answer entered.")
            time.sleep(2)
            page.click("button:has-text('Submit')")
            log("🚀 Answer submitted!")
            time.sleep(5)
        except Exception as e:
            log(f"⚠️ Error submitting flag: {e}")

        log("🛑 Closing browser...")
        browser.close()

# === Fetch and Print Profile Info ===
def fetch_profile_details():
    try:
        res = requests.get(PROFILE_URL, timeout=10)
        json_data = res.json()

        username = json_data.get("userName", "Unknown")
        rank = json_data.get("rank", {}).get("rankTitle", "Unknown")
        trophies = json_data.get("trophies", 0)
        streak = json_data.get("badgeStreak", {}).get("length", 0)
        awards = json_data.get("awards", 0)
        rooms_completed = json_data.get("completedRooms", 0)

        log("\n🧾 TryHackMe Profile Summary:")
        log(f"👤 Username: {username}")
        log(f"🏅 Rank: {rank}")
        log(f"🥇 Trophies: {trophies}")
        log(f"🔥 Streak: {streak}")
        log(f"🎖️ Awards: {awards}")
        log(f"🚪 Rooms Completed: {rooms_completed}")

        with open("streak.txt", "w") as f:
            f.write(str(streak))
        log(f"\n💾 Streak count saved: {streak}")

    except Exception as e:
        log(f"⚠️ Error fetching profile info: {e}")

# === MAIN ===
if __name__ == "__main__":
    automate_tryhackme()
    log("\n📈 Getting updated streak and profile...")
    fetch_profile_details()
    log("✅ Done!")
