# -*- coding utf-8 -*-
class ScheduleObj(object):
    '''ScheduleObj 待调度对象的抽象（房间）
    '''

    def __init__(self, room_id: int, current_room_temp: float):
        super().__init__()
        self.power_on = False
        self.room_id = room_id
        self.room_temp = current_room_temp

    def power_on(self) -> bool:
        self.power_on = True
        return self.power_on
