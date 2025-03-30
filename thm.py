from playwright.sync_api import sync_playwright
import pickle
import time

# Constants
COOKIE_FILE = "tryhackme_cookies.pkl"
ROOM_URL = "https://tryhackme.com/room/tutorial"
ANSWER = "flag{connection_verified}"

def fetch_streak(page):
    """Fetch TryHackMe streak count."""
    try:
        print("Fetching updated streak count...")

        # Use class-based locator (ensuring it picks the FIRST element)
        streak_element = page.locator("p.sc-bXWnss.bnzZjc").first
        streak_text = streak_element.inner_text().strip()
        print(f"Streak fetched via class locator: {streak_text}")
        return streak_text

    except Exception as e:
        print(f"Error fetching streak count: {e}")
        return "0"

# Start Playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
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
        print("
