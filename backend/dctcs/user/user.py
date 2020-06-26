# -*- coding utf-8 -*-
from dctcs.schedule.scheduler import Scheduler
from dctcs.schedule.schedule_obj import ScheduleObj


class User(object):
    '''User 客房用户抽象
    '''

    def __init__(
            self,
            scheduler: Scheduler,
            room_id: int,
            cur_temp: float,
            cur_speed: str):
        super().__init__()
        self.room_id = room_id
        self.schedule_obj = ScheduleObj(scheduler, cur_temp, cur_speed)
        self.schedule_obj.add_room(room_id)

    def request_on(self) -> bool:
        '''客户请求开机

        Args:
            None

        Returns:
            bool 开机结果，True 为成功，False 为失败
        '''
        return self.schedule_obj.power_on()

    def change_target_temp(self, target_temp: float) -> bool:
        '''客户请求修改房间到目标温度

        Args:
            target_temp 目标温度

        Returns:
            bool 修改结果，True 为成功，False 为失败
        '''
        return self.schedule_obj.change_target_temp(target_temp)

    def change_fan_speed(self, fan_speed: str) -> bool:
        '''客户请求修改房间送风速度

        Args:
            fan_speed 目标风速

        Returns:
            bool 修改结果，True 为成功，False 为失败
        '''
        return self.schedule_obj.change_fan_speed(fan_speed)
