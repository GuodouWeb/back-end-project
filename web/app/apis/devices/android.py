# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse
from WebSocket.app.controller.performance_testing.mobile_terminal.common import Devices


def getDevices(request):
    if request.method == 'GET':
        d = Devices()
        return HttpResponse(json.dumps(dict(
            code=200,
            data=d.getDevices(),
            msg="ok"
        )), content_type="application/json;charset=UTF-8")


def getPkgname(request):
    if request.method == 'GET':
        device = request.GET.get('deviceID')
        if not device:
            return HttpResponse(json.dumps(dict(
                code=404,
                msg="没找到该设备，无法查看设备所安装的应用"
            )), content_type="application/json;charset=UTF-8")
        d = Devices()
        return HttpResponse(json.dumps(dict(
            code=200,
            data=d.getPkgname(device),
            msg="ok"
        )), content_type="application/json;charset=UTF-8")
