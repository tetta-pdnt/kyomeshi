from flask import Flask, render_template, request
import numpy as np
import pandas as pd
from math import dist
# config.py
import config

app = Flask(__name__)


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
    s = [np.exp((-int(x))^2) for x in dists]
    prob = [x/sum(s) for x in s]
    result = np.random.choice(len(prob),size=3,p=prob,replace=False).tolist()
    result = [component[x][0] for x in result]
    # result = []
    # dists.sort(key=lambda x:x[1])
    # result = [component[x[0]][0] for x in dists[:3]]

    # api_key = config.HOTPEPPER_API_KEY

    # i_start = 1
    # restaurant_datas=[]

    # while True:
    #     query = {
    #         'key': api_key,
    #         'large_area': 'Z011', # 東京
    #         'order': 1, #名前の順
    #         'start': i_start, #検索結果の何番目から出力するか
    #         'count': 100, #最大取得件数
    #         'format': 'json',
    #         'keyword': result[0]
    #     }
    #     url_base = 'http://webservice.recruit.co.jp/hotpepper/gourmet/v1/'
    #     responce = requests.get(url_base, query)
    #     result = json.loads(responce.text)['results']['shop']
    #     if len(result) == 0:
    #         break
    #     for restaurant in result:
    #         restaurant_datas.append([restaurant['name'], restaurant['address'], restaurant['budget']['code'], restaurant['genre']['code']])
    #     i_start += 100
    #     print(i_start)

    # columns = ['name', 'address', 'budget', 'genre']
    # df_restaurants = pd.DataFrame(restaurant_datas, columns=columns)
    # df_restaurants.to_csv('restaurants_tokyo.csv')
    return render_template('/result.html',result0=result[0],
                                          result1=result[1],
                                          result2=result[2])

if __name__ == "__main__":
    app.run()