from playwright.sync_api import sync_playwright
import pickle
import time

# Constants
COOKIE_FILE = "tryhackme_cookies.pkl"
ROOM_URL = "https://tryhackme.com/room/tutorial"
ANSWER = "flag{connection_verified}"

# Start Playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Headless must be True for GitHub Actions
    context = browser.new_context()
    page = context.new_page()

    print("Opening TryHackMe...")
    
    # Debugging: Screenshot before page load
    page.goto("https://tryhackme.com", wait_until="domcontentloaded", timeout=60000)
    page.screenshot(path="debug_before_wait.png")
    print("Screenshot taken: debug_before_wait.png")

    # Load saved cookies
    print("Loading cookies...")
    try:
        with open(COOKIE_FILE, "rb") as f:
            cookies = pickle.load(f)
            context.add_cookies(cookies)
    except Exception as e:
        print(f"Error loading cookies: {e}")

    # Refresh page to apply session
    page.goto("https://tryhackme.com/dashboard", timeout=60000)
    time.sleep(5)

    # Step 2: Open the tutorial room
    print("Opening the tutorial room...")
    page.goto(ROOM_URL, timeout=60000)
    time.sleep(10)

    # Step 3: Click the options button
    try:
        page.click("button:has-text('Options')")
        time.sleep(3)
        print("Options menu opened!")
    except:
        print("Error clicking options button")

    # Step 4: Click Reset Room Button
    try:
        page.click("text=Reset Progress")
        print("Room reset button clicked!")
        time.sleep(3)
    except:
        print("Could not find the reset button. Skipping reset...")

    # Step 5: Confirm Reset
    try:
        page.click("button:has-text('Yes')")
        print("Room reset confirmed!")
        time.sleep(10)
    except:
        print("Could not confirm reset. Check manually.")

    # Step 6: Enter the answer
    try:
        input_field = page.locator("input[data-testid='answer-field']")
        input_field.wait_for(timeout=10000)  # Ensure element is loaded
        input_field.click()
        input_field.fill(ANSWER)
        print("Answer entered!")
        time.sleep(3)
    except Exception as e:
        print(f"Error finding answer input field: {e}")

    # Step 7: Click Submit Button
    try:
        page.click("button:has-text('Submit')")
        print("TryHackMe streak successfully updated!")
        time.sleep(10)
    except:
        print("Error clicking submit button")

    print("Process completed. Closing browser...")
    browser.close()
