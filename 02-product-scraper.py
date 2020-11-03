import json
from config import creds
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import time
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# read in json url list
with open('adidas_stockx_url_list.txt', 'r') as f:
    adidas_stockx_url_list = json.loads(f.read())

# len(jordan_stockx_url_list)     22,803
# len(nike_stockx_url_list)       13,809
# len(adidas_stockx_url_list)     5,476

def attempt_login(driver):
    try:
        # log in
        driver.find_element_by_id("nav-signup").click()
        time.sleep(3)

        driver.find_element_by_id("login-toggle").click()

        # add username
        username = driver.find_element_by_id("email-login")
        username.clear()
        username.send_keys(creds.EMAIL)

        # add password
        password = driver.find_element_by_id("password-login")
        password.clear()
        password.send_keys(creds.PASSWORD)

        # log in button
        driver.find_element_by_id("btn-login").click()
        time.sleep(3)
    except:
        pass


def replace_all_chars(text, chars_to_replace="$()%,", replace_chars_with=""):
    """ replace characters for cleaner results """
    for char in chars_to_replace:
        text = text.replace(char, replace_chars_with)
    return text


def get_sales_history():
    """ get sales history data from sales history table interaction """
    sales_hist_data = []

    try:
        # click 'View All Sales' text link
        driver.find_element_by_xpath(".//div[@class='market-history-sales']/a[@class='all']").click()

        # log in
        driver.find_element_by_id("nav-signup").click()

        # add username
        username = driver.find_element_by_id("email-login")
        username.clear()
        username.send_keys(creds.EMAIL)

        # add password
        password = driver.find_element_by_id("password-login")
        password.clear()
        password.send_keys(creds.PASSWORD)
    except:
        pass

    while True:
        try:
            # If 'Load More' Appears Click Button
            driver.find_element_by_xpath(
                ".//div[@class='latest-sales-container']/button[@class='button button-block button-white']").click()
            # WebDriverWait(driver, 20).until(EC.element_to_be_clickable(
            #     (By.XPATH, "//button[@class='button button-block button-white' and text()='Load More']"))).click()
            print("Loading More")
        except TimeoutException:
            print("Reached Bottom of Page")
            break

    content = driver.page_source
    soup = BeautifulSoup(content, 'lxml')

    div = soup.find('div', class_='latest-sales-container')

    for td in div.find_all('td'):
        sales_hist_data.append(td.text)

    return sales_hist_data


# run and collect data
sneaker_list_data = []
id_counter = 0
driver = webdriver.Firefox()

for url in adidas_stockx_url_list:

    driver.get(url)

    # login and wait
    attempt_login(driver)
    time.sleep(2)

    # get soup
    content = driver.page_source
    soup = BeautifulSoup(content, 'lxml')

    # prod name
    prod_name = soup.find('h1').string.lower()

    # condition
    condition = soup.find('div', class_='header-stat').text.split(':')[1]

    # last sale
    last_sale = replace_all_chars(soup.find('div', class_='sale-value').text)

    # last sale size
    last_sale_size = soup.find('span', class_='bid-ask-sizes').text.split(' ')[1]

    # lowest ask
    lowest_ask = replace_all_chars(
        soup.find('div', class_='bid bid-button-b').find('div', class_='en-us stat-value stat-small').text)

    # highest bid
    highest_bid = replace_all_chars(
        soup.find('div', class_='ask ask-button-b').find('div', class_='en-us stat-value stat-small').text)

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

    sales_hist_data = get_sales_history()

    id_counter = id_counter + 1

    sneaker_list_data.append({
        "id": id_counter,
        "product_name": prod_name,
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
        "num_sales_12_month":num_sales_12_month,
        "price_premium_12_month":price_premium_12_month,
        "avg_sale_price_12_month":avg_sale_price_12_month,
        "sales_hist_data": sales_hist_data
    })

    print(f'Progress: {id_counter} of {len(adidas_stockx_url_list)} Completed')

    time.sleep(3)


first_data = pd.DataFrame(sneaker_list_data)

first_data.to_csv('./first_adi_data.csv', index=False)

