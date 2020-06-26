# -*- coding utf-8 -*-
import datetime

from dctcs.constdef.const import DEFAULT_TMP


class ServiceObj(object):
    '''ServiceObj 待调度请求的抽象（调温，调风）
    '''

    def __init__(self):
        super().__init__()
        self.room_id = None
        self.start_time = None

        self.temperature = DEFAULT_TMP
        self.target_temp = DEFAULT_TMP

        self.fan_speed = 'mid'
        self.target_fan_speed = 'mid'

        self.fee = 0

        self.priority = 0  # 调度优先级
        self.wait_clock = 0  # 队列等待时长
        self.service_clock = 0  # 队列服务时长

    def ini_room(self, room_id: int) -> bool:
        '''初始化服务房间号

        Args:
            room_id 房间号

        Returns:
            bool 增加结果，True 为成功，False 为失败
        '''
        self.room_id = room_id
        return True

    def ini_server_start_time(self) -> bool:
        '''初始化服务开始时间

        Args:
            None

        Returns:
            bool 增加结果，True 为成功，False 为失败
        '''
        self.start_time = datetime.datetime.now()
        return True

    def ini_current_temp_and_speed(
            self,
            cur_temp: float,
            cur_speed: str) -> bool:
        '''初始化服务房间的当前温度

        Args:
            current_room_temp 房间当前温度

        Returns:
            bool 增加结果，True 为成功，False 为失败
        '''
        self.temperature = cur_temp
        self.fan_speed = cur_speed

        return True

    def ini_fee(self) -> bool:
        '''初始化费用

        Args:
            None

        Returns:
            bool 增加结果，True 为成功，False 为失败
        '''
        self.fee = 0
        return True

    def ini_target(self, target_temp: float, fan_speed: str) -> bool:
        '''初始化费用

        Args:
            None

        Returns:
            bool 增加结果，True 为成功，False 为失败
        '''
        self.target_temp = target_temp
        self.target_fan_speed = fan_speed

        # 判断优先级
        if self.target_fan_speed is not None:
            if self.target_fan_speed == 'high':
                self.priority = 1
            elif self.target_fan_speed == 'mid':
                self.priority = 2
            else:
                self.priority = 3
        else:
            if self.fan_speed == 'high':
                self.priority = 1
            elif self.fan_speed == 'mid':
                self.priority = 2
            else:
                self.priority = 3

        return True
