import pandas as pd
import re
from sklearn.model_selection import train_test_split

BRANDS = [
    "Gibson", "Fender", "PRS", "Gretsch", "Ibanez",
    "Schecter", "Epiphone", "Jackson", "LTD", 
    "Yamaha", "Squier", "Donner"
]

TYPES = [
    "Telecaster", "Stratocaster", "Les Paul", "Jazzmaster", "Jaguar",
    "SG", "Firebird", "Explorer", "Modern Player Telecaster",
    "American Performer Telecaster", "American Performer Jazzmaster",
    "Player Plus Telecaster", "Player II Stratocaster", "Standard Stratocaster",
    "Standard Telecaster", "Classic Player Jazzmaster", "Standard Strat",
    "Stratacoustic", "Dot Studio", "Dot CH", "ES-339", "EA-250",
    "SL Les Paul", "Les Paul Standard Pro", "Les Paul Prophecy",
    "Les Paul Studio", "Les Paul Standard 60s Quilt", "Les Paul Special Plus",
    "Les Paul 120th Anniversary", "Limited Edition", "Special Edition",
    "SE Zach Myers", "PRS SE Special", "AlleyKat", "Firebird Studio",
    "Kurt Cobain NOS Jaguar", "Chris Shiflett Telecaster Deluxe",
    "JTK30H-BK Jet King Standard", "AF151 Aged Whiskey Burst",
    "Ibanez AS Series Artcore Expressionist", "Epiphone SG Custom Shop"
]

SERIES = {
    "american performer": "American Performer",
    "american professional": "American Pro",
    "american standard": "American Standard",
    "player plus": "Player Plus",
    "player ii": "Player II",
    "player": "Player",
    "classic player": "Classic Player",
    "modern player": "Modern Player",
    "vintera": "Vintera",
    "standard": "Standard",
    "studio": "Studio",
    "tribute": "Tribute",
    "custom shop": "Custom Shop",
    "limited edition": "Limited Edition",
    "special edition": "Special Edition",
    "sg custom shop": "SG Custom Shop",
    "zach myers": "Zach Myers",
    "dot": "Dot",
    "es-339": "ES-339",
    "ea-250": "EA-250",
    "sl les paul": "SL Les Paul",
    "alleykat": "AlleyKat",
    "firebird studio": "Firebird Studio",
    "les paul": "Les Paul",
    "explorer": "Explorer",
    "ibanez as series": "AS Series",
    "af151": "AF151",
    "jtk30h-bk": "Jet King",
    "stratacoustic": "Stratacoustic"
}

ORIGINS = {
    "USA": ["usa", "american"],
    "Mexico": ["mexico", "mim"],
    "Japan": ["japan", "mij"],
    "Korea": ["korea"],
    "Asia": ["china", "indonesia"]
}



def extract_brand(title):
        for brand in BRANDS:
            if brand.lower() in title.lower():
                return brand
        return "Other"

def extract_type(title):
    t = title.lower()
    found = [style for style in TYPES if style.lower() in t]
    return found if found else ["Other"]

def extract_origin(title):
    t = title.lower()
    for country, keywords in ORIGINS.items():
        if any(k in t for k in keywords):
            return country
    return "Other"


def extract_series(title):
    t = title.lower()
    found = []
    for k, v in SERIES.items():
        if k in t:
            found.append(v)
    
    return found if found else ["Other"]


def extract_year(title):
    match = re.search(r'(19[5-9]\d|20[0-2]\d)', title)
    if match:
        return int(match.group())
    return None

def parse_title(df: pd.DataFrame):
    df['brand'] = df['title'].apply(extract_brand)
    df['style'] = df['title'].apply(extract_type)
    df['origin'] = df['title'].apply(extract_origin)
    df['series'] = df['title'].apply(extract_series)
    df['year'] = df['title'].apply(extract_year)
    df['decade'] = (df['year'] // 10) * 10
    df['decade'] = df['decade'].fillna(0)

    for style in TYPES:
        df[f"type_{style}"] = df["style"].apply(lambda x: int(style in x))

    for s in SERIES.values():
        df[f"series_{s}"] = df["series"].apply(lambda x: int(s in x))

    return df

def create_splits():
    df = pd.read_csv("data/processed/electric_guitar_listings_clean.csv")

    df = parse_title(df)
    df['discount_pct'] = ((df['original_price'] - df['price']) / df['original_price']).fillna(0)

    # Convert categorical features to numerical using one-hot encoding
    categorical_features = ['brand', 'condition', 'origin']
    df = pd.get_dummies(df, columns=categorical_features, drop_first=True)
    with open("titles.txt", "w", encoding="utf-8") as f:
        for title in df["title"][:500]:
            f.write(str(title) + "\n")

    # Remove rows with missing price
    df = df[df['price'].notnull()]

    X = df.drop(columns=['price', 'itemId', 'title', 'url', 'location', 'original_price', 'discount_amount', 'currency', 'year', 'style', 'series'])
    y = df['price']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    create_splits()