from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

# 🛠 Setup Chrome WebDriver with Headless Mode for CI/CD
options = webdriver.ChromeOptions()
options.add_argument("--headless=new")  # Headless mode for GitLab CI/CD
options.add_argument("--disable-gpu")  # Disables GPU for better stability
options.add_argument("--no-sandbox")  # Required for GitLab CI/CD
options.add_argument("--disable-dev-shm-usage")  # Prevents memory issues
options.add_argument("--window-size=1920,1080")  # Set screen size for headless mode
options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid bot detection

# 🌐 Initialize WebDriver (Auto-downloads correct ChromeDriver version)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    print("🔄 Opening TryHackMe...")
    driver.get("https://tryhackme.com/")

    # ✅ Accept Cookies
    try:
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Accept')]"))
        ).click()
        print("🍪 Cookies accepted.")
    except:
        print("⚠️ No cookies popup found, continuing...")

    # 🏴 Open the tutorial room
    driver.get("https://tryhackme.com/room/tutorial")
    print("📂 Opened the tutorial room.")

    # ✅ Click Options Button
    try:
        options_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Options')]"))
        )
        options_button.click()
        print("✅ Options button clicked!")
    except Exception as e:
        print(f"❌ Error clicking options button: {e}")

    # ✅ Click Reset Button
    try:
        reset_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'modal')]//button[contains(text(),'Reset')]"))
        )
        reset_button.click()
        print("✅ Reset button clicked!")
    except Exception as e:
        print(f"❌ Reset button not found: {e}")

    # ✅ Confirm Reset
    try:
        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//footer//button[contains(text(),'Confirm')]"))
        )
        confirm_button.click()
        print("✅ Confirmation button clicked!")
    except Exception as e:
        print(f"❌ Confirmation button not found: {e}")

    # ✅ Enter Answer
    try:
        answer_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter your answer']"))
        )
        answer_field.send_keys("Sample Answer")
        print("📝 Answer entered!")

        # ✅ Submit Answer
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Submit')]"))
        )
        submit_button.click()
        print("🎉 Answer submitted successfully!")
    except Exception as e:
        print(f"❌ Error submitting answer: {e}")

    print("✅ TryHackMe streak successfully updated!")

except Exception as main_error:
    print(f"🚨 Fatal Error: {main_error}")

finally:
    print("🛑 Process completed. Closing browser...")
    driver.quit()
