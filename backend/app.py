# -*- coding utf-8 -*-
from user.user import User

from flask import Flask, request
app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'


'''
用户侧相关接口

* /check_in           入住
* /adjust_temperature 调温
* /adjust_wind        调风
* /status_heartbeat   状态心跳
* /get_room_bill      获取账单（退房时调取）
'''


@app.route('/check_in', methods=['POST'])
def check_in():
    pass


@app.route('/adjust_temperature', methods=['POST'])
def adjust_temperature():
    pass


@app.route('/adjust_wind', methods=['POST'])
def adjust_wind():
    pass


@app.route('/status_heartbeat', methods=['GET'])
def status_heartbeat():
    pass


@app.route('/get_room_bill', methods=['GET'])
def get_room_bill():
    pass


'''
空调管理员侧相关接口

* /get_room_list   获取当前已入住客房列表
* /get_room_detail 获取客房详单
'''


@app.route('/get_room_list', methods=['GET'])
def get_room_list():
    pass


@app.route('/get_room_detail', methods=['GET'])
def get_room_detail():
    pass
