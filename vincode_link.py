import requests
import json
import glob
import pandas as pd
import os

def get_models_ids(csv_path):
    df=pd.read_csv(csv_path)
    return df

def test():
    url='http://www.17vin.com/ajax/vindecodelink.aspx?modelid=1105'
    r=requests.get(url)

    print(r.status_code)
    print(r.encoding)
    print(r.apparent_encoding)

    # print(r.text)
    json_text=json.loads(r.text)
    print(json_text)

def get_cata1_url(model_id):
    if(model_id==-1):
        return 'None'
    url='http://www.17vin.com/ajax/vindecodelink.aspx?modelid={}'.format(model_id)
    r=requests.get(url)
    json_text=json.loads(r.text)
    # 'http://www.17vin.com'
    return 'http://www.17vin.com'+json_text['url']

if __name__ == "__main__":
    # test()

    os.makedirs('models_url_web',exist_ok=True)
    csvs=glob.glob('models_web/*.csv')
    for csv_path in csvs:
        # data=get_models_ids(csv_path)
    
        # csv_path='models_web/12C.csv'
        data=get_models_ids(csv_path)
        data['url']=data['model_id'].apply(lambda x:get_cata1_url(x))
        print(data)
        output_path=os.path.join('models_url_web',csv_path.split('/')[-1])
        data.to_csv(output_path)


    

