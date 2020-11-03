## StockX Scraper
A program to get all StockX URL's and then scrape the info from each given URL. This is currently a work in progress with several steps being done manually due to time constraints.

### About
These scripts allow a 2-step approach for:
1) Getting all URL's by brand, make, and year
    - Currently, I split up brands vs loop through all due to time constraint. Outputs 3 json files for Nike, adi, and Jordan
    - Removed Jordan Off White "Make" to save time

2) From the list of URL's scrape all information in 2 steps. I broke out page and sales history components:
    - Currently, looping through brands individually (each of the 3 json files from above) vs all combined
    - Step 1: Use `02-product-scraper-no-history.py` to collect page level information for each URL
    - Step 2: Use `02-product-scraper-history-only.py` to collect page level sales history data found within sales history pop up tab 

Currently the process to scrape all URL's and product info is very time consuming. Also, there is an occasional "Verify" button that may come up that I've just manually clicked for now.

The product sales history script `02-product-scraper-history-only.py` is also very time consuming due to some products having a lot of history.

### Dependencies
```python
time
json
pandas
bs4
selenium
```

