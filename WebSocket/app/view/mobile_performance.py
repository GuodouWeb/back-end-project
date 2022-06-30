# -*- coding: utf-8 -*-
import asyncio
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer, WebsocketConsumer
from ..controller.performance_testing.mobile_terminal.apm import CPU, MEM, Flow, FPS, Battery
from ..controller.performance_testing.mobile_terminal.common import Devices

d = Devices()


class MobilePerformanceConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cpu = None
        self.fa = True

    def connect(self):
        # Join room group
        kwargs = self.scope['url_route']['kwargs']
        self.room_name = kwargs['device_name']
        self.pkgname = kwargs.get('pkgname')

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
        if message.get('stop'):
            self.fa = False
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
                'type': 'WebSocketSend',
                'message': message
            }
        )

    def WebSocketSend(self, event):
        cpuRate = self.cpu.getSingCpuRate()
        result = {'status': 1, 'cpuRate': cpuRate}
        self.send(text_data=json.dumps({
            'message': result
        }))
