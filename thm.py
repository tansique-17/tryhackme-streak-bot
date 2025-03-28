from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Set up Chrome WebDriver options
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")  # Maximize window
options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid detection
options.headless = False  # Disable headless mode for debugging

# Start WebDriver
driver = webdriver.Chrome(options=options)

try:
    print("🔄 Opening TryHackMe...")
    driver.get("https://tryhackme.com/")  # Change to the correct URL

    # Wait for cookies (if applicable)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Accept')]"))
    ).click()
    print("🍪 Cookies accepted.")

    # Open the tutorial room
    print("📂 Opening the tutorial room...")
    driver.get("https://tryhackme.com/room/tutorial")  # Update to correct room URL

    # Wait for options button
    try:
        options_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div/main/div[2]/div[2]/div/div[2]/button[4]"))
        )
        options_button.click()
        print("✅ Options button clicked!")
    except Exception as e:
        print(f"❌ Error clicking options button: {e}")

    # Wait for Reset button
    try:
        reset_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/div[1]/div"))
        )
        reset_button.click()
        print("✅ Reset button clicked!")
    except Exception as e:
        print(f"❌ Reset button not found: {e}")

    # Wait for Confirmation button
    try:
        confirm_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[3]/div/footer/button[2]"))
        )
        confirm_button.click()
        print("✅ Confirmation button clicked!")
    except Exception as e:
        print(f"❌ Confirmation button not found: {e}")

    # Enter answer
    try:
        answer_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Enter your answer']"))
        )
        answer_field.send_keys("Sample Answer")
        print("📝 Answer entered!")

        # Submit button
        submit_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div[1]/div/div[2]/div/main/div[4]/div/div/div/div[2]/div/section/div[2]/div[2]/form/div[2]/button[1]"))
        )
        submit_button.click()
        print("🎉 Answer submitted successfully!")
    except Exception as e:
        print(f"❌ Error submitting answer: {e}")

    # Final confirmation message
    print("✅ TryHackMe streak successfully updated!")

except Exception as main_error:
    print(f"🚨 Fatal Error: {main_error}")

finally:
    # Close browser after 5 seconds
    print("🛑 Process completed. Closing browser in 5 seconds...")
    time.sleep(5)
    driver.quit()
