from flask import Flask, render_template, request
import requests
import json
import numpy as np
import pandas as pd
from math import dist
# config.py
import config

app = Flask(__name__)

def hp_api(lati,longi,i_start,count,key):
    api_key = config.HOTPEPPER_API_KEY
    query = {
        'key': api_key,
        'lat': lati,
        'lng': longi,
        'range': 5,
        'start': i_start, #検索結果の何番目から出力するか
        'count': count, #最大取得件数
        'format': 'json',
        'keyword': key
    }
    url_base = 'http://webservice.recruit.co.jp/hotpepper/gourmet/v1/'
    responce = requests.get(url_base, query)
    result = json.loads(responce.text)['results']['shop']
    return result

@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/choice', methods=['POST'])
def choice():
    personNum = request.form.get('personNum')
    if personNum=="人数を選んでね":
        return render_template('/index.html')
    return render_template('/choice.html',personNum=personNum)

@app.route('/result', methods=['GET','POST'])
def result():
    array = request.form.getlist("coor")
    array = np.array(array).reshape(-1,5)
    personNum = array.shape[0]
    array = array.T.tolist()
    array = [[int(s) for s in col] for col in array]
    coor = []
    for data in array:  # 平均を算出
        coor.append(np.mean(data))
    coor[0] = 100-coor[0]
    coor[1] = 100-coor[1]
    coor = [(x-50)*np.sqrt(personNum) for x in coor] #-50から50の値に中心をずらして1.5倍に誇張
    dists = []
    component = pd.read_csv("component.csv").values.tolist()
    for con in component:  # すべての料理候補との距離を算出
        con = con[1:]
        dists.append(dist(coor, con))
    # s = [max(dists)-x for x in dists]
    s = [np.exp(-x**2/10000) for x in dists]
    prob = [x/sum(s) for x in s]
    result = np.random.choice(len(prob),size=len(component),p=prob,replace=False).tolist()
    result = [component[x][0] for x in result]

    longi  = request.form.get('longi')
    lati = request.form.get('lati')
    for i,r in enumerate(result):
        api_ret = hp_api(lati,longi,1,1,r)
        if len(api_ret):
            result = result[i:i+3]
            break
    else:
        return render_template('/index.html')
    return render_template('/result.html',result0=result[0],
                                          result1=result[1],
                                          result2=result[2])

@app.route('/showmap',methods=['POST'])
def showmap():
    longi  = request.form.get('longi')
    lati = request.form.get('lati')
    # longi = 139.692
    # lati = 35.689
    i_start = 1
    key = request.form.get('result')
    restaurant_datas=[]
    while True:
        result = hp_api(lati,longi,i_start,100,key)
        if len(result) == 0:
            break
        for restaurant in result:
            restaurant_datas.append([restaurant['name'], restaurant['lat'],
            restaurant['lng'],
            restaurant['address'],
            restaurant['urls']['pc']])

        i_start += 100

    columns = ['name','lat','lng','address','url']
    df_restaurants = pd.DataFrame(restaurant_datas, columns=columns)
    return render_template('/showmap.html',result=df_restaurants.to_json(orient = 'records',force_ascii=False),longi=longi,lati=lati,n=request.form.get('result'))

if __name__ == "__main__":
    app.run()