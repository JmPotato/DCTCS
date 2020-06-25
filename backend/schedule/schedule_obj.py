# -*- coding utf-8 -*-
class ScheduleObj(object):
    '''ScheduleObj 待调度对象的抽象（房间）
    '''

    def __init__(self, current_room_temp: float):
        super().__init__()
        self.room_id = None
        self.power_on = False
        self.room_temp = current_room_temp

        self.priority = 0

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

    def make_service_object(self) -> bool:
        '''要求服务队列创建服务对象

        Args:
            room_id 房间号

        Returns:
            bool 创建结果，True 为成功，False 为失败
        '''
        pass

    def change_target_temp(self, target_temp: float) -> bool:
        '''要求服务队列修改服务对象的目标温度

        Args:
            target_temp 目标温度

        Returns:
            bool 修改结果，True 为成功，False 为失败
        '''
        pass

    def change_fan_speed(self, fan_speed: float) -> bool:
        '''要求服务队列修改服务对象的风速

        Args:
            fan_speed 目标风速

        Returns:
            bool 修改结果，True 为成功，False 为失败
        '''
        pass
