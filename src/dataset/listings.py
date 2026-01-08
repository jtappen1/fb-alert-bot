import json
import os
import time
import requests
import base64
import yaml
import pandas as pd

yaml_path = "/Users/jtappen/Projects/fb-alert-bot/configs/ebay_dev_acc.yaml"

with open(yaml_path, "r") as f:
    config = yaml.safe_load(f)

CLIENT_ID = config["client_id"]
CLIENT_SECRET = config["cert_id"]

def get_env_token():
    token = os.getenv("EBAY_ACCESS_TOKEN")
    expires_at = os.getenv("EBAY_TOKEN_EXPIRES_AT")

    if not token or not expires_at:
        return None

    if time.time() > float(expires_at) - 300:
        return None

    return token


def request_new_token():
    auth = (CLIENT_ID, CLIENT_SECRET)

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope"
    }

    response = requests.post(
        "https://api.ebay.com/identity/v1/oauth2/token",
        headers=headers,
        data=data,
        auth=auth
    )

    response.raise_for_status()
    token_data = response.json()

    access_token = token_data["access_token"]
    expires_in = token_data["expires_in"]
    expires_at = time.time() + expires_in

    os.environ["EBAY_ACCESS_TOKEN"] = access_token
    os.environ["EBAY_TOKEN_EXPIRES_AT"] = str(expires_at)

    return access_token


def get_listings(access_token: str):
    os.makedirs("data/raw/ebay", exist_ok=True)

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    all_items = []
    continuation = None
    total_listings = 0
    while total_listings < 5000:
        params = {
            "q": "electric guitar (Fender,Gibson,Ibanez,PRS,Yamaha,Epiphone,Schecter) (Telecaster,Stratocaster,Tele,Strat,Hollow,Semi-Hollow,Solid,Les Paul,SG,Jazzmaster,Jaguar)",
            "filter": "conditionIds:{1000|3000},price:[300..1000],priceCurrency:USD",
            "limit": 50,
            "priceCurrency": "USD",
            "soldItems": "SOLD"
            }

        if continuation:
            params["continuation"] = continuation

        response = requests.get(
            "https://api.ebay.com/buy/browse/v1/item_summary/search",  
            headers=headers, 
            params=params
        )
        data = response.json()

        all_items.extend(data.get("itemSummaries", []))

        continuation = data.get("next")
        if not continuation:
            break
        total_listings += 50

        with open("data/raw/ebay/electric_guitar_page_clean.json", "w") as f:
            json.dump(data, f, indent=2)
        print(f"Processed {total_listings} entries")
    
    items = []
    for item in all_items:
        items.append({
            "itemId": item["itemId"],
            "title": item["title"],
            "price": float(item["price"]["value"]),
            "original_price": item.get("marketingPrice", {}).get("originalPrice", {}).get("value"),
            "discount_amount": item.get("marketingPrice", {}).get("discountAmount", {}).get("value"),
            "currency": item["price"]["currency"],
            "condition": item["conditionId"],
            "url": item["itemWebUrl"],
            "location": item.get("itemLocation", {}).get("country")
        })

    df = pd.DataFrame(items)
    output_file = "data/processed/electric_guitar_listings_clean.csv"

    if os.path.exists(output_file):
        df.to_csv(output_file, mode='a', header=False, index=False)
    else:
        df.to_csv(output_file, mode='w', header=True, index=False)

def get_access_token():
    token = get_env_token()
    if token:
        return token

    return request_new_token()



def main():
    access_token = get_access_token()
    get_listings(access_token=access_token)


if __name__ == "__main__":
    main()