import sys
import time
import pickle
from playwright.sync_api import sync_playwright

# Ensure Unicode support (fix for Windows GitHub Actions)
sys.stdout.reconfigure(encoding='utf-8')

# Constants
COOKIE_FILE = "tryhackme_cookies.pkl"
ROOM_URL = "https://tryhackme.com/room/tutorial"
ANSWER = "flag{connection_verified}"

# Start Playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Set to True to run headless
    context = browser.new_context()
    page = context.new_page()

    print("🔄 Opening TryHackMe...")
    page.goto("https://tryhackme.com")
    page.wait_for_load_state("networkidle")

    # Load saved cookies
    print("🍪 Loading cookies...")
    try:
        with open(COOKIE_FILE, "rb") as f:
            cookies = pickle.load(f)
            context.add_cookies(cookies)
    except Exception as e:
        print(f"⚠️ No valid cookies found: {e}")

    # Refresh page to apply session
    page.goto("https://tryhackme.com/dashboard")
    page.wait_for_load_state("networkidle")

    # Step 2: Open the tutorial room
    print("📂 Opening the tutorial room...")
    page.goto(ROOM_URL)
    page.wait_for_load_state("networkidle")

    # Step 3: Click the options button
    try:
        page.locator("button:has-text('Options')").click()
        print("📂 Options menu opened!")
    except Exception as e:
        print(f"❌ Error clicking options button: {e}")

    # Step 4: Click Reset Room Button
    try:
        page.locator("text=Reset Progress").click()
        print("✅ Room reset button clicked!")
    except Exception as e:
        print(f"❌ Could not find the reset button: {e}")

    # Step 5: Confirm Reset
    try:
        page.locator("button:has-text('Yes')").click()
        print("✅ Room reset confirmed!")
    except Exception as e:
        print(f"❌ Could not confirm reset: {e}")

    # Step 6: Enter the answer
    try:
        input_field = page.locator("input[data-testid='answer-field']")
        input_field.wait_for(timeout=5000)  # Ensure element is loaded
        input_field.click()
        input_field.fill(ANSWER)
        print("📝 Answer entered!")
    except Exception as e:
        print(f"❌ Error finding answer input field: {e}")

    # Step 7: Click Submit Button
    try:
        page.locator("button:has-text('Submit')").click()
        print("🎉 TryHackMe streak successfully updated!")
    except Exception as e:
        print(f"❌ Error clicking submit button: {e}")

    print("🛑 Process completed. Closing browser...")
    browser.close()
