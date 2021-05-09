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
import glob
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

def get_car_series_info(url):
    # url='http://www.17vin.com/models.html?p=YnJhbmQ96ZW_5a6J5qyn5bCaJmNoYW5namlhPemVv-Wuieasp-WwmiZzZXJpZXM9Q1g3MA=='
    print(url)
    browser.get(url)
    html = browser.page_source
    print(html)
    soup = BeautifulSoup(html, "lxml")
    tables=soup.find_all('table')
    # print(tables)
    n=len(tables)
    for i in range(n): # table 0 没有数据
        # print(tables[i])
        list_data=[]
        for tr in tables[i].findAll('tr'):
            t=[]
            tds=tr.findAll('td')
            # print(tds)
            for td in tds:
                t.append(td.getText())
            if(len(tds)>0 and tds[-1].getText()!='无配件目录'):
                t.append(tds[-1].find('a')['href'])
            list_data.append(t)
        print(list_data)
        df=pd.DataFrame(list_data)

        # csv_name=os.path.join('cata1_web','test.csv')
        # df.to_csv(csv_name,index=False,header=False)
        return df
    # for i in range(n):
    #     df_tables=pd.read_html(str(tables[i]))
    #     for j in range(len(df_tables)):
    #         df=df_tables[j]
    #         csv_name=os.path.join('cata1_web','test.csv')
    #         df.to_csv(csv_name,index=False,header=False)
    #     print(df_tables)

def get_series_urls(series_path):
    df=pd.read_csv(series_path)
    return df

def write_to_csv(output_name,list_data):
    df=pd.DataFrame(list_data,columns=['title','url'])
    df.to_csv(output_name,index=False)

def main():

    # url='http://www.17vin.com/changan/cata1/240e73b04f43343da93a41aac6f47fdb/7301.html?p=aXNfbW9kZWw9MQ=='
    # get_car_series_info(url)
    cata1_paths=glob.glob('models_url_web/*.csv')
    os.makedirs('cata1_web',exist_ok=True)
    for cata1_path in cata1_paths:
        series_df=get_series_urls(cata1_path)
        for index, row in series_df.iterrows():
            brand=row['品牌']
            year=row['年款']
            displacement=row['排量']
            transmission=row['变速箱档位']
            gearbox=row['变速箱']
            url=row['url']
            if(url=='None'):
                continue
            output_name='cata1_web/{}_{}_{}_{}_{}.csv'.format(year,brand,displacement,transmission,gearbox)
            df=get_car_series_info(url)
            df.to_csv(output_name,index=False)
            # write_to_csv(output_name,list_data)
    # browser.close()

if __name__ == '__main__':
    main()