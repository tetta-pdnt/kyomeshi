from flask import Flask, render_template, request, redirect, url_for, g
import json
import numpy as np
import pandas as pd
from math import dist
import json
# import requests
# config.py
# import config

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
# db = SQLAlchemy(app)

# class PersonNum(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     num = db.Column(db.Integer)

# class Coor(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     junky = db.Column(db.Integer)
#     spicy = db.Column(db.Integer)
#     noisy = db.Column(db.Integer)
#     appetite = db.Column(db.Integer)

@app.route('/')
def index():
    return render_template('/index.html')



# array = [[] for _ in range(4)]
@app.route('/choice', methods=['POST'])
def choice():
    # comp = ["calorie","spisy","amount","strong","share"]
    # if str(request.referrer)[-7:]!="/choice":
    #     g.personNum = request.form.get('personNum')
    personNum = request.form.get('personNum')
    #     g.count = 0
    # else:
    #     for (c,col) in zip(comp,g.array):
    #         col.append(request.form.get(c))
    #     print(g.array)

    # if g.count == g.personNum:
    #     return render_template('result.html',array = g.array)
    # else:
    #     g.count += 1
    #     return render_template('choice.html',count=g.count)
    return render_template('/choice.html',personNum=personNum)

# @app.route('/json',methods=['GET','POST'])
# def json():
#     array = request.json
#     print(type(array))
#     print(array)

@app.route('/result', methods=['GET','POST'])
def result():
    # array = request.get_data()
    # array = array.decode('utf-8')
    # # array = eval(str(array))
    # # array = str(array)
    # array = array.replace('"',"")
    array = request.json
    print(type(array))
    print(array)
    # coor = []
    # for data in array:  # 平均を算出
    #     coor.append(np.mean(data))
    # dists = []
    # component = pd.read_csv("component.csv").values.tolist()
    # for con in component:  # すべての料理候補との距離を算出
    #     con = [(n-1)*25 for n in con[1:]]  # CSVの1-5の値を0,25,50,75,100に変換
    #     dists.append(dist(coor, con))
    # result = []
    # for i in range(dists.count(min(dists))):  # 最短距離の料理をすべて出力
    #     m = dists.index(min(dists))
    #     result.append(component[m][0])
    #     dists.pop(m)
    return render_template('/result.html',array = str(array))

if __name__ == "__main__":
    app.run(debug=True)