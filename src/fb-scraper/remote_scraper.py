from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

chrome_options = Options()
chrome_options.add_experimental_option(
    "debuggerAddress", "127.0.0.1:9222"
)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)
base_url = 'https://www.facebook.com/marketplace/philly/search?'
initial_url = "https://www.facebook.com/login/device-based/regular/login/"

min_price = 200
max_price = 1000
days_since_listed = 1

url = f"{base_url}minPrice={min_price}&maxPrice={max_price}&daysSinceListed={days_since_listed}&query=electric%20guitars&exact=false"
driver.get(url)
print("Successfully Worked!!")
time.sleep(30)

