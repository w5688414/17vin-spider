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

def get_car_series_info(browser,url):
    # url='http://www.17vin.com/series.html?p=YnJhbmQ96ZW_5a6J5qyn5bCa'
    print(url)
    browser.get(url)
    html = browser.page_source
    doc = pq(html)
    
    li= doc('li').items()
    list_data=[]
    for item in li:
        print(item)
        short_url=item('a').attr('href')
        if(short_url is None):
            continue
        url='http://www.17vin.com'+short_url
        brand_name=item.attr('title')
        if(brand_name=="" or brand_name is None):
            continue
        if(brand_name=='无epc目录数据'):
            brand_name=item('a').text()
        list_data.append([brand_name,url])

    return list_data

def write_to_csv(output_name,list_data):
    df=pd.DataFrame(list_data,columns=['title','url'])
    df.to_csv(output_name,index=False)

def get_series_urls():
    df=pd.read_csv('brand_url.csv')
    return df

def main():
    series_df=get_series_urls()
    # output_name='models_url.csv'
    os.makedirs('series_web',exist_ok=True)
    for index, row in series_df.iterrows():
        brand_name=row['brand_name']
        url=row['url']
        output_name=os.path.join('series_web',brand_name+'.csv')
        list_data=get_car_series_info(browser,url)
        write_to_csv(output_name,list_data)

    # brand_name='赫菲勒'
    # url='http://www.17vin.com/series.html?p=YnJhbmQ96LWr6I-y5YuS'
    # output_name=os.path.join('series_web',brand_name+'.csv')
    # list_data=get_car_series_info(browser,url)
    # write_to_csv(output_name,list_data)
    browser.close()

if __name__ == '__main__':
    main()