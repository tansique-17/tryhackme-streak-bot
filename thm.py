import requests
import pickle
import time
from playwright.sync_api import sync_playwright

# === CONFIGURATION ===
COOKIE_FILE = "tryhackme_cookies.pkl"
ROOM_URL = "https://tryhackme.com/room/tutorial"
ANSWER = "flag{connection_verified}"
PROFILE_URL = "https://tryhackme.com/api/v2/badges/public-profile?userPublicId=1282671"

# === Automate Room Reset & Flag Submission ===
def automate_tryhackme():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("🌐 Opening TryHackMe...")
        page.goto("https://tryhackme.com", wait_until="domcontentloaded", timeout=60000)

        print("🍪 Loading cookies...")
        try:
            with open(COOKIE_FILE, "rb") as f:
                cookies = pickle.load(f)
                context.add_cookies(cookies)
        except Exception as e:
            print(f"⚠️ Error loading cookies: {e}")

        print("🚪 Opening the tutorial room...")
        page.goto(ROOM_URL, timeout=60000)
        time.sleep(10)

        try:
            page.click("button:has-text('Options')")
            time.sleep(2)
            page.click("text=Reset Progress")
            time.sleep(2)
            page.click("button:has-text('Yes')")
            print("♻️ Room reset confirmed!")
            time.sleep(5)
        except Exception as e:
            print(f"⚠️ Could not reset room: {e}")

        try:
            input_field = page.locator("input[data-testid='answer-field']")
            input_field.wait_for(timeout=10000)
            input_field.click()
            input_field.fill(ANSWER)
            print("✏️ Answer entered.")
            time.sleep(2)
            page.click("button:has-text('Submit')")
            print("🚀 Answer submitted!")
            time.sleep(5)
        except Exception as e:
            print(f"⚠️ Error submitting flag: {e}")

        print("🛑 Closing browser...")
        browser.close()

# === Fetch Profile Badge and Save ===
def fetch_profile_details():
    try:
        res = requests.get(PROFILE_URL, timeout=10)
        json_data = res.json()

        user = json_data.get("user", {})
        username = user.get("name", "Unknown")
        rank = user.get("rank", "Unknown")
        trophies = user.get("trophies", 0)
        streak = user.get("streak", 0)
        awards = user.get("awards", 0)
        rooms_completed = user.get("roomsCompleted", 0)

        profile_summary = (
            f"🧾 TryHackMe Profile Summary:\n"
            f"👤 Username: {username}\n"
            f"🏅 Rank: {rank}\n"
            f"🥇 Trophies: {trophies}\n"
            f"🔥 Streak: {streak} days\n"
            f"🎖️ Awards: {awards}\n"
            f"🚪 Rooms Completed: {rooms_completed}"
        )

        print(f"\n{profile_summary}")

        with open("streak.txt", "w", encoding="utf-8") as f:
            f.write(profile_summary)

        print(f"\n💾 Streak count saved: {streak} days")

    except Exception as e:
        print(f"⚠️ Error fetching profile info: {e}")

# === MAIN ===
if __name__ == "__main__":
    automate_tryhackme()
    print("\n📈 Getting updated streak and profile...")
    fetch_profile_details()
    print("✅ Done!")
