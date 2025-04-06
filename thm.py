from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pickle
import time
import re

# Constants
COOKIE_FILE = "tryhackme_cookies.pkl"
ROOM_URL = "https://tryhackme.com/room/tutorial"
ANSWER = "flag{connection_verified}"

def fetch_streak(page):
    """Fetch TryHackMe streak by searching full page HTML for 'X day streak'."""
    try:
        print("Fetching updated streak count from full page...")

        # Ensure we're on the dashboard page
        page.goto("https://tryhackme.com/dashboard", timeout=60000)
        page.wait_for_timeout(5000)

        # Get full HTML content
        full_html = page.content()

        # Parse with BeautifulSoup
        soup = BeautifulSoup(full_html, "html.parser")
        body_text = soup.get_text(separator=' ', strip=True)

        # Optional debug
        # print("Page text:")
        # print(body_text)

        # Search for streak using regex
        match = re.search(r'(\d+)\s+day(?:s)?\s+streak', body_text, re.IGNORECASE)
        if match:
            streak = match.group(1)
            print(f"✅ Found streak: {streak} day streak")
            return streak
        else:
            print("❌ Could not find 'X day streak' in page.")
            return "0"

    except Exception as e:
        print(f"⚠️ Error fetching streak: {e}")
        return "0"

# Start Playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Set to True to run headless
    context = browser.new_context()
    page = context.new_page()

    print("Opening TryHackMe...")
    page.goto("https://tryhackme.com", wait_until="domcontentloaded", timeout=60000)

    # Load saved cookies
    print("Loading cookies...")
    try:
        with open(COOKIE_FILE, "rb") as f:
            cookies = pickle.load(f)
            context.add_cookies(cookies)
    except Exception as e:
        print(f"Error loading cookies: {e}")

    # Refresh dashboard to apply session
    page.goto("https://tryhackme.com/dashboard", timeout=60000)
    time.sleep(5)

    # Open the tutorial room
    print("Opening the tutorial room...")
    page.goto(ROOM_URL, timeout=60000)
    time.sleep(10)

    # Click Options Button
    try:
        page.click("button:has-text('Options')")
        time.sleep(3)
        print("Options menu opened!")
    except:
        print("Error clicking options button")

    # Click Reset Room
    try:
        page.click("text=Reset Progress")
        print("Room reset button clicked!")
        time.sleep(3)
    except:
        print("Could not find the reset button. Skipping reset...")

    # Confirm Reset
    try:
        page.click("button:has-text('Yes')")
        print("Room reset confirmed!")
        time.sleep(10)
    except:
        print("Could not confirm reset. Check manually.")

    # Enter the answer
    try:
        input_field = page.locator("input[data-testid='answer-field']")
        input_field.wait_for(timeout=10000)
        input_field.click()
        input_field.fill(ANSWER)
        print("Answer entered!")
        time.sleep(3)
    except Exception as e:
        print(f"Error finding answer input field: {e}")

    # Click Submit Button
    try:
        page.click("button:has-text('Submit')")
        print("Answer submitted!")
        time.sleep(10)
    except:
        print("Error clicking submit button")

    # Fetch and save streak
    streak_count = fetch_streak(page)
    with open("streak.txt", "w") as f:
        f.write(streak_count)
    print(f"Streak count saved: {streak_count}")

    print("Closing Playwright browser...")
    browser.close()
