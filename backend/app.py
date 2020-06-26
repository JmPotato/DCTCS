# -*- coding utf-8 -*-
from dctcs.schedule.scheduler import Scheduler
from threading import Thread
from dctcs.user.user import User
from dctcs.db.models import db_handler

from flask import Flask, request, jsonify
app = Flask(__name__)

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
    return jsonify(
        status=1,
        message='Check in successfully',
        room_id=db_handler.check_in(),
    )


@app.route('/adjust_temperature', methods=['POST'])
def adjust_temperature():
    room_id = int(request.form['room_id'])
    cur_temp = float(request.form['cur_temp'])
    cur_speed = float(request.form['cur_speed'])
    target_temp = float(request.form['target_temp'])

    user = User(scheduler, room_id, cur_temp, cur_speed)
    return jsonify(
        status=1 if user.change_target_temp(target_temp) else -1,
        message='Adjust temperature request received'
    )


@app.route('/adjust_wind', methods=['POST'])
def adjust_wind():
    pass


@app.route('/status_heartbeat', methods=['GET'])
def status_heartbeat():
    # room_id = int(request.args.get('room_id'))
    pass


@app.route('/check_out', methods=['POST'])
def check_out():
    room_id = int(request.form['room_id'])
    bill, detailed_list = db_handler.check_out(room_id)
    return jsonify(
        status=1,
        message='Adjust temperature request received',
        bill=bill,
        detailed_list=detailed_list
    )


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
