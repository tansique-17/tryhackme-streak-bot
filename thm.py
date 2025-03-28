from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time
import pickle

# Constants
COOKIE_FILE = "tryhackme_cookies.pkl"
ROOM_URL = "https://tryhackme.com/room/tutorial"
ANSWER = "flag{connection_verified}"

# Set up WebDriver (Headless for GitHub Actions)
options = webdriver.ChromeOptions()
# Comment this line if you want to see the browser
options.add_argument("--headless")  

# Start WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    print("🔄 Opening TryHackMe...")
    driver.get("https://tryhackme.com")
    time.sleep(5)

    # Load cookies
    print("🍪 Loading cookies...")
    with open(COOKIE_FILE, "rb") as f:
        cookies = pickle.load(f)
        for cookie in cookies:
            driver.add_cookie(cookie)

    # Refresh to apply session
    driver.get("https://tryhackme.com/dashboard")
    time.sleep(5)

    # Open tutorial room
    print("📂 Opening the tutorial room...")
    driver.get(ROOM_URL)
    time.sleep(10)

    # Click options menu
    try:
        options_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div/main/div[2]/div[2]/div/div[2]/button[4]")
        options_button.click()
        time.sleep(3)
        print("✅ Options menu opened!")
    except Exception as e:
        print(f"❌ Error clicking options button: {e}")

    # Click Reset Room Button
    try:
        reset_button = driver.find_element(By.XPATH, "/html/body/div[3]/div/div[1]/div")
        reset_button.click()
        print("✅ Room reset button clicked!")
        time.sleep(3)
    except Exception as e:
        print(f"❌ Reset button not found: {e}")

    # Click "Yes" to confirm reset
    try:
        yes_button = driver.find_element(By.XPATH, "/html/body/div[3]/div/footer/button[2]")
        yes_button.click()
        print("✅ Room reset confirmed!")
        time.sleep(10)
    except Exception as e:
        print(f"❌ Confirmation button not found: {e}")

    # Enter the answer
    try:
        answer_input = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div/main/div[4]/div/div/div/div[2]/div/section/div[2]/div[2]/form/div[1]/div/input")
        answer_input.send_keys(ANSWER)
        time.sleep(3)
        print("📝 Answer entered!")
    except Exception as e:
        print(f"❌ Error finding answer input field: {e}")

    # Click Submit Button
    try:
        submit_button = driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div/main/div[4]/div/div/div/div[2]/div/section/div[2]/div[2]/form/div[2]/button[1]")
        submit_button.click()
        print("🎉 TryHackMe streak successfully updated!")
        time.sleep(10)
    except Exception as e:
        print(f"❌ Error clicking submit button: {e}")

except Exception as e:
    print(f"❌ Unexpected error: {e}")

finally:
    print("🛑 Process completed. Closing browser in 5 seconds...")
    time.sleep(5)
    driver.quit()
