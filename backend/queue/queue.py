# -*- coding utf-8 -*-
from ..service.service_obj import ServiceObj


class ServiceQueue(object):
    '''ServiceQueue 维护待调度调温和调风请求的队列抽象
    '''

    def __init__(self):
        super().__init__()

    def create_service_obj(self,
                           room_id: int,
                           cur_temp: float,
                           cur_fan_speed: float) -> ServiceObj:
        '''创建服务对象

        Args:
            room_id       房间号
            cur_temp      当前温度
            cur_fan_speed 当前风速

        Returns:
            ServiceObj 服务对象
        '''
        pass

    def add(self, service_obj: ServiceObj) -> bool:
        '''将服务对象加入队列

        Args:
            service_obj 服务对象

        Returns:
            bool 添加结果，True 为成功，False 为失败
        '''
        pass

    def count_pp(self):
        '''服务对象数自增

        Args:
            None

        Returns:
            None
        '''
        pass
