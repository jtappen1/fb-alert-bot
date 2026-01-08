# fb-alert-bot
Bot that checks Facebook Marketplace and sends an alert when good deals on guitars have been added.

## Scraping Steps:
Note: **Scraping can violate the FB TOS, which can result in account/IP bans.  Be aware and act accordingly**.  
These steps allow you to scrape FB using an active account.  It is suggested to make a shadow account.  
Create a remote Chrome session: 
```bash 
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/chrome-fb-profile"
```

## Models:
On the dataset of 5000 ebay guitar listings, the model performs accordingly:  
### Random Forest
```
Train RMSE: 36.24203013410519
Test  RMSE: 39.90399772229029
Train R2: 0.9582566894628349
Test  R2: 0.9457597166152396
```