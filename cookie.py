from playwright.sync_api import sync_playwright
import pickle
import os
import base64

# Constants
COOKIE_DIR = "cookies"
COOKIE_FILE = os.path.join(COOKIE_DIR, "tryhackme_cookies.txt")
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

    # Save cookies and encode to base64
    cookies = context.cookies()
    cookies_pickled = pickle.dumps(cookies)  # Pickle cookies
    cookies_base64 = base64.b64encode(cookies_pickled).decode('utf-8')  # Base64 encode the pickled cookies

    # Save the base64 encoded cookies to a .txt file
    with open(COOKIE_FILE, "w") as f:
        f.write(cookies_base64)

    print(f"✅ Login detected! Cookies saved as base64 in: {COOKIE_FILE}")

    browser.close()
