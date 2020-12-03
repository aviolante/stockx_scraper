import json
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# read in json url list
with open('jordan_stockx_url_list.txt', 'r') as f:
    jordan_stockx_url_list = json.loads(f.read())


def replace_all_chars(text, chars_to_replace="$()%,", replace_chars_with=""):
    """ replace characters for cleaner results """
    for char in chars_to_replace:
        text = text.replace(char, replace_chars_with)
    return text


# run and collect data
sneaker_list_data = []
brand = "jordan"
driver = webdriver.Firefox()

for url in jordan_stockx_url_list:

    # get url and pause
    driver.get(url)
    time.sleep(5.5)

    content = driver.page_source
    soup = BeautifulSoup(content, 'lxml')

    # get current url and skip if 404
    if driver.current_url == 'https://stockx.com/404':
        continue

    else:
        # get soup
        content = driver.page_source
        soup = BeautifulSoup(content, 'lxml')

        # prod name
        prod_name = soup.find('h1').string.lower()

        # url
        page_url = url

        # condition
        if soup.find('div', class_='header-stat') == None:
            condition = '--'
        else:
            condition = soup.find('div', class_='header-stat').text.split(':')[1]

        # last sale
        if soup.find('div', class_='sale-value') == None:
            last_sale = '--'
        else:
            last_sale = replace_all_chars(soup.find('div', class_='sale-value').text)

        # last sale size, handle NoneType return
        if soup.find('span', class_='bid-ask-sizes') == None:
            last_sale_size = '--'
        else:
            last_sale_size = soup.find('span', class_='bid-ask-sizes').text.split(' ')[1]

        # lowest ask
        if soup.find('div', class_='bid bid-button-b') == None:
            lowest_ask = '--'
        else:
            lowest_ask = replace_all_chars(
                soup.find('div', class_='bid bid-button-b').find('div', class_='stats').text.strip('Lowest Ask'))

        # highest bid
        if soup.find('div', class_='ask ask-button-b') == None:
            highest_bid = '--'
        else:
            highest_bid = replace_all_chars(
                soup.find('div', class_='ask ask-button-b').find('div', class_='stats').text.strip('Highest Bid'))

        # since last sale dollar amount
        since_last_sale_dollar = replace_all_chars(soup.select_one('div.dollar').text)

        # since last sale percent amount (%)
        since_last_sale_percent = replace_all_chars(soup.select_one('div.percentage').text)

        # product info: colorway, retail price, release date
        prod_info = soup.find_all('div', class_='detail')

        # prefill in case of missing results below
        colorway = '--'
        retail_price = '--'
        release_date = '--'

        for info in prod_info:
            # pass style
            if info.get_text().split(' ')[0] == 'Style':
                pass
            elif info.get_text().split(' ')[0] == 'Colorway':
                colorway = info.get_text().replace('Colorway ', '').strip()
            elif info.get_text().split(' ')[0] == 'Retail':
                retail_price = replace_all_chars(info.get_text().split(' ')[2].strip(''))
            elif info.get_text().split(' ')[0] == 'Release':
                release_date = info.get_text().split(' ')[2].strip()

        # 52 week high
        high_52_week = replace_all_chars(soup.find('div', class_='value-container').text.split(' ')[1])

        # 52 week low
        low_52_week = replace_all_chars(soup.find('div', class_='value-container').text.split(' ')[4])

        # 12 month trade range low
        low_12_month_trade = replace_all_chars(soup.find('div', class_='ds-range value-container').text.split(' ')[0])

        # 12 month trade range high
        high_12_month_trade = replace_all_chars(soup.find('div', class_='ds-range value-container').text.split(' ')[2])

        # volatility
        volatility = replace_all_chars(soup.find('li', class_='volatility-col market-down').text.strip('Volatility'))

        # market information (12 month - num sales, price premium, avg sale price)
        market_info = soup.find_all('div', class_='gauge-container')

        for m in market_info:
            if m.text.split(' ')[0] == '#':
                num_sales_12_month = m.text.strip('# of Sales')
            elif m.text.split(' ')[0] == 'Price':
                price_premium_12_month = m.text.strip('Price Premium(Over Original Retail Price)%')
            elif m.text.split(' ')[0] == 'Average':
                avg_sale_price_12_month = m.text.strip('Average Sale Price$,')

        id_counter = jordan_stockx_url_list.index(url)

        sneaker_list_data.append({
            "id": id_counter,
            "brand": brand,
            "product_name": prod_name,
            "page_url": page_url,
            "condition": condition,
            "last_sale": last_sale,
            "last_sale_size": last_sale_size,
            "lowest_ask": lowest_ask,
            "highest_bid": highest_bid,
            "since_last_sale_dollar": since_last_sale_dollar,
            "since_last_sale_percent": since_last_sale_percent,
            "colorway": colorway,
            "retail_price": retail_price,
            "release_date": release_date,
            "high_52_week": high_52_week,
            "low_52_week": low_52_week,
            "low_12_month_trade": low_12_month_trade,
            "high_12_month_trade": high_12_month_trade,
            "volatility": volatility,
            "num_sales_12_month": num_sales_12_month,
            "price_premium_12_month": price_premium_12_month,
            "avg_sale_price_12_month": avg_sale_price_12_month
        })

        print(f'Progress: {id_counter} of {len(jordan_stockx_url_list)} Completed')


# save out data
with open('jordan_data.txt', 'w') as f:
    f.write(json.dumps(sneaker_list_data))
