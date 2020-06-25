# -*- coding utf-8 -*-
class User(object):
    '''User 客房用户抽象
    '''

    def __init__(self, room_id: int, current_room_temp: float):
        super().__init__()
        pass

    def request_on(self) -> bool:
        '''客户请求开机

        Args:
            None

        Returns:
            bool 开机结果，True 为成功，False 为失败
        '''
        pass

    def change_target_temp(self, target_temp: float) -> bool:
        '''客户请求修改房间到目标温度

        Args:
            target_temp 目标温度

        Returns:
            bool 修改结果，True 为成功，False 为失败
        '''
        pass

    def change_fan_speed(self, fan_speed: float) -> bool:
        '''客户请求修改房间送风速度

        Args:
            fan_speed 目标风速

        Returns:
            bool 修改结果，True 为成功，False 为失败
        '''
        pass
