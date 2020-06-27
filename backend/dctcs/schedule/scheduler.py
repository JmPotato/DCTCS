# -*- coding utf-8 -*-
import logging
from time import sleep

from dctcs.db.models import db_handler
from dctcs.queue.service_queue import ServiceQueue


class Scheduler(object):
    '''Scheduler 温控系统的抽象
    '''

    def __init__(self, max_service_obj=3):
        super().__init__()
        self.serv_queue = ServiceQueue()
        # 服务对象上限
        self.max_service_obj = max_service_obj

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def tick(self):
        '''时间流逝函数，给所有以秒为单位的时间计数函数加一
        '''
        with self.serv_queue.wait_lock:
            for item in self.serv_queue.wait_queue:
                item[-1].wait_clock += 1
        with self.serv_queue.service_lock:
            for room_id in self.serv_queue.service_queue:
                self.serv_queue.service_queue[room_id].service_clock += 1

    def dispatcher(self):
        '''调度逻辑
        '''
        while True:
            sleep(1)  # 等待一秒
            self.tick()
            # 服务队列未满
            serv_obj = self.serv_queue.get_wait()
            if serv_obj is None:
                # self.logger.info('No service request found.')
                continue
            self.logger.info(
                'Handle request from room #{}.'.format(serv_obj.room_id))
            if self.serv_queue.serivce_count < self.max_service_obj:
                self.logger.info('Queue is not full. Start to serv.')
                self.serv_queue.pop_wait()
                self.serv_queue.add_service(serv_obj)
            else:  # 服务队列已满
                lowest_obj = self.serv_queue.get_lowest_priority()
                # 替换优先级服务
                if serv_obj.priority < lowest_obj.priority:
                    self.logger.info(
                        'Queue is full. But lower priority found.')
                    self.serv_queue.pop_wait()
                    self.serv_queue.add_service(serv_obj)
                    # 非相同房间，需要换出
                    if serv_obj.room_id != lowest_obj.room_id:
                        self.serv_queue.pop_service_by_room_id(
                            lowest_obj.room_id)
                        self.serv_queue.add_wait(lowest_obj)
                elif serv_obj.priority == lowest_obj.priority:
                    self.logger.info('Queue is full. But same priority found.')
                    if serv_obj.wait_clock >= 5:  # 等待时间已满，强行替换
                        self.logger.info('Already wait for 2 mins.')
                        self.serv_queue.pop_wait()
                        self.serv_queue.add_service(serv_obj)
                        # 非相同房间，需要换出
                        if serv_obj.room_id != lowest_obj.room_id:
                            self.serv_queue.pop_service_by_room_id(
                                lowest_obj.room_id)
                            self.serv_queue.add_wait(lowest_obj)
                else:
                    self.logger.info(
                        'Queue is full. But no lower priority found.')

    def query(self, room_id: int):
        '''查询函数，用于响应心跳请求，返回当前房间的状态：温度，风速，耗电和费用
        '''
        return db_handler.get_room_stat(room_id)

    def check_out(self, room_id: int):
        with self.serv_queue.service_lock:
            if room_id in self.serv_queue.service_queue:
                db_handler.stop_air_conditioner(
                    self.serv_queue.service_queue[room_id].detailed_item_id
                )
                del self.serv_queue.service_queue[room_id]
        with self.serv_queue.wait_lock:
            for index, wait_obi in enumerate(self.serv_queue.wait_queue):
                if wait_obi[-1].room_id == room_id:
                    del self.serv_queue.wait_queue[index]
        return db_handler.check_out(room_id)
