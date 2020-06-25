# -*- coding utf-8 -*-
class ServiceObj(object):
    '''ServiceObj 待调度请求的抽象（调温，调风）
    '''

    def __init__(self):
        super().__init__()
        pass

    def ini_server_start_time(self) -> bool:
        '''初始化服务开始时间

        Args:
            None

        Returns:
            bool 增加结果，True 为成功，False 为失败
        '''
        pass

    def ini_current_room_temp(self, current_room_temp: float) -> bool:
        '''初始化服务房间的当前温度

        Args:
            current_room_temp 房间当前温度

        Returns:
            bool 增加结果，True 为成功，False 为失败
        '''
        pass

    def ini_fee(self) -> bool:
        '''初始化费用

        Args:
            None

        Returns:
            bool 增加结果，True 为成功，False 为失败
        '''
        pass

    def ini_room(self, room_id: int) -> bool:
        '''初始化服务房间号

        Args:
            room_id 房间号

        Returns:
            bool 增加结果，True 为成功，False 为失败
        '''
        pass
