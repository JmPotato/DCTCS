# -*- coding utf-8 -*-
from threading import Thread

from dctcs.user.user import User
from dctcs.db.models import db_handler
from dctcs.constdef.const import DEFAULT_TMP
from dctcs.schedule.scheduler import Scheduler

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 初始化温控系统
scheduler = Scheduler()
# 新建线程运行调度器
t = Thread(target=scheduler.dispatcher)
t.start()

'''
用户侧相关接口

* /check_in           入住
* /adjust_temperature 调温
* /adjust_wind        调风
* /status_heartbeat   状态心跳
* /check_out          退房
'''


@app.route('/check_in', methods=['POST'])
def check_in():
    room_id = db_handler.check_in()
    # 初始化第一个调度请求
    user = User(scheduler, room_id, DEFAULT_TMP, 'mid')
    user.change_target_temp(DEFAULT_TMP)

    return jsonify(
        status=1,
        message='Check in successfully',
        room_id=room_id,
    )


@app.route('/adjust_temperature', methods=['POST'])
def adjust_temperature():
    room_id = int(request.form['room_id'])
    cur_temp = float(request.form['cur_temp'])
    cur_speed = str(request.form['cur_speed'])
    target_temp = float(request.form['target_temp'])

    user = User(scheduler, room_id, cur_temp, cur_speed)
    return jsonify(
        status=1 if user.change_target_temp(target_temp) else -1,
        message='Adjust temperature request received'
    )


@app.route('/adjust_wind', methods=['POST'])
def adjust_wind():
    room_id = int(request.form['room_id'])
    cur_temp = float(request.form['cur_temp'])
    cur_speed = str(request.form['cur_speed'])
    target_speed = str(request.form['target_speed'])

    user = User(scheduler, room_id, cur_temp, cur_speed)
    return jsonify(
        status=1 if user.change_fan_speed(target_speed) else -1,
        message='Adjust fan speed request received'
    )


@app.route('/status_heartbeat', methods=['GET'])
def status_heartbeat():
    room_id = int(request.args.get('room_id', -1))
    status = scheduler.query(room_id)
    return jsonify(
        temperature=status[0],
        speed=status[1],
        electrical_usage=status[2],
        fee=status[3],
    )


@app.route('/check_out', methods=['POST'])
def check_out():
    room_id = int(request.form['room_id'])
    bill, detailed_list = scheduler.check_out(room_id)
    return jsonify(
        status=1,
        message='Check out successfully',
        bill=bill,
        detailed_list=detailed_list
    )


'''
空调管理员侧相关接口

* /get_room_detial_list   获取当前已入住客房列表及详单信息
'''


@app.route('/get_room_detial_list', methods=['GET'])
def get_room_detial_list():
    return jsonify(
        rooms=db_handler.get_checked_in_room_info()
    )
