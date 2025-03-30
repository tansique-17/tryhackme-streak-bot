from playwright.sync_api import sync_playwright
import pickle
import time

# Constants
COOKIE_FILE = "tryhackme_cookies.pkl"
ROOM_URL = "https://tryhackme.com/room/tutorial"
ANSWER = "flag{connection_verified}"

# Start Playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Set to False for debugging
    context = browser.new_context()
    page = context.new_page()

    print("🔄 Opening TryHackMe...")
    page.goto("https://tryhackme.com", timeout=60000)  # Increase timeout
    page.wait_for_load_state("domcontentloaded")  # Faster page detection

    time.sleep(5)  # Small delay to ensure elements load

    # Load saved cookies
    print("🍪 Loading cookies...")
    with open(COOKIE_FILE, "rb") as f:
        cookies = pickle.load(f)
        context.add_cookies(cookies)

    # Refresh page to apply session
    page.goto("https://tryhackme.com/dashboard", timeout=60000)
    page.wait_for_load_state("domcontentloaded")
    time.sleep(5)

    # Step 2: Open the tutorial room
    print("📂 Opening the tutorial room...")
    page.goto(ROOM_URL, timeout=60000)
    page.wait_for_load_state("domcontentloaded")
    time.sleep(10)

    # Step 3: Click the options button
    try:
        page.locator("button:has-text('Options')").click(timeout=5000)
        time.sleep(3)
        print("📂 Options menu opened!")
    except:
        print("❌ Error clicking options button")

    # Step 4: Click Reset Room Button
    try:
        page.locator("text=Reset Progress").click(timeout=5000)
        print("✅ Room reset button clicked!")
        time.sleep(3)
    except:
        print("❌ Could not find the reset button. Skipping reset...")

    # Step 5: Confirm Reset
    try:
        page.locator("button:has-text('Yes')").click(timeout=5000)
        print("✅ Room reset confirmed!")
        time.sleep(10)
    except:
        print("❌ Could not confirm reset. Check manually.")

    # Step 6: Enter the answer
    try:
        input_field = page.locator("input[data-testid='answer-field']")
        input_field.wait_for(timeout=5000)
        input_field.click()
        input_field.fill(ANSWER)
        print("📝 Answer entered!")
        time.sleep(3)
    except Exception as e:
        print(f"❌ Error finding answer input field: {e}")

    # Step 7: Click Submit Button
    try:
        page.locator("button:has-text('Submit')").click(timeout=5000)
        print("🎉 TryHackMe streak successfully updated!")
        time.sleep(10)
    except:
        print("❌ Error clicking submit button")

    print("🛑 Process completed. Closing browser...")
    browser.close()
