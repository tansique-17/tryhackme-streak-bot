from playwright.sync_api import sync_playwright
import pickle
import time

# Constants
COOKIE_FILE = "tryhackme_cookies.pkl"
ROOM_URL = "https://tryhackme.com/room/tutorial"
ANSWER = "flag{connection_verified}"

# Start Playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Run headless for GitHub Actions
    context = browser.new_context()
    page = context.new_page()

    print("🔄 Opening TryHackMe...")
    page.goto("https://tryhackme.com")
    time.sleep(5)

    # Load saved cookies
    print("🍪 Loading cookies...")
    with open(COOKIE_FILE, "rb") as f:
        cookies = pickle.load(f)
        context.add_cookies(cookies)

    # Refresh page to apply session
    page.goto("https://tryhackme.com/dashboard")
    time.sleep(5)

    # Step 2: Open the tutorial room
    print("📂 Opening the tutorial room...")
    page.goto(ROOM_URL)
    time.sleep(10)

    # Step 3: Click the options button
    try:
        page.click("button:has-text('Options')")
        time.sleep(3)
        print("📂 Options menu opened!")
    except:
        print("❌ Error clicking options button")

    # Step 4: Click Reset Room Button
    try:
        page.click("text=Reset Room")
        print("✅ Room reset button clicked!")
        time.sleep(3)
    except:
        print("❌ Could not find the reset button. Skipping reset...")

    # Step 5: Confirm Reset
    try:
        page.click("button:has-text('Yes')")
        print("✅ Room reset confirmed!")
        time.sleep(10)
    except:
        print("❌ Could not confirm reset. Check manually.")

    # Step 6: Enter the answer
    try:
        page.fill("input[type='text']", ANSWER)
        time.sleep(3)
        print("📝 Answer entered!")
    except:
        print("❌ Error finding answer input field")

    # Step 7: Click Submit Button
    try:
        page.click("button:has-text('Submit')")
        print("🎉 TryHackMe streak successfully updated!")
        time.sleep(30)
    except:
        print("❌ Error clicking submit button")

    print("🛑 Process completed. Closing browser...")
    browser.close()
