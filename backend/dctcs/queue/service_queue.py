# -*- coding utf-8 -*-
import heapq
import threading

from dctcs.service.service_obj import ServiceObj


class ServiceQueue(object):
    '''ServiceQueue 维护待调度调温和调风请求的队列抽象
    '''

    def __init__(self):
        super().__init__()
        self.wait_count = 0
        self.index = 0
        self.wait_queue = []
        self.wait_lock = threading.Lock()

        self.serivce_count = 0
        self.service_queue = {}
        self.service_lock = threading.Lock()

    @staticmethod
    def create_service_obj(
            room_id: int,
            cur_temp: float,
            cur_fan_speed: str,
            target_temp: float,
            target_fan_speed: str) -> ServiceObj:
        '''创建服务对象

        Args:
            room_id          房间号
            cur_temp         当前温度
            cur_fan_speed    当前风速
            target_temp      目标温度
            target_fan_speed 目标风速

        Returns:
            ServiceObj 服务对象
        '''
        service_obj = ServiceObj()
        service_obj.ini_room(room_id)
        service_obj.ini_server_start_time()
        service_obj.ini_current_temp_and_speed(cur_temp, cur_fan_speed)
        service_obj.ini_target(target_temp, target_fan_speed)
        service_obj.ini_fee()
        return service_obj

    def add_wait(self, service_obj: ServiceObj) -> bool:
        '''将服务对象加入等待/待调度队列

        Args:
            service_obj 服务对象

        Returns:
            bool 添加结果，True 为成功，False 为失败
        '''
        with self.wait_lock:
            self.wait_count += 1
            heapq.heappush(
                self.wait_queue,
                (
                    service_obj.priority,  # 优先级
                    self.index,  # 加入顺序
                    service_obj  # 服务对象
                )
            )
            self.index += 1
        return True

    def get_wait(self) -> ServiceObj:
        '''从等待/待调度队列获取优先级最高的服务对象

        Args:
            None

        Returns:
            service_obj 服务对象
        '''
        with self.wait_lock:
            serv_objs = heapq.nsmallest(1, self.wait_queue)
            if not serv_objs:
                return None
            return serv_objs[0][-1]

    def pop_wait(self) -> ServiceObj:
        '''从等待/待调度队列弹出优先级最高的服务对象

        Args:
            None

        Returns:
            service_obj 服务对象
        '''
        with self.wait_lock:
            if self.wait_count == 0:
                return None
            self.wait_count -= 1
            serv_obj = heapq.heappop(self.wait_queue)[-1]
            serv_obj.wait_clock = 0  # 清空等待时长
        return serv_obj

    def add_service(self, service_obj: ServiceObj) -> bool:
        '''将服务对象加入服务队列

        Args:
            service_obj 服务对象

        Returns:
            bool 添加结果，True 为成功，False 为失败
        '''
        with self.service_lock:
            if service_obj.room_id not in self.service_queue:
                self.serivce_count += 1
            self.service_queue[service_obj.room_id] = service_obj
            # 初始化时钟
            service_obj.wait_clock = 0
            service_obj.service_clock = 0
            service_obj.start_serve()
        return True

    def pop_service_by_room_id(self, room_id: int) -> ServiceObj:
        '''通过房间号从服务队列调出服务对象

        Args:
            room_id 房间号

        Returns:
            service_obj 服务对象
        '''
        with self.service_lock:
            service_obj = self.service_queue.pop(room_id)
            # 初始化时钟
            service_obj.wait_clock = 0
            service_obj.service_clock = 0
            self.serivce_count -= 1
            service_obj.stop_serve()
        return service_obj

    def get_lowest_priority(self) -> ServiceObj:
        '''从服务队列调出优先级最低的调度请求，如果存在多个相同最低优先级，则取出服务时间最长者

        Args:
            None

        Returns:
            service_obj 服务对象
        '''
        lowest_objs = []
        with self.service_lock:
            lowest_priority = None
            # 先遍历判断最小的优先级
            for room_id in self.service_queue:
                if lowest_priority is None or \
                        self.service_queue[room_id].priority > lowest_priority:
                    lowest_priority = self.service_queue[room_id].priority
            for room_id in self.service_queue:
                if self.service_queue[room_id].priority == lowest_priority:
                    lowest_objs.append(self.service_queue[room_id])
        # 取服务时间最长
        longest_obj = None
        for obj in lowest_objs:
            if longest_obj is None or \
                    longest_obj.service_clock < obj.service_clock:
                longest_obj = obj
        return longest_obj
