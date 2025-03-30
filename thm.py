from playwright.sync_api import sync_playwright
import pickle
import time

# Constants
COOKIE_FILE = "tryhackme_cookies.pkl"
ROOM_URL = "https://tryhackme.com/room/tutorial"
ANSWER = "flag{connection_verified}"
STREAK_FILE = "streak.txt"  # File to store streak count

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    print("Opening TryHackMe...")

    # Load cookies
    try:
        with open(COOKIE_FILE, "rb") as f:
            cookies = pickle.load(f)
            context.add_cookies(cookies)
    except Exception as e:
        print(f"Error loading cookies: {e}")

    # Open TryHackMe dashboard
    page.goto("https://tryhackme.com/dashboard", timeout=60000)
    time.sleep(5)

    # Open tutorial room
    page.goto(ROOM_URL, timeout=60000)
    time.sleep(10)

    # Reset room (if needed)
    try:
        page.click("button:has-text('Options')")
        time.sleep(3)
        page.click("text=Reset Progress")
        time.sleep(3)
        page.click("button:has-text('Yes')")
        time.sleep(10)
    except:
        print("Skipping reset...")

    # Submit answer
    try:
        input_field = page.locator("input[data-testid='answer-field']")
        input_field.wait_for(timeout=10000)
        input_field.click()
        input_field.fill(ANSWER)
        time.sleep(3)
        page.click("button:has-text('Submit')")
        print("TryHackMe streak updated!")
        time.sleep(10)
    except Exception as e:
        print(f"Error submitting answer: {e}")

    # Extract updated streak count
    try:
        print("Fetching updated streak count...")
        page.goto("https://tryhackme.com/dashboard", timeout=60000)
        time.sleep(5)

        streak_element = page.locator("button[aria-label$='day streak'] p")
        streak_element.wait_for(timeout=10000)
        streak_count = streak_element.inner_text()

        print(f"🔥 Your updated TryHackMe streak: {streak_count} days!")

        # Save streak count to a file
        with open(STREAK_FILE, "w") as f:
            f.write(streak_count)

    except Exception as e:
        print(f"Error fetching streak count: {e}")

    print("Process completed. Closing browser...")
    browser.close()
