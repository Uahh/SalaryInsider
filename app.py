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
app.jinja_env.variable_start_string = '{['
app.jinja_env.variable_end_string = ']}'
print('Waiting......')



# 主要逻辑视图函数
@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
    return render_template('index.html')

@app.route('/create_room', methods=["POST"])
def create_room():
    data = json.loads(request.get_data(as_text=True))
    id = str(uuid.uuid1())
    rs.set(id + '_roomPeople', data['roomPeople'], ex=600)  # 10分钟消除
    rs.set(id + '_nowPeople', "1", ex=600)  # 10分钟消除
    rs.set(id + '_salaryType', data['salaryType'], ex=600)
    rs.set(id + '_salary', data['salary'], ex=600)
    return id

@app.route('/join_room', methods=["POST"])
def join_room():
    data = json.loads(request.get_data(as_text=True))
    id = data['roomNumber']
    room_number = rs.get(data['roomNumber'] + '_roomNumber')
    if room_number:
        salary = data['salary'] + int(salary)
        rs.set(id + '_salary', str(salary), ex=600)
        now_people = int(rs.get(id + 'nowPeople'))
        if now_people + 1 == int(rs.get(id + '_roomPeople')):
            return int(rs.get(id + '_salary')) / (now_people + 1)
    return "房间号不存在或已失效"

@app.route('/error')
def error():
    return '404 not found'


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=173)