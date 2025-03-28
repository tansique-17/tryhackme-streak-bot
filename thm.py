from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pickle
import time

# Constants
COOKIE_FILE = "tryhackme_cookies.pkl"
ROOM_URL = "https://tryhackme.com/room/tutorial"
ANSWER = "flag{connection_verified}"

# Set up WebDriver (Headless for GitHub Actions)
options = webdriver.ChromeOptions()
#options.add_argument("--headless")  # Run in headless mode for CI/CD
options.add_argument("--no-sandbox")  # Fix for GitHub Actions
options.add_argument("--disable-dev-shm-usage")  # Prevent memory issues
options.add_argument("--window-size=1920,1080")  # Ensure full viewport rendering

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    print("🔄 Opening TryHackMe...")
    driver.get("https://tryhackme.com")
    time.sleep(5)  # Ensure full site load

    # Load saved cookies
    print("🍪 Loading cookies...")
    with open(COOKIE_FILE, "rb") as f:
        cookies = pickle.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)

    # Refresh page to apply session
    driver.get("https://tryhackme.com/dashboard")
    time.sleep(5)  # Ensure dashboard loads

    # Step 2: Open the tutorial room
    print("📂 Opening the tutorial room...")
    driver.get(ROOM_URL)
    time.sleep(10)  # Increased wait time for full room load

    # Step 3: Click the options button to reveal reset option
    try:
        options_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Options')]"))
        )
        options_button.click()
        print("📂 Options menu opened!")
        time.sleep(3)
    except Exception as e:
        print(f"❌ Error clicking options button: {e}")

    # Step 4: Click Reset Room Button
    reset_clicked = False
    reset_xpaths = [
        "//div[contains(text(), 'Reset Room')]",  # Dynamic XPath
        "/html/body/div[3]/div/div[1]/div"  # Backup XPath
    ]

    for xpath in reset_xpaths:
        try:
            reset_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            reset_button.click()
            print(f"✅ Room reset button clicked using XPath: {xpath}")
            reset_clicked = True
            time.sleep(3)
            break  # Exit loop once reset is successful
        except Exception:
            print(f"⚠️ Reset button not found with XPath: {xpath}")

    if not reset_clicked:
        print("❌ Could not find the reset button. Skipping reset...")

    # Step 5: Click "Yes" to confirm reset
    yes_clicked = False
    yes_xpaths = [
        "//button[contains(text(), 'Yes')]",  # Dynamic XPath
        "/html/body/div[3]/div/footer/button[2]"  # Backup XPath
    ]

    for xpath in yes_xpaths:
        try:
            yes_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            yes_button.click()
            print(f"✅ Room reset confirmed using XPath: {xpath}")
            yes_clicked = True
            time.sleep(10)  # 🔥 NEW: Wait 10 seconds to allow reset
            break  # Exit loop once confirmation is successful
        except Exception:
            print(f"⚠️ Confirmation button not found with XPath: {xpath}")

    if not yes_clicked:
        print("❌ Could not confirm reset. Check manually.")

    # Step 6: Enter the answer
    try:
        answer_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='text']"))
        )
        answer_input.send_keys(ANSWER)
        time.sleep(3)
        print("📝 Answer entered!")
    except Exception as e:
        print(f"❌ Error finding answer input field: {e}")

    # Step 7: Click Submit Button
    try:
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Submit')]"))
        )
        submit_button.click()
        print("🎉 TryHackMe streak successfully updated!")

        # NEW: Wait 30 seconds after submitting
        print("⏳ Waiting 30 seconds to ensure streak updates...")
        time.sleep(30)

    except Exception as e:
        print(f"❌ Error clicking submit button: {e}")

except Exception as e:
    print(f"❌ Unexpected error: {e}")

finally:
    print("🛑 Process completed. Closing browser in 5 seconds...")
    time.sleep(5)
    driver.quit()
