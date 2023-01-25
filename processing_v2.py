'''
Google Map Scraper Using Selenium
Code By Nikhil Rathour
17 July, 2022
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException  
import csv
import time
from bs4 import BeautifulSoup as bs


Keyword= input("Enter Keyword: ")
city = input('Enter city name: ')
search = (Keyword + 'in' + city)
pages = 2

header = ["title", "address", "website", "phone","profiles"]
data = []

        
options = webdriver.ChromeOptions()
options.headless = True
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options)

driver.get('https://www.google.com')

driver.implicitly_wait(2)
driver.find_element(By.NAME,"q").send_keys(search + Keys.ENTER)
more = driver.find_element(By.TAG_NAME,"g-more-link")
more_btn = more.find_element(By.TAG_NAME,"a")
more_btn.click()
time.sleep(10)
def fetch():
    for page in range(2, pages+1):
        elements = driver.find_elements(By.CSS_SELECTOR, 'div#search a[class="vwVdIc wzN8Ac rllt__link a-no-hover-decoration"')
        counter = 1

        for element in elements:
            data_cid = element.get_attribute('data-cid')
            element.click()
            print('item click... 5 seconds...')
            time.sleep(3)

            html = driver.page_source
            soup = bs(html,'html.parser')

            #image
            # try:
            #     temp_obj = driver.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/location/location:media"] > div > a > div')

            #     if len(temp_obj.get_attribute('style')) > 0:
            #         image = temp_obj.get_attribute('style')
            #         if 'background' in image:
            #             image = image.replace('background-image: url("','')
            #             image = image.replace('"','')
            #             image = image.replace(');','')
            # except Exception:
            #     image =""
            # print('image:', image)
            
            #title
            title = soup.find('div', class_='SPZz6b')
            print('title: ', title.string)

            #address
            try:
                temp_obj = soup.find('span', class_='LrzXr')
                address = temp_obj.string
            except Exception:
                address =""
            print ('address: ',address[0:8],'..')

            #website
            try:
                temp_obj = soup.find('a', class_='dHS6jb', href=True)
                if len(temp_obj['href']) > 0:
                    website = (temp_obj['href'])
            except Exception:
                website =""

            print('website:', website)

            #phone
            try:
                temp_obj = soup.find('span', class_='zdqRlf')
                print('phone:', temp_obj.string)
                phone = temp_obj.string
            except Exception :
                phone = ""

            # social profiles
            profiles=""
            for s_count in range (1, 6):
                try:
                    temp_obj = driver.find_element(By.CSS_SELECTOR, 'div[data-attrid="kc:/common/topic:social media presence"] div:nth-child(2) > div:nth-child(' + str(s_count) + ') > div > g-link > a')
                    if len(temp_obj.get_attribute('href')) > 0:
                        profiles_str = temp_obj.get_attribute('href')
                except Exception:
                    profiles_str = ""
                    break
                profiles += "<br/>" + profiles_str
            print('profiles: ', profiles)

            try:
            #print(counter, data_cid, title.text, address, website, phone,rating,reviews,image,category,timing,description,profiles)
                row = [title.string, address, website, phone,profiles]
                with open('gmap.csv', 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(row)
                    
                counter+=1
            except Exception:
                pass

        try:
            
            page_button = driver.find_element(By.ID,'pnnext')
            #page_button = driver.find_element(By.CSS_SELECTOR, 'a[aria-label="Page ' + str(page) + '"]')
            page_button.click()
            print('page click... 10 seconds...')
            time.sleep(10)
        except Exception:
            break
        fetch()
        
fetch()
for i in range (5):
    print("hello world")
for i in range(5):
    print("hello world")
