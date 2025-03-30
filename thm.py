from playwright.sync_api import sync_playwright
import pickle
import time

# Constants
COOKIE_FILE = "tryhackme_cookies.pkl"
ROOM_URL = "https://tryhackme.com/room/tutorial"
ANSWER = "flag{connection_verified}"
STREAK_FILE = "streak.txt"

def get_streak(page):
    """Attempts to fetch the streak count using XPath first, then falls back to class selector."""
    try:
        print("Fetching updated streak count...")

        # Try XPath first
        streak_element = page.locator("//body/div[1]/div[1]/div/div[2]/div/div[1]/header/div/div[2]/div/button[2]/p")
        streak_element.wait_for(timeout=5000)
        streak_text = streak_element.inner_text().strip()
        print(f"Streak fetched via XPath: {streak_text}")
        return streak_text

    except:
        print("XPath failed, trying class-based locator...")

        try:
            # Fall back to class name selector
            streak_element = page.locator("p.sc-bXWnss.bnzZjc")
            streak_element.wait_for(timeout=5000)
            streak_text = streak_element.inner_text().strip()
            print(f"Streak fetched via class selector: {streak_text}")
            return streak_text

        except Exception as e:
            print(f"Error fetching streak count: {e}")
            return "0"  # Default fallback

# Start Playwright
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)  # Headless mode for GitHub Actions
    context = browser.new_context()
    page = context.new_page()

    print("Opening TryHackMe...")

    # Load TryHackMe website
    page.goto("https://tryhackme.com", wait_until="domcontentloaded", timeout=60000)

    # Load cookies for authentication
    print("Loading cookies...")
    try:
        with open(COOKIE_FILE, "rb") as f:
            cookies = pickle.load(f)
            context.add_cookies(cookies)
    except Exception as e:
        print(f"Error loading cookies: {e}")

    # Refresh to apply session
    page.goto("https://tryhackme.com/dashboard", timeout=60000)
    time.sleep(5)

    # Open the tutorial room
    print("Opening the tutorial room...")
    page.goto(ROOM_URL, timeout=60000)
    time.sleep(10)

    # Click the "Options" button
    try:
        page.click("button:has-text('Options')")
        time.sleep(3)
        print("Options menu opened!")
    except:
        print("Error clicking options button")

    # Click "Reset Progress" (if available)
    try:
        page.click("text=Reset Progress")
        print("Room reset button clicked!")
        time.sleep(3)
    except:
        print("Could not find the reset button. Skipping reset...")

    # Confirm reset
    try:
        page.click("button:has-text('Yes')")
        print("Room reset confirmed!")
        time.sleep(10)
    except:
        print("Could not confirm reset. Check manually.")

    # Enter the answer
    try:
        input_field = page.locator("input[data-testid='answer-field']")
        input_field.wait_for(timeout=10000)  # Ensure element is loaded
        input_field.click()
        input_field.fill(ANSWER)
        print("Answer entered!")
        time.sleep(3)
    except Exception as e:
        print(f"Error finding answer input field: {e}")

    # Click "Submit"
    try:
        page.click("button:has-text('Submit')")
        print("TryHackMe streak successfully updated!")
        time.sleep(10)
    except:
        print("Error clicking submit button")

    # Fetch and Save Streak Count
    streak_text = get_streak(page)
    with open(STREAK_FILE, "w") as f:
        f.write(streak_text)
    print(f"Streak count saved: {streak_text}")

    print("Process completed. Closing browser...")
    browser.close()
