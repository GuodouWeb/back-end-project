# -*- coding: utf-8 -*-
# chat/routing.py
from django.urls import re_path

from . import consumers
from WebSocket.app.view.mobile_performance import MobilePerformanceConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', consumers.ChatConsumer.as_asgi()),
    re_path(r'ws/api/performance_testing/mobile/(?P<device_name>\w+)/$', MobilePerformanceConsumer.as_asgi()),
]
