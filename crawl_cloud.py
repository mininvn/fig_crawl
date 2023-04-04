import time 
# from selenium import webdriver 
# from selenium.webdriver import Chrome 
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from urllib.parse import urlparse
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
def crawl(url):
    driver.get(url) 
    time.sleep(5)
    item_about = driver.find_elements(By.CLASS_NAME, value = "item-about")[0]
    item_data_dls = item_about.find_elements(By.TAG_NAME, value = "dl")
    res = {}
    for dl in item_data_dls:
        dts = dl.find_elements(By.TAG_NAME, value = "dt")
        dds = dl.find_elements(By.TAG_NAME, value = "dd")
        for index in range(len(dts)):
            res[dts[index].text] = dds[index].text

    for key in res:
        if ("\n" in res[key]):
            data = res[key]
            res[key] = {}
            data = data.split("\n")
            for value in data:
                # print(value)
                value = value.split(":")
                res[key][value[0]] = value[1] if len(value) == 2 else value[0]
    return res

urls_file = "urls.txt"
crawled_urls_file = "crawled_urls.txt"
result_file = "result.csv"
required_rows = {
    "Release Date": True,
    "List Price": True,
    "Shop Code": True,
    "Character Name": True,
    "Specifications": {
        "Scale": True,
        "Size": True
    }
}

def read_urls():
    f = open(urls_file)
    urls = f.read()
    urls = urls.split("\n")
    return urls

def produce_headings(obj):
    res = ""
    for key, value in obj.items():
        if (value == True):
            res += key
            res += ","
        elif (isinstance(value, dict)):
            res += produce_headings(value)
            res += ","
    res = res[:-1]
    return res

def handle_price(data):
    return data.replace(",", ".")

def convert_res_to_csv_row(res):
    csv_row = ""

    handle_rows = {
        "List Price": handle_price
    }

    for key, value in required_rows.items():
        if (value == True):
            data = res[key]
            if (key in handle_rows):
                data = handle_rows[key](data)
            data = data.strip()
            csv_row += data
            csv_row += ","
        elif (isinstance(value, dict)):
            for key_inside, value_inside in value.items():
                if (value_inside == True):
                    data = res[key][key_inside]
                    data = data.strip()
                    csv_row += data
                    csv_row += ","
    csv_row = csv_row[:-1]
    return csv_row

def append_result(row):
    try:
        f = open(result_file)
        f.close()
        f = open(result_file, "a")
        f.write(row + "\n")
        f.close()
    except:
        f = open(result_file, "a")
        f.write(produce_headings(required_rows) + "\n")
        f.write(row + "\n")
        f.close()

def handle_url(res):
    try:
        csv_row = convert_res_to_csv_row(res)
        append_result(csv_row)
        return True
    except:
        return False
    
def overwrite_urls_file(urls):
    try:
        text = ""
        for url in urls:
            text += url 
            text += "\n"
        f = open(urls_file, "w")
        f.write(text)
        f.close()
    except:
        print("Cloz gi do hong r")

def save_crawled_url(url):
    try:
        text = url
        text += "\n"
        f = open(crawled_urls_file, "a")
        f.write(text)
        f.close()
    except:
        print("Cloz gi do hong r")

def handle_urls(urls):
    failed_urls = []
    for url in urls:
        if not validate_url(url):
            failed_urls.append(url)
            print("Invalid url:", url)
            continue
        res = crawl(url)
        if (not handle_url(res)):
            failed_urls.append(url)
        else: 
            save_crawled_url(url)
    overwrite_urls_file(failed_urls)

def validate_url(url):
    try:
        result = urlparse(url)
        if all([result.scheme, result.netloc]):
            return True
        else:
            return False
    except:
        return False
    
urls = read_urls()
handle_urls(urls)