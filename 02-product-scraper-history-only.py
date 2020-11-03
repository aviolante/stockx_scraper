import json
from config import creds
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import time
import pandas as pd

# read in json url list
with open('jordan_stockx_url_list.txt', 'r') as f:
    jordan_stockx_url_list = json.loads(f.read())

# len(jordan_stockx_url_list)     4,598
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
        print('Successful Log In!')
    except Exception:
        print('Already Logged In or Cant Log In')
        pass


def get_sales_history():
    """ get sales history data from sales history table interaction """

    # sales hist data
    sales_hist_data = []

    # check if sales data exists
    if driver.find_element_by_xpath(".//div[@class='latest-sales-container']").text.split()[0] == 'Nothing':
        sales_hist_data = '-'

    else:
        # if exists click 'View All Sales' text link
        # driver.find_element_by_xpath(".//div[@class='market-history-sales']/a[@class='all']").click()

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, ".//div[@class='market-history-sales']/a[@class='all']"))).click()

        # view page
        content = driver.page_source
        soup = BeautifulSoup(content, 'lxml')

        # max load button attempts for sales history tabular data
        max_loads = 15

        if soup.find('div', class_='modal-body').text == 'No Sales Available':
            sales_hist_data = '-'

        else:
            try:
                # find load button if exists
                loadingButton = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH,
                     ".//div[@class='latest-sales-container']/button[@class='button button-block button-white']")))

            except TimeoutException:
                loadingButton = False
                print('No load button exists')

            # loop till load button doesnt appear or max loads
            for _ in range(max_loads):
                while loadingButton:
                    try:
                        loadingButton.click()
                        time.sleep(2)
                        print("Loading Results")

                    except Exception:
                        print("Reached Bottom")
                        break

                else:
                    print('Skipped Loading Button')
                break

            # view newly loaded content of page
            content = driver.page_source
            soup = BeautifulSoup(content, 'lxml')
            div = soup.find('div', class_='latest-sales-container')

            # loop through and get all tabular data
            for td in div.find_all('td'):
                sales_hist_data.append(td.text)

            # append url to each record for later dataframe joining
            i = 0
            while i < len(sales_hist_data):
                sales_hist_data.insert(i, url)
                i += 5

    return sales_hist_data


# run and collect data
sneaker_list_data = []
id_counter = len(sneaker_list_data)
driver = webdriver.Firefox()

for url in jordan_stockx_url_list:

    driver.get(url)
    time.sleep(3)

    if driver.current_url == 'https://stockx.com/404':
        continue

    else:
        # login and wait
        attempt_login(driver)
        time.sleep(3)

        # sales history
        sales_hist_data = get_sales_history()

        sneaker_list_data.append(sales_hist_data)

        print(f'Progress: {id_counter} of {len(jordan_stockx_url_list)} Completed')

        id_counter += 1

        time.sleep(3)


# save out data to .txt and .csv
with open('jordan_data_history.txt', 'w') as f:
    f.write(json.dumps(sneaker_list_data))




