# -*- coding utf-8 -*-
from dctcs.schedule.scheduler import Scheduler


class ScheduleObj(object):
    '''ScheduleObj 待调度对象的抽象（房间）
    '''

    def __init__(self, scheduler: Scheduler, cur_temp: float, cur_speed: str):
        super().__init__()
        self.scheduler = scheduler

        self.power_on = False

        self.room_id = None
        self.room_temp = cur_temp
        self.room_speed = cur_speed

    def power_on(self) -> bool:
        self.power_on = True
        return self.power_on

    def add_room(self, room_id: int) -> bool:
        '''增加服务房间

        Args:
            None

        Returns:
            bool 增加结果，True 为成功，False 为失败
        '''
        self.room_id = room_id
        return True

    def is_room_list(self) -> bool:
        '''判断该房间是否在服务队列中

        Args:
            None

        Returns:
            bool 判断结果，True 为是，False 为否
        '''
        pass

    def make_service_object(
            self,
            target_temp: float,
            target_speed: str) -> bool:
        '''要求服务队列创建服务对象

        Args:
            room_id 房间号

        Returns:
            bool 创建结果，True 为成功，False 为失败
        '''
        self.service_object = self.scheduler.serv_queue.create_service_obj(
            self.room_id,
            self.room_temp,
            self.room_speed,
            target_temp,
            target_speed
        )

        return True

    def change_target_temp(self, target_temp: float) -> bool:
        '''要求服务队列修改服务对象的目标温度

        Args:
            target_temp 目标温度

        Returns:
            bool 修改结果，True 为成功，False 为失败
        '''
        self.make_service_object(target_temp, None)
        return self.scheduler.serv_queue.add_wait(self.service_object)

    def change_fan_speed(self, fan_speed: str) -> bool:
        '''要求服务队列修改服务对象的风速

        Args:
            fan_speed 目标风速

        Returns:
            bool 修改结果，True 为成功，False 为失败
        '''
        self.make_service_object(None, fan_speed)
        return self.scheduler.serv_queue.add_wait(self.service_object)
