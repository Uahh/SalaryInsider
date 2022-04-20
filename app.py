# -*- coding: utf-8 -*-
import time
import json
from flask import Flask
from flask import request
from flask import render_template
import redis   # 导入redis 模块

rs = redis.Redis(host='localhost', port=6379, decode_responses=True)  
idx = 0

app = Flask(__name__, template_folder='templates', static_folder='static')
print('Waiting......')


# 主要逻辑视图函数
@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
    return render_template('index.html')

@app.route('/create_room', methods=["POST"])
def create_room(salary, people_num):
    rs.setnx(str(idx), people_num, ex=300)  # 1小时消除
    rs.setnx(str(idx) + '_0', salary, ex=300)


@app.route('/join_room', methods=["POST"])
def create_room(room_num, salary):
    total = rs.get(room_num)
    for i in range(1, total):
        if rs.get(str(idx) + '_' + str(i)):
            continue
        rs.setnx(str(idx) + '_' + str(i), salary, ex=300)
    if rs.get(room_num + '_' + str(total - 1)):
        return True
    return False

@app.route('/error')
def error():
    return '404 not found'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=173)