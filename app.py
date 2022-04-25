# -*- coding: utf-8 -*-
import time
import uuid
import json
from flask import Flask
from flask import request
from flask import render_template
import redis   
from model import server_config

rs = redis.Redis(host=server_config.server_ip, port=server_config.redis_port, password=server_config.redis_pw, decode_responses=True)

app = Flask(__name__, template_folder='templates', static_folder='static')
print('Waiting......')



# 主要逻辑视图函数
@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
    return render_template('index.html')

@app.route('/create_room', methods=["POST"])
def create_room():
    data = json.loads(request.get_data(as_text=True))
    id =  str(uuid.uuid1())
    rs.set(id + '_roomNumber', data['roomNumber'], ex=600)  # 10分钟消除
    rs.set(id + '_salaryType', data['salaryType'], ex=600)
    rs.set(id + '_salary', data['salary'], ex=600)
    return "0"

# @app.route('/join_room', methods=["POST"])
# def join_room(room_num, salary):
#     total = rs.get(room_num)
#     for i in range(1, total):
#         if rs.get(str(idx) + '_' + str(i)):
#             continue
#         rs.setnx(str(idx) + '_' + str(i), salary, ex=300)
#     if rs.get(room_num + '_' + str(total - 1)):
#         return True
#     return False

@app.route('/error')
def error():
    return '404 not found'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=173)