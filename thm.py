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

# Set up WebDriver (USE Xvfb for GitHub Actions)
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Keep for GitHub Actions
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")  # Ensure elements load properly

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    print("🔄 Opening TryHackMe...")
    driver.get("https://tryhackme.com")
    
    # Wait until page loads fully
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Load saved cookies
    print("🍪 Loading cookies...")
    try:
        with open(COOKIE_FILE, "rb") as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                driver.add_cookie(cookie)
        driver.get("https://tryhackme.com/dashboard")  # Refresh page to apply cookies
    except Exception as e:
        print(f"⚠️ No cookies found or failed to load: {e}")

    # Step 2: Open the tutorial room
    print("📂 Opening the tutorial room...")
    driver.get(ROOM_URL)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    # Step 3: Click the options button to reveal reset option
    try:
        print("📂 Clicking options menu...")
        options_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div/main/div[2]/div[2]/div/div[2]/button[4]"))
        )
        driver.execute_script("arguments[0].click();", options_button)  # JavaScript click
        print("✅ Options menu opened!")
    except Exception as e:
        print(f"❌ Error clicking options button: {e}")
        driver.save_screenshot("debug_options.png")

    # Step 4: Click Reset Room Button
    reset_clicked = False
    reset_xpaths = [
        "/html/body/div[3]/div/div[1]/div",  # First XPath
        "//*[@id='radix-:r1l:']/div[1]/div"  # Alternative XPath
    ]

    for xpath in reset_xpaths:
        try:
            reset_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            driver.execute_script("arguments[0].click();", reset_button)  # JavaScript click
            print(f"✅ Room reset button clicked using XPath: {xpath}")
            reset_clicked = True
            break
        except Exception:
            print(f"⚠️ Reset button not found with XPath: {xpath}")
            driver.save_screenshot("debug_reset.png")

    if not reset_clicked:
        print("❌ Could not find the reset button. Skipping reset...")

    # Step 5: Click "Yes" to confirm reset
    yes_clicked = False
    yes_xpaths = [
        "//*[@id='radix-:r1m:']/footer/button[2]",  # New XPath
        "/html/body/div[3]/div/footer/button[2]"  # Old XPath
    ]

    for xpath in yes_xpaths:
        try:
            yes_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            driver.execute_script("arguments[0].click();", yes_button)  # JavaScript click
            print(f"✅ Room reset confirmed using XPath: {xpath}")
            yes_clicked = True
            time.sleep(10)  # Wait for reset to complete
            break
        except Exception:
            print(f"⚠️ Confirmation button not found with XPath: {xpath}")
            driver.save_screenshot("debug_confirm.png")

    if not yes_clicked:
        print("❌ Could not confirm reset. Check manually.")

    # Step 6: Enter the answer
    try:
        answer_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[1]/div/div[2]/div/main/div[4]/div/div/div/div[2]/div/section/div[2]/div[2]/form/div[1]/div/input'))
        )
        answer_input.send_keys(ANSWER)
        print("📝 Answer entered!")
    except Exception as e:
        print(f"❌ Error finding answer input field: {e}")
        driver.save_screenshot("debug_answer.png")

    # Step 7: Click Submit Button
    try:
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div[1]/div/div[2]/div/main/div[4]/div/div/div/div[2]/div/section/div[2]/div[2]/form/div[2]/button[1]'))
        )
        driver.execute_script("arguments[0].click();", submit_button)  # JavaScript click
        print("🎉 TryHackMe streak successfully updated!")

        # NEW: Wait 30 seconds after submitting
        print("⏳ Waiting 30 seconds to ensure streak updates...")
        time.sleep(30)

    except Exception as e:
        print(f"❌ Error clicking submit button: {e}")
        driver.save_screenshot("debug_submit.png")

except Exception as e:
    print(f"❌ Unexpected error: {e}")

finally:
    print("🛑 Process completed. Closing browser in 5 seconds...")
    time.sleep(5)
    driver.quit()
