import time
from bs4 import BeautifulSoup
from selenium import webdriver
import json


def get_types(brand):
    # return make within each brand (air max, foamposite, lebron, etc)
    type_list = []
    # open browser
    driver = webdriver.Firefox()
    driver.get("https://stockx.com/{}".format(brand))
    # click 'Show More' button to view all makes
    btn = driver.find_element_by_xpath(".//div[@class='subcategory show-more']")
    btn.click()
    elems = driver.find_elements_by_xpath("//div[@class='subcategoryList']/div[@class='form-group']/div[@class='checkbox subcategory']")
    for elem in elems:
        item = elem.find_element_by_tag_name('label').get_attribute('innerHTML')
        # account for unique identifiers
        if len(item.split(' ')) > 0:
            item = '-'.join(item.split(' '))
        if item == 'Other':
            item = 'footwear'
        if item.isdigit():
            item = 'air-jordan-'+item
        type_list.append(item.lower())
    driver.quit()
    print(type_list)
    return type_list


def return_urls(soup):
    # return all urls found on a product search page
    url_list = []
    for div in soup.findAll('div', attrs={'class': 'tile css-1bonzt1 e1yt6rrx0'}):
        links = div.findAll('a')
        for a in links:
            url_list.append("http://www.stockx.com" + a['href'])
    return url_list


jordan_list = ['air-jordan-1', 'air-jordan-2', 'air-jordan-3', 'air-jordan-4',
               'air-jordan-5', 'air-jordan-6', 'air-jordan-7', 'air-jordan-8', 'air-jordan-9',
               'air-jordan-10', 'air-jordan-11', 'air-jordan-12', 'air-jordan-13', 'air-jordan-14',
               'air-jordan-15', 'air-jordan-16', 'air-jordan-17', 'air-jordan-18', 'air-jordan-19',
               'air-jordan-20', 'air-jordan-21', 'air-jordan-22', 'air-jordan-23', 'air-jordan-24',
               'air-jordan-25', 'air-jordan-26', 'air-jordan-27', 'air-jordan-28', 'air-jordan-29',
               'air-jordan-30', 'air-jordan-31', 'air-jordan-32', 'air-jordan-33', 'air-jordan-34',
               'packs', 'spizike', 'footwear']


def page_information():
    # go through brand, make, year and page to scrape all product URLs
    # brands = ['nike', 'retro-jordans', 'adidas']
    brands = ['retro-jordans']
    years = ['before-2001', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009',
             '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020']

    # max 25 pages to grab
    pages = [str(x) for x in range(1,26)]

    url_list = []

    # open URL with webdriver
    driver = webdriver.Firefox()

    for b in brands:
        # for t in get_types(b):
        for t in jordan_list:
            for y in years:
                for p in pages:
                    print("Starting "+b.capitalize()+" - "+t.capitalize()+" "+y)
                    url = "https://stockx.com/{}/{}".format(b,t)+"?years="+y+"&page="+p
                    driver.get(url)
                    content = driver.page_source
                    soup = BeautifulSoup(content)
                    time.sleep(5)
                    print("Beginning Extraction")
                    # check if page has no results
                    try:
                        no_result = soup.findAll('div', {'class': 'no-results'})[0].text
                        no_result_check = no_result.split(' ')[0]
                        if no_result_check == 'NOTHING':
                            print('No result found. Going to next page')
                            break
                        else:
                            continue
                    except:
                        pass
                    # find url for all products
                    url_list += return_urls(soup)
                    print(f'Total Sneaker Count: {len(url_list)}')
    driver.quit()
    return url_list

jordan_stockx_url_list = page_information()

with open('jordan_stockx_url_list.txt', 'w') as f:
    f.write(json.dumps(jordan_stockx_url_list))

