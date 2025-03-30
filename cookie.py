from playwright.sync_api import sync_playwright
import pickle
import os

# Constants
COOKIE_DIR = "cookies"
COOKIE_FILE = os.path.join(COOKIE_DIR, "tryhackme_cookies.pkl")
LOGIN_URL = "https://tryhackme.com/login"
DASHBOARD_URL = "https://tryhackme.com/dashboard"

# Ensure the cookies directory exists
os.makedirs(COOKIE_DIR, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # Open browser with UI
    context = browser.new_context()
    page = context.new_page()

    print("🔄 Opening TryHackMe login page...")
    page.goto(LOGIN_URL)

    # Wait until login is detected (when redirected to the dashboard)
    print("⏳ Waiting for login completion...")
    page.wait_for_url(DASHBOARD_URL, timeout=120000)  # 2-minute timeout for manual login

    # Save cookies in .pkl format inside "cookies" directory
    cookies = context.cookies()
    with open(COOKIE_FILE, "wb") as f:
        pickle.dump(cookies, f)

    print(f"✅ Login detected! Cookies saved at: {COOKIE_FILE}")

    browser.close()
