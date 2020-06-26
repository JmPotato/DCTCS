import sys
import datetime

from math import ceil
from time import sleep
from peewee import *

from ..constdef import const


class DataBase:
    def __init__(self):
        self.db = SqliteDatabase('DCTCS.db')
        self.db.connect()
        self.RoomTable.create_table()
        self.BillTable.create_table()
        self.DetailedItemTable.create_table()
        for i in range(10):
            self.RoomTable.create(room_id=i + 1,
                                  date_in=datetime.datetime.now(),
                                  is_empty=True)

    class BaseModel(Model):
        class Meta:
            database = SqliteDatabase('DCTCS.db')

    class RoomTable(BaseModel):
        room_id = AutoField()
        date_in = DateTimeField()
        is_empty = BooleanField()

    class BillTable(BaseModel):
        room_id = IntegerField()
        detailed_item_id = IntegerField()

    class DetailedItemTable(BaseModel):
        detailed_item_id = AutoField()
        room_id = IntegerField()
        start_time = DateTimeField(default=datetime.datetime.strptime(
            '2020-06-25 19:00:00', "%Y-%m-%d %H:%M:%S"))
        end_time = DateTimeField(default=datetime.datetime.now())
        start_temp = IntegerField()
        target_temp = IntegerField()
        mode = CharField()
        speed = CharField()
        fee_rate = IntegerField()

    def cul_fee(self, detailed_item_id):
        detailed_item = self.DetailedItemTable.filter(
            detailed_item_id=detailed_item_id)
        item = detailed_item[0]
        duration = ceil((item.end_time - item.start_time).seconds / 60)
        temp_change_rate = 0
        electrical_rate = 0
        if item.speed == "high":
            temp_change_rate = const.HIGH_SPEED_TMP_PER_MIN
            electrical_rate = const.HIGH_SPEED_MIN_PER_KWH
        if item.speed == "mid":
            temp_change_rate = const.MID_SPEED_TMP_PER_MIN
            electrical_rate = const.MID_SPEED_MIN_PER_KWH
        if item.speed == "low":
            temp_change_rate = const.LOW_SPEED_TMP_PER_MIN
            electrical_rate = const.LOW_SPEED_MIN_PER_KWH
        temp_time = 0
        temp_temp = item.start_temp
        electrical_usage = 0
        while temp_time < duration:
            if item.mode == "cold":  # 制冷模式
                if temp_temp >= item.target_temp + 1:
                    work_time = (temp_temp - item.target_temp) / \
                        temp_change_rate
                    if work_time > duration - temp_time:  # 工作时间大于剩余时间
                        electrical_usage += (duration -
                                             temp_time) / electrical_rate
                        break
                    else:
                        electrical_usage += work_time / electrical_rate
                        temp_time += work_time
                        temp_temp = item.target_temp
                    temp_temp += 1
                    temp_time += 2
                    continue
                else:
                    break
            else:  # 制热模式
                if temp_temp <= item.target_temp - 1:
                    work_time = (item.target_temp - temp_temp) / \
                        temp_change_rate
                    if work_time > duration - temp_time:  # 工作时间大于剩余时间
                        electrical_usage += (duration -
                                             temp_time) / electrical_rate
                        break
                    else:
                        electrical_usage += work_time / electrical_rate
                        temp_time += work_time
                        temp_temp = item.target_temp
                    temp_temp -= 1
                    temp_time += 2
                    continue
                else:
                    break
        fee = format(float(electrical_usage), '.2f')
        return fee

    def get_bill(self, room_id):
        have_record = self.RoomTable.filter(room_id=room_id)
        if len(have_record) == 0:
            return []
        date_in = have_record[0].date_in
        bills = self.BillTable.filter(room_id=room_id)
        total_fee = 0
        for bill in bills:
            total_fee += float(self.cul_fee(bill.detailed_item_id))
        ans = [room_id, date_in, total_fee]
        return ans

    def get_detailed_list(self, room_id):
        bills = self.BillTable.filter(room_id=room_id)
        if len(bills) == 0:
            return []
        ans = []
        for bill in bills:
            detailed_item = self.DetailedItemTable.filter(
                detailed_item_id=bill.detailed_item_id)[0]
            ans_item = [detailed_item.room_id,
                        detailed_item.start_time,
                        detailed_item.end_time,
                        detailed_item.start_temp,
                        detailed_item.target_temp,
                        detailed_item.mode,
                        detailed_item.speed,
                        detailed_item.fee_rate,
                        self.cul_fee(bill.detailed_item_id)]
            ans.append(ans_item)
        return ans

    def check_in(self):
        empty_rooms = self.RoomTable.filter(is_empty=True)
        if len(empty_rooms) != 0:
            room_id = empty_rooms[0].room_id
            query = self.RoomTable.update(is_empty=False, date_in=datetime.datetime.now())\
                .where(self.RoomTable.room_id == room_id)
            query.execute()
            return room_id
        else:
            new_room = self.RoomTable.create(
                is_empty=False, date_in=datetime.datetime.now())
            return new_room.room_id

    def use_air_conditioner(self, room_id, start_temp, target_temp, mode, speed, fee_rate):
        detailed_item_id = self.DetailedItemTable.create(room_id=room_id,
                                                         start_temp=start_temp,
                                                         target_temp=target_temp,
                                                         start_time=datetime.datetime.now(),
                                                         mode=mode,
                                                         speed=speed,
                                                         fee_rate=fee_rate)
        self.BillTable.create(
            room_id=room_id, detailed_item_id=detailed_item_id)
        return detailed_item_id

    def stop_air_conditioner(self, detailed_item_id):
        query = self.DetailedItemTable.update(end_time=datetime.datetime.now())\
            .where(self.DetailedItemTable.detailed_item_id == detailed_item_id)
        query.execute()

    def check_out(self, room_id):
        bill = self.get_bill(room_id)
        detailed_list = self.get_detailed_list(room_id)
        if room_id > 10:
            query = self.RoomTable.delete().where(self.RoomTable.room_id == room_id)
            query.execute()
        else:
            query = self.RoomTable.update(is_empty=True).where(
                self.RoomTable.room_id == room_id)
            query.execute()
        query = self.BillTable.delete().where(self.BillTable.room_id == room_id)
        query.execute()
        query = self.DetailedItemTable.delete().where(
            self.DetailedItemTable.room_id == room_id)
        query.execute()
        return bill, detailed_list


db = DataBase()  # 实例化
room = db.check_in()  # 入住，返回房间号
# 房间号，现温度，目标温度，模式（cold、hot），风速（high，mid，low），fee_rate（默认1）
# 返回详单记录号
detail_id = db.use_air_conditioner(room, 25, 22, "cold", "mid", 1)
sleep(70)  # 开了70s
db.stop_air_conditioner(detail_id)  # 关空调
sleep(70)  # 过了会又想开
detail_id = db.use_air_conditioner(room, 25, 22, "cold", "mid", 1)
sleep(10)  # 开了10s
db.stop_air_conditioner(detail_id)  # 关掉
b, d = db.check_out(room)  # 退房，返回账单、详单
print(b)  # 打印账单
print(d)  # 打印详单
room1 = db.check_in()  # 入住，返回房间号
room2 = db.check_in()  # 入住，返回房间号
room3 = db.check_in()  # 入住，返回房间号
room4 = db.check_in()  # 入住，返回房间号
room5 = db.check_in()  # 入住，返回房间号
room6 = db.check_in()  # 入住，返回房间号
room7 = db.check_in()  # 入住，返回房间号
room8 = db.check_in()  # 入住，返回房间号
room9 = db.check_in()  # 入住，返回房间号
room10 = db.check_in()  # 入住，返回房间号
room11 = db.check_in()  # 入住，返回房间号
room12 = db.check_in()  # 入住，返回房间号
b, d = db.check_out(room1)  # 退房，返回账单、详单
print(b)  # 打印账单
print(d)  # 打印详单
b, d = db.check_out(room2)  # 退房，返回账单、详单
print(b)  # 打印账单
print(d)  # 打印详单
b, d = db.check_out(room3)  # 退房，返回账单、详单
print(b)  # 打印账单
print(d)  # 打印详单
b, d = db.check_out(room4)  # 退房，返回账单、详单
print(b)  # 打印账单
print(d)  # 打印详单
b, d = db.check_out(room5)  # 退房，返回账单、详单
print(b)  # 打印账单
print(d)  # 打印详单
b, d = db.check_out(room6)  # 退房，返回账单、详单
print(b)  # 打印账单
print(d)  # 打印详单
b, d = db.check_out(room7)  # 退房，返回账单、详单
print(b)  # 打印账单
print(d)  # 打印详单
b, d = db.check_out(room8)  # 退房，返回账单、详单
print(b)  # 打印账单
print(d)  # 打印详单
b, d = db.check_out(room9)  # 退房，返回账单、详单
print(b)  # 打印账单
print(d)  # 打印详单
b, d = db.check_out(room10)  # 退房，返回账单、详单
print(b)  # 打印账单
print(d)  # 打印详单
b, d = db.check_out(room11)  # 退房，返回账单、详单
print(b)  # 打印账单
print(d)  # 打印详单
b, d = db.check_out(room12)  # 退房，返回账单、详单
print(b)  # 打印账单
print(d)  # 打印详单
