from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pickle

# Set up Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Open TryHackMe login page
driver.get("https://tryhackme.com/login")
time.sleep(60)  # Wait for you to manually log in and solve CAPTCHA

# Save cookies
cookies = driver.get_cookies()
with open("tryhackme_cookies.pkl", "wb") as f:
    pickle.dump(cookies, f)

print("✅ Cookies saved as tryhackme_cookies.pkl!")
driver.quit()
