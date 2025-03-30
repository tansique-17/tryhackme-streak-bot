from playwright.sync_api import sync_playwright
import pickle
import time
import os

# Constants
COOKIE_FILE = "tryhackme_cookies.pkl"
ROOM_URL = "https://tryhackme.com/room/tutorial"
ANSWER = "flag{connection_verified}"

# Start Playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Change to False for debugging locally
    context = browser.new_context()
    page = context.new_page()

    print("Opening TryHackMe...")
    page.goto("https://tryhackme.com")
    page.wait_for_load_state("networkidle")

    # Load cookies
    if os.path.exists(COOKIE_FILE):
        print("Loading cookies...")
        with open(COOKIE_FILE, "rb") as f:
            cookies = pickle.load(f)
            context.add_cookies(cookies)
    else:
        print("No cookies found! Logging in manually required.")
        page.goto("https://tryhackme.com/login")
        input("Press Enter after logging in manually...")
        pickle.dump(context.cookies(), open(COOKIE_FILE, "wb"))

    # Refresh page to apply session
    page.goto("https://tryhackme.com/dashboard")
    page.wait_for_load_state("networkidle")
    time.sleep(5)

    # Open room
    print("Opening tutorial room...")
    page.goto(ROOM_URL)
    page.wait_for_load_state("networkidle")
    time.sleep(5)

    # Click Options Button
    if page.locator("button:has-text('Options')").is_visible():
        page.click("button:has-text('Options')")
        print("Options menu opened!")
        time.sleep(3)
    else:
        print("Options button NOT found!")

    # Click Reset Room Button
    if page.locator("text=Reset Progress").is_visible():
        page.click("text=Reset Progress")
        print("Room reset button clicked!")
        time.sleep(3)
    else:
        print("Reset button NOT found!")

    # Confirm Reset
    if page.locator("button:has-text('Yes')").is_visible():
        page.click("button:has-text('Yes')")
        print("Room reset confirmed!")
        time.sleep(10)
    else:
        print("Reset confirmation button NOT found!")

    # Enter Answer
    input_field = page.locator("input[data-testid='answer-field']")
    if input_field.is_visible():
        input_field.click()
        input_field.fill(ANSWER)
        print(f"Entered Answer: {input_field.input_value()}")
        time.sleep(3)
    else:
        print("Answer input field NOT found!")

    # Submit Answer
    submit_button = page.locator("button:has-text('Submit')")
    if submit_button.is_visible():
        submit_button.click()
        print("Submit button clicked!")
        time.sleep(10)
    else:
        print("Submit button NOT found!")

    print("Process completed. Closing browser...")
    browser.close()
