import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# read in json url list
with open('nike_stockx_url_list.txt', 'r') as f:
    nike_stockx_url_list = json.loads(f.read())


# run and collect data
sneaker_images = []

driver = webdriver.Chrome(executable_path='./chromedriver')

for url in nike_stockx_url_list:

    # get url and pause
    driver.get(url)

    # get current url is 404 skip
    if driver.current_url == 'https://stockx.com/404':
        continue

    else:
        wait = WebDriverWait(driver, 10)

        prod_name = wait.until(EC.visibility_of_element_located((By.XPATH, "//h1[@class='name']"))).text

        img_src = wait.until(EC.visibility_of_element_located((
            By.XPATH, "//img[@data-testid='product-detail-image']"))).get_attribute('src')

        id_counter = nike_stockx_url_list.index(url)

        sneaker_images.append({
            "id": id_counter,
            "url": url,
            "product_name": prod_name,
            "image_url": img_src
        })

        print(f'Progress: {id_counter} of {len(nike_stockx_url_list)} Completed')


# # save out data
with open('nike_image_data.txt', 'w') as f:
    f.write(json.dumps(sneaker_images))



