# -*- coding: utf-8 -*-
import json
import threading

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from WebSocket.app.controller.performance_testing import CPU, FPS
from WebSocket.app.controller.performance_testing import Devices

d = Devices()

client = []


class MobilePerformanceConsumer(WebsocketConsumer):
    obj = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cpu = None

    def connect(self):
        # Join room group

        kwargs = self.scope['url_route']['kwargs']
        self.room_name = kwargs['device_name']
        self.pkgname = kwargs.get('pkgname')
        if self.scope['client'][1] not in client:
            client.append(dict(
                clint=self.scope['client'][1],
                obj=self
            ))
            if not self.obj:
                self.obj = Producer('producer', self.room_name, self.pkgname)
        self.room_group_name = 'chat_%s' % self.room_name
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                # 通过type决定去调用指定函数
                'type': 'web_socket_send',
                'message': message
            }
        )

    def web_socket_send(self, event):
        message = event['message']
        try:
            if message.get("stop"):
                if len(client)<2:
                    self.obj.join()
                    client.remove(self.scope['client'][1])
                    self.obj = None
                    return
                client.remove(self.scope['client'][1])
                return
            if not self.obj or self.obj is None:
                device = message.get('device')
                pkgname = message.get('pkgname')
                self.obj = Producer('producer', device, pkgname)
                self.obj.start()
            if not self.obj.is_alive():
                self.obj.start()
        except:
            pass


class Producer(threading.Thread):

    def __init__(self, name, device, pkgname):
        super().__init__(name=name)
        self.device = device
        self.pkgname = pkgname
        self.create_performance_data(pkgname, d.getIdbyDevice(device))
        self.value = 0

    def create_performance_data(self, pkgname, deviceId):
        pid = d.getPid(deviceId=deviceId, pkgName=pkgname)
        if pid:
            self.cpu = CPU(pkgName=pkgname, deviceId=deviceId)
            self.fps_monitor = FPS(pkgName=pkgname, deviceId=deviceId)
            return
        return False

    def run(self):
        try:
            while True:
                result = f"cpu: {self.cpu.getSingCpuRate()}; fps: {self.fps_monitor.getFPS()}"
                for i in client:
                    i.get('obj').send(text_data=json.dumps({
                        'message': result
                    }))
        except:
            for i in client:
                i.get('obj').send(text_data=json.dumps({
                    'message': '当前设备性能数据获取失败，尝试连接设备重新获取数据。',
                }))
            self.create_performance_data(self.pkgname, d.getIdbyDevice(self.device))
