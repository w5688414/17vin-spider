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

browser = webdriver.Chrome()
wait = WebDriverWait(browser,20)

def get_url_encode(key,value):
    values={}
    values[key]=value
    KEYWORD=urllib.parse.urlencode(values)
    return KEYWORD

def get_car_series_info(browser):
    url='http://www.17vin.com/brand.html'
    print(url)
    browser.get(url)
    html = browser.page_source
    doc = pq(html)
    # //*[@id="slist_0"]/div[2]/ul/li[1]/a
    
    li= doc('li').items()
    list_data=[]
    for item in li:
        print(item)
        short_url=item('a').attr('href')
        if(short_url is None):
            continue
        url='http://www.17vin.com'+short_url
        brand_name=item('.abc_li_name').text()
        if(brand_name==""):
            continue
        # print(item('a').attr('href'))
        # print(item('.abc_li_name').text())
        list_data.append([brand_name,url])

    return list_data

def write_to_csv(output_name,list_data):
    df=pd.DataFrame(list_data,columns=['brand_name','url'])
    df.to_csv(output_name,index=False)

def main():
    output_name='brand_url.csv'
    list_data=get_car_series_info(browser)
    write_to_csv(output_name,list_data)
    browser.close()

if __name__ == '__main__':
    main()