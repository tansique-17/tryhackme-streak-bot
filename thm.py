import sys
import requests
import pickle
import time
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

# === Fix Unicode Encoding for Windows Terminals ===
if sys.platform == "win32":
    import os
    os.system("")  # Enables ANSI/VT100 support in newer Windows terminals
    sys.stdout.reconfigure(encoding='utf-8')

# === CONFIGURATION ===
COOKIE_FILE = "tryhackme_cookies.pkl"
ROOM_URL = "https://tryhackme.com/room/tutorial"
ANSWER = "flag{connection_verified}"
url = "https://tryhackme.com/api/v2/badges/public-profile?userPublicId=1282671"

# === Automate Room Reset & Flag Submission ===
def automate_tryhackme():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  # Set to False to see the browser
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

        # Reset room progress
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

        # Submit the flag
        try:
            input_field = page.locator("input[data-testid='answer-field']")
            input_field.wait_for(timeout=10000)
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

# === Fetch and Print Profile Info from Badge API ===
def fetch_badge_profile():
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    username = soup.find("span", class_="user_name").text.strip()
    rank = soup.find("span", class_="rank-title").text.strip()
    details = soup.find_all("span", class_="details-text")

    trophies = details[0].text.strip() if len(details) > 0 else None
    streak = details[1].text.strip() if len(details) > 1 else None
    awards = details[2].text.strip() if len(details) > 2 else None
    rooms_completed = details[3].text.strip() if len(details) > 3 else None

    badge_output = (
        f"👤 Username: {username}\n"
        f"🏅 Rank: {rank}\n"
        f"🥇 Trophies: {trophies}\n"
        f"🔥 Streak: {streak}\n"
        f"🎖️ Awards: {awards}\n"
        f"🚪 Rooms Completed: {rooms_completed}\n"
        f"✅ Done!"
    )

    with open("streak.txt", "w", encoding="utf-8") as f:
        f.write(badge_output)

    print(badge_output)

# === MAIN ===
if __name__ == "__main__":
    automate_tryhackme()
    print("\n📈 Getting updated streak and profile...")
    fetch_badge_profile()
