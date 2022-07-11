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
                self.obj = Producer('producer')
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
        device = message.get('device')
        pkgname = message.get('pkgname')
        deviceId = d.getIdbyDevice(device)
        pid = d.getPid(deviceId=deviceId, pkgName=pkgname)
        if pid:
            self.cpu = CPU(pkgName=pkgname, deviceId=deviceId)
        # Send message to room group
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
                for i in client:
                    if self.scope['client'][1] == i.get('client'):
                        client.remove(i.get('client'))
                        return
            if not self.obj:
                self.obj = Producer('producer')
                self.obj.start()
            if not self.obj.is_alive():
                self.obj.start()
        except:
            pass


class Producer(threading.Thread):
    device = '3c2691fe'
    pkgname = "com.qiyi.video"
    deviceId = d.getIdbyDevice(device)
    pid = d.getPid(deviceId=deviceId, pkgName=pkgname)
    cpu = None
    if pid:
        cpu = CPU(pkgName=pkgname, deviceId=deviceId)
        fps_monitor = FPS(pkgName=pkgname, deviceId=deviceId)

    def __init__(self, name):
        super().__init__(name=name)
        self.value = 0

    def run(self):
        while True:
            result = f"cpu: {self.cpu.getSingCpuRate()}; fps: {self.fps_monitor.getFPS()}"
            for i in client:
                i.get('obj').send(text_data=json.dumps({
                    'message': result
                }))
