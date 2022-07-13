#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
@author: Frank
@contact: frank.chang@shoufuyou.com
@file: 18.py
@time: 2018/7/10 下午8:59

一个简单的demon   生产者与消费者

"""
import asyncio
import queue

import threading
from WebSocket.app.controller import Devices
from WebSocket.app.controller import CPU

d = Devices()

# 哨兵
_sentinel = object()
b1 = 0
device = '3c2691fe'
pkgname = "com.qiyi.video"
deviceId = d.getIdbyDevice(device)
pid = d.getPid(deviceId=deviceId, pkgName=pkgname)
if pid:
    cpu = CPU(pkgName=pkgname, deviceId=deviceId)

dit1 = dict(v=0, value=0)


async def get_cpu():
    a = cpu.getSingCpuRate()
    return a

class Producer(threading.Thread):
    """
    只负责产生数据
    """

    def __init__(self, name, queue, loop):
        super().__init__(name=name)
        self.queue = queue
        self.value = 0
        self.loop = loop
        self.list = []

    def run(self):
        global dit1
        while True:

            task = self.loop.create_task(get_cpu())
            self.loop.run_until_complete(task)
            a = cpu.getSingCpuRate()
            for i in self.list:
                i.s(a)



class Consumer(threading.Thread):
    """
    数据处理,对数据进行消费.
    """

    def __init__(self, name, queue):
        super().__init__(name=name)
        self.queue = queue
        self.value = None
        self.diact = dict(v=0, value=0)

    def run(self):
        while True:
            if self.diact['v'] != dit1['v']:
                self.diact = dit1
                # 用来退出线程
                # if value is _sentinel:
                #     # 添加哨兵,让其他线程有机会退出来
                #     self.queue.put(value)
                #     break
                print("{} 正在消费. {} 被消耗！".format(self.getName(), self.diact['v']))
    def s(self, a):
        print("{} 正在消费. {} 被消耗！".format(self.getName(), a))


if __name__ == '__main__':
    queue = queue.Queue()
    loop = asyncio.get_event_loop()
    producer = Producer('producer', queue, loop)

    consumer_threads = []
    for i in range(5):
        consumer = Consumer('consumer_' + str(i), queue)
        producer.list.append(consumer)

    producer.start()

    # producer.join()
    # for consumer in consumer_threads:
    #     consumer.join()
    #
    # producer.join()

    print('All threads  done')
