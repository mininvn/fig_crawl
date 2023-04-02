import time 
import json
import pandas as pd 
from selenium import webdriver 
from selenium.webdriver import Chrome 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
"""
Using cloudscraper (can't wait for the js loading)
# import cloudscraper
# scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
# a = scraper.get(url).text  # => "<!DOCTYPE html><html><head>..."
# print(a)
"""
url = "https://www.amiami.com/eng/detail/?gcode=FIGURE-152781" 

# start by defining the options 
options = uc.ChromeOptions() 
options.add_argument('--headless') # it's more scalable to work in headless mode 
# normally, selenium waits for all resources to download 
# we don't need it as the page also populated with the running javascript code. 
options.page_load_strategy = 'none' 
# this returns the path web driver downloaded 
chrome_path = ChromeDriverManager().install() 
chrome_service = Service(chrome_path) 
# pass the defined options and service objects to initialize the web driver 
driver = uc.Chrome(options=options, service=chrome_service) 
driver.implicitly_wait(5)
 
driver.get(url) 
time.sleep(3)
item_about = driver.find_elements(By.CLASS_NAME, value = "item-about")[0]
item_data_dls = item_about.find_elements(By.TAG_NAME, value = "dl")
res = {}
for dl in item_data_dls:
    dts = dl.find_elements(By.TAG_NAME, value = "dt")
    dds = dl.find_elements(By.TAG_NAME, value = "dd")
    for index in range(len(dts)):
        res[dts[index].text] = dds[index].text

f = open("original.txt", "w")
f.write(json.dumps(res))
f.close()

for key in res:
    if ("\n" in res[key]):
        data = res[key]
        res[key] = {}
        data = data.split("\n")
        for value in data:
            print(value)
            value = value.split(":")
            res[key][value[0]] = value[1] if len(value) == 2 else value[0]

f = open("res.json", "w")
f.write(json.dumps(res))
f.close()