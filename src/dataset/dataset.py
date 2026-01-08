import pandas as pd
import re
from sklearn.model_selection import train_test_split

def create_splits():
    df = pd.read_csv("data/processed/electric_guitar_listings_clean.csv")

    def extract_brand(title):
        brands = [
            "Gibson",
            "Fender",
            "PRS",
            "Gretsch",
            "Ibanez",
            "Schecter",
            "Epiphone",
            "Jackson",
            "LTD",
            "Yamaha",
            "Squier",
            "Donner"
        ]
        for brand in brands:
            if brand.lower() in title.lower():
                return brand
        return "Other"

    def extract_type(title):
        styles = [
            "Telecaster",
            "Stratocaster",
            "Les Paul",
            "Jazzmaster",
            "Jaguar",
            "SG",
            "Semi-Hollow",
            "Hollow",
            "Solid"
        ]
        for style in styles:
            if style.lower() in title.lower():
                return style
        return "Other"

    def extract_origin(title):
        title = title.lower()
        if "usa" in title or "american" in title:
            return "USA"
        if "mexico" in title or "mim" in title:
            return "Mexico"
        if "japan" in title or "mij" in title:
            return "Japan"
        if "korea" in title:
            return "Korea"
        if "china" in title or "indonesia" in title:
            return "Asia"
        return "Unknown"

    def extract_series(title):
        series = {
            "american professional": "American Pro",
            "american standard": "American Standard",
            "custom shop": "Custom Shop",
            "player": "Player",
            "vintera": "Vintera",
            "standard": "Standard",
            "studio": "Studio",
            "tribute": "Tribute"
        }
        t = title.lower()
        for k, v in series.items():
            if k in t:
                return v
        return "Other"


    def extract_year(title):
        match = re.search(r'(19[5-9]\d|20[0-2]\d)', title)
        if match:
            return int(match.group())
        return None


    df['brand'] = df['title'].apply(extract_brand)
    df['style'] = df['title'].apply(extract_type)
    df['origin'] = df['title'].apply(extract_origin)
    df['series'] = df['title'].apply(extract_series)
    df['year'] = df['title'].apply(extract_year)
    df['decade'] = (df['year'] // 10) * 10
    df['decade'] = df['decade'].fillna(0)
    df['discount_pct'] = ((df['original_price'] - df['price']) / df['original_price']).fillna(0)



    # Convert categorical features to numerical using one-hot encoding
    categorical_features = ['brand', 'condition', 'style', 'series', 'origin']
    df = pd.get_dummies(df, columns=categorical_features, drop_first=True)

    # Remove rows with missing price
    df = df[df['price'].notnull()]

    X = df.drop(columns=['price', 'itemId', 'title', 'url', 'location', 'original_price', 'discount_amount', 'currency', 'year'])
    y = df['price']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    create_splits()