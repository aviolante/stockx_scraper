## StockX Scraper
A program to get all StockX Product URL's and then scrape the info from each given URL. This is currently a work in progress with several steps being done manually due to time constraints.

### About
These scripts allow a 2-step approach for:
1) Getting all URL's by brand, make, and year
    - Currently, I split up brands vs loop through all due to time constraint. Outputs 3 files for Nike, adi, and Jordan

2) From the list of URL's scrape all information in 2 steps. I broke out page and sales history components:
    - Currently, looping through brands individually (each of the 3 files from above) vs all combined
    - Step 1: Use `02_product_scraper_no_history.py` to collect page level information for each product URL
    - Step 2: Use `03_product_scraper_history_only.py` to collect individual product level sales history found within sales history pop up tab 

Currently, the process to scrape all URL's and product info is very time-consuming. Also, there is an occasional "Verify" button that may come up that I've manually clicked for now just to bypass and keep moving forward.

The product sales history script `03_product_scraper_history_only.py` is also very time-consuming due to some products having <b>A LOT</b> of transaction history.

### Dependencies
```
time
json
pandas
bs4
selenium
```

