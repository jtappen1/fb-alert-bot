from splinter import Browser
from bs4 import BeautifulSoup as soup
import re
import pandas as pd
import matplotlib.pyplot as plt
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np


def main():

    chrome_options = Options()
    # chrome_options.add_argument("--user-data-dir=/Users/jtappen/Library/Application Support/Google/Chrome")
    # chrome_options.add_argument("--profile-directory=Profile 5")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--start-maximized")

    
    print("About to launch Browser")
    browser = Browser(
        "chrome",
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    print("Browser Launched")

    base_url = 'https://www.facebook.com/marketplace/philly/search?'
    initial_url = "https://www.facebook.com/login/device-based/regular/login/"

    min_price = 200
    max_price = 1000
    days_since_listed = 1

    url = f"{base_url}minPrice={min_price}&maxPrice={max_price}&daysSinceListed={days_since_listed}&query=electric%20guitars&exact=false"
    print("Created URL")
    browser.visit(initial_url)
    print("Visited URL")
    
    driver = browser.driver
    wait = WebDriverWait(driver, 15)

    try:
        time.sleep(1 )
        email_input = wait.until(
            EC.presence_of_element_located((By.NAME, "email"))
        )
        email_input.clear()
        email_input.send_keys("fbhelper1@proton.me")
        time.sleep(1)

        password_input = wait.until(
            EC.presence_of_element_located((By.NAME, "pass"))
        )
        password_input.clear()
        password_input.send_keys("useFB2025!")

        time.sleep(2)

        login_button = wait.until(
            EC.element_to_be_clickable((By.NAME, "login"))
        )
        login_button.click()

        # wait.until(EC.url_contains("facebook.com"))
        # browser.visit(url)

    except Exception as e:
        print("Login skipped or already authenticated:", e)
        browser.visit(url)

    time.sleep(5)
    print("GOT TO URL")
    # Gentle scrolling
    for _ in range(5):
        browser.execute_script("window.scrollBy(0, 800);")
        time.sleep(3)
    
    print("SUCCESSFULLY SCROLLED")

    time.sleep(30)  # inspect manually


if __name__ == "__main__":
    main()