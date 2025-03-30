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

        # Try XPath first
        streak_xpath = page.locator("xpath=/html/body/div[1]/div[1]/div/div[2]/div/div[1]/header/div/div[2]/div/button[2]/p")
        if streak_xpath.count() > 0:
            streak_text = streak_xpath.first.inner_text().strip()
            print(f"Streak fetched via XPath: {streak_text}")
            return streak_text

        # If XPath fails, try class-based locator (ensuring it picks the FIRST element)
        print("XPath failed, trying class-based locator...")
        streak_element = page.locator("p.sc-bXWnss.bnzZjc").first  # Picks only the first match
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
        print("TryHackMe streak updated!")
        time.sleep(10)
    except:
        print("Error clicking submit button")

    # Fetch and save streak count
    streak_count = fetch_streak(page)
    with open("streak.txt", "w") as f:
        f.write(streak_count)
    print(f"Streak count saved: {streak_count}")

    print("Process completed. Closing browser...")
    browser.close()
