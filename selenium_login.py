from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import time
import pandas as pd
import urllib.parse
import os

from bs4 import BeautifulSoup

# browser = webdriver.Chrome()
options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
browser = webdriver.Chrome(options=options)

wait = WebDriverWait(browser,20)

def get_url_encode(key,value):
    values={}
    values[key]=value
    KEYWORD=urllib.parse.urlencode(values)
    return KEYWORD

def get_car_series_info(browser,Mobile,Password):
    url='http://www.17vin.com/login'
    print(url)
    browser.get(url)

    browser.find_element_by_xpath('//*[@id="Mobile"]').send_keys(Mobile)
    browser.find_element_by_xpath('//*[@id="Password"]').send_keys(Password)

    # verify_code='http://www.17vin.com/common/verifyimage.aspx'
    time.sleep(10)

def write_to_csv(output_name,list_data):
    df=pd.DataFrame(list_data,columns=['title','url'])
    df.to_csv(output_name,index=False)

def main():
    output_name='models_url.csv'
    # Mobile=''
    Mobile=''
    Password=''
    get_car_series_info(browser,Mobile,Password)
    # write_to_csv(output_name,list_data)
    # browser.close()

if __name__ == '__main__':
    main()