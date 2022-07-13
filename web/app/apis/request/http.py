# -*- coding: utf-8 -*-
import json

from django.http import HttpResponse

from web.app.controller.HttpClient import Request


def request(request):
    if request.method == "POST":
        data = json.loads(request.body)
        method = data.get('method')
        if not method:
            return HttpResponse(json.dumps(dict(code=101, msg='请求方式不能为空')))
        url = data.get('url')
        if not url:
            return HttpResponse(json.dumps(dict(code=101, msg='请求路径不能为空')))
        body = data.get('body')
        headers = data.get('headers')
        if not headers:
            headers = {
                "Content-Type": "application/json; charset=utf-8",
            }
        if request.headers.get('Postman-Token'):
            r = Request(url, json=body, headers=headers)
        else:
            r = Request(url, data=body, headers=headers)
        response = r.request(method)
        if response.get('status'):
            return HttpResponse(json.dumps(dict(
                code=0,
                data=response,
                msg='操作成功')), headers={"Content-Type": "application/json; charset=utf-8"})
        return HttpResponse(json.dumps(dict(
            code=110,
            data=response,
            msg=response.get('msg'))), headers={"Content-Type": "application/json; charset=utf-8"})