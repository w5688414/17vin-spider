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
import re

browser = webdriver.Chrome()
wait = WebDriverWait(browser,20)

def get_url_encode(key,value):
    values={}
    values[key]=value
    KEYWORD=urllib.parse.urlencode(values)
    return KEYWORD

def get_car_series_info(browser,tilte,url):
    # url='http://www.17vin.com/models.html?p=YnJhbmQ96ZW_5a6J5qyn5bCaJmNoYW5namlhPemVv-Wuieasp-WwmiZzZXJpZXM9Q1g3MA=='
    print(url)
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, "lxml")
    tables=soup.find_all('table')
    # print(tables)
    n=len(tables)
    columns=['品牌','年款','车型','发动机','排量','进气方式','燃油类型','变速箱','变速箱档位','配件目录','model_id']
    for i in range(1,n): # table 0 没有数据
        # print(tables[i])
        list_data=[]
        for tr in tables[i].findAll('tr'):
            t=[]
            tds=tr.findAll('td')
            # print(tds)
            for td in tds:
                t.append(td.getText())
            if(len(tds)>0 and tds[-1].getText()!='无配件目录'):
                model_id=tds[-1].find('a')['href']
                model_id= re.findall("\d+",model_id)
                t.append(model_id[0])
            else:
                t.append('-1')
            list_data.append(t)
        print(list_data)
        list_data=list_data[1:]
        df=pd.DataFrame(list_data,columns=columns)

        csv_name=os.path.join('models_web',tilte+'.csv')
        df.to_csv(csv_name,index=False)

        # df_tables=pd.read_html(str(tables[i]))
        # for j in range(len(df_tables)):
        #     df=df_tables[j]
        #     csv_name=os.path.join('models_web',tilte+'_'+str(j)+'.csv')
        #     df.to_csv(csv_name,index=False,header=False)
        # print(df_tables)

def get_series_urls(series_path):
    df=pd.read_csv(series_path)
    return df

def write_to_csv(output_name,list_data):
    df=pd.DataFrame(list_data,columns=['title','url'])
    df.to_csv(output_name,index=False)

def main():
    series_paths=glob.glob('series_web/*.csv')
    os.makedirs('models_web',exist_ok=True)
    for series_path in series_paths:
        series_df=get_series_urls(series_path)
        for index, row in series_df.iterrows():
            tilte=row['title']
            url=row['url']
            output_name='models_url.csv'
            get_car_series_info(browser,tilte,url)
    # write_to_csv(output_name,list_data)
    browser.close()

if __name__ == '__main__':
    main()