# -*- coding: utf-8 -*-
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from WebSocket.app.controller.performance_testing import *
from WebSocket.app.controller.performance_testing import Devices

d = Devices()

current_device_observer = {
    "device": {
    },
}


class MobilePerformanceConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_current_device(self, room_name):
        current_device_observer.get("device")[room_name] = {
            "tasks": [],
            "device_observer": [],
            "device_observer_obj": []
        }
        return current_device_observer.get("device").get(self.room_name)

    def connect(self):
        # Join room group
        kwargs = self.scope['url_route']['kwargs']
        self.room_name = kwargs['device_name']
        self.observer = dict(clint=self.scope['headers'][10][1], obj=self)
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        current_device = current_device_observer.get("device").get(self.room_name)
        if current_device:
            current_device.get("device_observer").remove(self.scope['client'][1])
            current_device.get("device_observer_obj").remove(self.observer)
            if len(current_device.get("device_observer")) < 1:
                current_device.clear()
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        device = message.get("device")
        current_device = current_device_observer.get("device").get(device)
        # 判断设备是否以加入列表
        if not current_device:
            current_device = self.add_current_device(message.get("device"))
        # 客户端是否订阅
        if self.scope['client'][1] not in current_device.get("device_observer"):
            current_device.get("device_observer").append(self.scope['headers'][10][1])
            current_device.get("device_observer_obj").append(self.observer)
        # 判断是否发送断开请求
        if message.get("close"):
            if current_device:
                current_device["device_observer"] = [
                    item for item in current_device["device_observer"]
                    if item != self.scope['headers'][10][1]
                ]
                current_device["device_observer_obj"] = [
                    item for item in current_device["device_observer_obj"]
                    if item != self.observer
                ]
                # current_device.get("device_observer_obj").remove(self.observer)
                if len(current_device.get("device_observer")) == 0:
                    current_device.clear()
            return

        if not self.judgment_application(d.getIdbyDevice(message.get("device")),  message.get('pkgname')):
            return

        self.performance_dict = self.create_performanceObj_dict(d.getIdbyDevice(message.get("device")),  message.get('pkgname'))
        # 是否已经生成任务
        if current_device and len(current_device.get("tasks")) < 1:
            self.create_tasks(current_device, device)
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                # 通过type决定去调用指定函数
                'type': 'web_socket_send',
                'message': message
            }
        )

    def create_tasks(self, current_device, device):
        """
        创建任务
        :param current_device: dict中对应设备的value
        :param device: 设备名
        :return:
        """
        current_device["tasks"] = [
            MultithreadedPerformance("cpu", self.performance_dict.get("cpu").getSingCpuRate, device),
            MultithreadedPerformance("fps", self.performance_dict.get("fps").getFPS, device),
            MultithreadedPerformance("flow", self.performance_dict.get("flow").getAllFlow, device),
            MultithreadedPerformance("battery", self.performance_dict.get("battery").getBattery, device),
            MultithreadedPerformance("mem", self.performance_dict.get("mem").getProcessMem, device)
        ]

    def web_socket_send(self, event):
        message = event['message']
        current_device = current_device_observer.get("device").get(message.get("device"))
        try:
            for task in current_device.get("tasks"):
                if not task.is_alive():
                    task.start()
        except:
            pass

    def judgment_application(self, deviceId, pkgname):
        pid = d.getPid(deviceId=deviceId, pkgName=pkgname)
        if not pid:
            current_device = current_device_observer.get("device").get(d.getDevicesName(deviceId))
            for client in current_device.get("device_observer_obj"):
                client.get('obj').send(text_data=json.dumps({
                    'message': '当前设备性能数据获取失败，请尝试连接设备重新获取数据。',
                }))
            return False
        return True

    def create_performanceObj_dict(self, deviceId, pkgname):
        return {
            "cpu": CPU(pkgName=pkgname, deviceId=deviceId),
            "fps": FPS(pkgName=pkgname, deviceId=deviceId),
            "flow": Flow(pkgName=pkgname, deviceId=deviceId),
            "battery": Battery(deviceId=deviceId),
            "mem": MEM(pkgName=pkgname, deviceId=deviceId)
        }

import threading
class MultithreadedPerformance(threading.Thread):
    def __init__(self, name, task, device):
        threading.Thread.__init__(self)
        self.threadName = name
        self.device = device
        self.task = task

    def run(self):
        current_device = current_device_observer.get("device").get(self.device)
        try:
            while True:
                if not len(current_device.get("device_observer")):
                    break
                for client in current_device.get("device_observer_obj"):
                    client.get('obj').send(text_data=json.dumps({
                        'message': {
                            "taskName": self.threadName,
                            "ruslt": self.task()
                        },
                    }))
        except Exception as e:
            print(e)
