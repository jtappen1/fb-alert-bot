from splinter import Browser
from bs4 import BeautifulSoup as soup
import re
import pandas as pd
import matplotlib.pyplot as plt
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def main():

    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir=/Users/jtappen/Library/Application Support/Google/Chrome")
    chrome_options.add_argument("--profile-directory=Profile 5")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--no-first-run")
    chrome_options.add_argument("--no-default-browser-check")
    chrome_options.add_argument("--disable-popup-blocking")
    
    print("About to launch Browser")
    browser = Browser(
        "chrome",
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    print("Browser Launched")

    base_url = 'https://www.facebook.com/marketplace/philly/search?'

    min_price = 200
    max_price = 1000
    days_since_listed = 1

    url = f"{base_url}minPrice={min_price}&maxPrice={max_price}&daysSinceListed={days_since_listed}&query=electric%20guitars&exact=false"
    print("Created URL")
    browser.visit("https://www.facebook.com/marketplace")
    # browser.visit(url)
    print("Visited URL")
    print(browser.url)
    # if browser.is_element_present_by_css('div[aria-label="Close"]', wait_time=10):
    #     # Click on the element once it's found
    #     browser.find_by_css('div[aria-label="Close"]').first.click()
    time.sleep(10)

    # Gentle scrolling
    for _ in range(5):
        browser.execute_script("window.scrollBy(0, 800);")
        time.sleep(3)

    time.sleep(30)  # inspect manually


if __name__ == "__main__":
    main()