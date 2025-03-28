from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import pickle
import time

# Constants
COOKIE_FILE = "tryhackme_cookies.pkl"
ROOM_URL = "https://tryhackme.com/room/tutorial"
ANSWER = "flag{connection_verified}"

# Set up WebDriver (SHOW browser for debugging)
options = webdriver.ChromeOptions()
#options.add_argument("--headless")  # Comment this to see the browser
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
        options_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div/main/div[2]/div[2]/div/div[2]/button[4]")
        options_button.click()
        time.sleep(3)
        print("📂 Options menu opened!")
    except Exception as e:
        print(f"❌ Error clicking options button: {e}")

    # Step 4: Click Reset Room Button
    reset_clicked = False
    reset_xpaths = [
        "/html/body/div[3]/div/div[1]/div",  # First XPath
        "//*[@id='radix-:r1l:']/div[1]/div"  # Alternative XPath
    ]

    for xpath in reset_xpaths:
        try:
            reset_button = driver.find_element(By.XPATH, xpath)
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
        "//*[@id='radix-:r1m:']/footer/button[2]",  # New XPath
        "/html/body/div[3]/div/footer/button[2]"  # Old XPath
    ]

    for xpath in yes_xpaths:
        try:
            yes_button = driver.find_element(By.XPATH, xpath)
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
        answer_input = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[2]/div/main/div[4]/div/div/div/div[2]/div/section/div[2]/div[2]/form/div[1]/div/input')
        answer_input.send_keys(ANSWER)
        time.sleep(3)
        print("📝 Answer entered!")
    except Exception as e:
        print(f"❌ Error finding answer input field: {e}")

    # Step 7: Click Submit Button
    try:
        submit_button = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div/div[2]/div/main/div[4]/div/div/div/div[2]/div/section/div[2]/div[2]/form/div[2]/button[1]')
        submit_button.click()
        print("🎉 TryHackMe streak successfully updated!")

        # NEW: Wait 30 seconds after submitting
        print("⏳ Waiting 30 seconds to ensure streak updates...")
        time.sleep(0)

    except Exception as e:
        print(f"❌ Error clicking submit button: {e}")

except Exception as e:
    print(f"❌ Unexpected error: {e}")

finally:
    print("🛑 Process completed. Closing browser in 5 seconds...")
    time.sleep(10)
    driver.quit()
