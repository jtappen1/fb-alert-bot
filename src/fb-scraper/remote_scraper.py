from collections import defaultdict
import json
import pickle
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup as soup
import time
import pandas as pd
from src.dataset.dataset import parse_title

def human_typing_delay(mean=2.5, std_dev=1.0, min_delay=0.5, max_delay=5.0):
    """
    Returns a random delay in seconds that mimics human typing.
    - mean: average delay
    - std_dev: how variable the delay is
    - min_delay / max_delay: clamp values
    """
    delay = random.gauss(mean, std_dev)
    # clamp the value to a reasonable range
    delay = max(min_delay, min(max_delay, delay))
    return delay

def human_scroll(driver, total_scrolls=20, min_step=300, max_step=700):
    """
    Scrolls the page like a human.
    - total_scrolls: number of scroll actions
    - min_step/max_step: pixel step size per scroll
    """
    for _ in range(total_scrolls):
        # Random scroll amount
        scroll_amount = random.randint(min_step, max_step)
        
        # Scroll by that amount
        driver.execute_script(f"window.scrollBy(0, {scroll_amount});")
        
        # Random pause
        time.sleep(human_typing_delay(mean=1.5, std_dev=0.7, min_delay=0.5, max_delay=3.0))

        if random.random() < 0.1:  # 10% chance
            driver.execute_script("window.scrollBy(0, -100);")
            time.sleep(human_typing_delay(mean=1.5, std_dev=0.7, min_delay=0.5, max_delay=3.0))


def main():

    chrome_options = Options()
    chrome_options.add_experimental_option(
        "debuggerAddress", "127.0.0.1:9222"
    )

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    base_url = 'https://www.facebook.com/marketplace/philly/search?'

    min_price = 200
    max_price = 1000
    days_since_listed = 1

    url = f"{base_url}minPrice={min_price}&maxPrice={max_price}&daysSinceListed={days_since_listed}&query=electric%20guitars&exact=false"
    driver.get(url)

    # Time given for the initial page to load 
    time.sleep(human_typing_delay(mean=5, std_dev=2, min_delay=3, max_delay=10))
    print("Page Loaded!")

def scrape(driver):
    print("Starting Scroll")
    # Scroll to the bottom of the page
    human_scroll(driver, total_scrolls=5, min_step=200, max_step=600)

    print("Finished Scroll")

    html = driver.page_source

    with open("marketplace_page.html", "w", encoding="utf-8") as f:
        f.write(html)

def parse_price(price: str):
    price = price.lower()
    return float(price.replace("$", "").replace(",",""))


def find_listing_container(tag):
    return tag.find_parent(
        "div",
        class_=lambda c: c and "x1r8uery" in c
    )


def parse_listings():
    with open("marketplace_page.html", "r", encoding='utf-8') as f:
        saved_html = f.read()

    listings = defaultdict(lambda: {
        "title": None,
        "original_price": None,
        "price": None
    })

    market_soup = soup(saved_html, "html.parser")

    titles_div = market_soup.find_all('span', class_='x1lliihq x6ikm8r x10wlt62 x1n2onr6')

    for span in titles_div:
        container = find_listing_container(span)
        if not container:
            continue
        listings[id(container)]["title"] = span.text.strip()

    discount_div = market_soup.find_all('span', class_= "x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x1lkfr7t x1lbecb7 xk50ysn xi81zsa")

    for span in discount_div:
        container = find_listing_container(span)
        if not container:
            continue
        listings[id(container)]["original_price"] = parse_price(span.text.strip())
    
    prices_div = market_soup.find_all('span', class_="x193iq5w xeuugli x13faqbe x1vvkbs xlh3980 xvmahel x1n0sxbx x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x3x7a5m x1lkfr7t x1lbecb7 x1s688f xzsf02u")
    for span in prices_div:
        container = find_listing_container(span)
        if not container:
            continue
        listings[id(container)]["price"] = parse_price(span.text.strip())
    
    df = pd.DataFrame(listings.values())
    df = parse_title(df)

    df['discount_pct'] = ((df['original_price'] - df['price']) / df['original_price']).fillna(0)

    # Convert categorical features to numerical using one-hot encoding
    categorical_features = ['brand', 'style', 'series', 'origin']
    df_filtered = df[(df[categorical_features] != 'Other').any(axis=1)]
    print(df_filtered)

    # Remove rows with missing price
    df_filtered = df_filtered[df_filtered['price'].notnull()]

    df_encoded = pd.get_dummies(df_filtered, columns=categorical_features, drop_first=True)

    X = df_encoded.drop(columns=['price', 'title', 'year', 'original_price'])

    with open('models/random_forest_model.pkl', "rb") as f:
        model = pickle.load(f)
    
    with open("models/random_forest_model_features.pkl", "rb") as f:
        feature_columns = pickle.load(f)

    X = X.reindex(columns=feature_columns, fill_value=0)

    y_pred = model.predict(X)

    df_encoded['predicted_price'] = y_pred
    df_encoded['price_diff_pct'] = (df_encoded['predicted_price'] - df_encoded['price']) / df_encoded['predicted_price'] * 100

    alert_threshold_pct = 40  # alert if listing is ≥40% cheaper than predicted
    alerts = df_encoded[df_encoded['price_diff_pct'] >= alert_threshold_pct]

    print(alerts[['title', 'price', 'predicted_price', 'price_diff_pct']])


if __name__ == "__main__":
    parse_listings()




