# -*- coding: utf-8 -*-
import json
import time

import pymysql
from django.http import HttpResponse
from web.uilts.Jwt import UserToken
from web.locatsettings import Config


def login(request):
    if request.method == 'POST':
        account = json.loads(request.body)
        sql_settings = Config.get_Sqlsettins()
        db = pymysql.connect(host=sql_settings.host, user=sql_settings.user, password=sql_settings.password,
                             db=sql_settings.db, port=sql_settings.port, charset=sql_settings.charset,
                             cursorclass=sql_settings.Cursorclass(pymysql.cursors.DictCursor))
        cursor = db.cursor()
        cursor.execute(
            f'select id, username from user where '
            f'username="{account.get("username")}" and password="{account.get("password")}"')
        data = dict(cursor.fetchone())
        jwt = UserToken.get_token(data)
        refreshToken = UserToken.add_salt(data.get("username") + str(time.time()))
        cursor.execute(
            f'insert into RefreshToken(token_key,token_value,expiration_time_stamp,username) '
            f'values("{refreshToken}","{data}",{int(time.time()) + 3600}, "{data.get("username")}");')
        db.commit()
        db.close()
        return HttpResponse(json.dumps({'token': jwt, 'data': {'userinfo': data, 'refToken': refreshToken}}),
                            content_type="application/json;charset=UTF-8")
    return HttpResponse(json.dumps({'code': 404, 'msg': '请求方式问题'}), content_type="application/json;charset"
                                                                                 "=UTF-8")


def userInfo(request):
    if request.method == "GET":
        userinfo = UserToken.parse_token(request.headers.get('Token'))
        return HttpResponse(json.dumps({'data': userinfo}), content_type="application/json;charset"
                                                                     "=UTF-8")
def ref_token(request):
    if request.method == "GET":
        account = json.loads(request.body)
        sql_settings = Config.get_Sqlsettins()
        db = pymysql.connect(host=sql_settings.host, user=sql_settings.user, password=sql_settings.password,
                             db=sql_settings.db, port=sql_settings.port, charset=sql_settings.charset,
                             cursorclass=sql_settings.Cursorclass(pymysql.cursors.DictCursor))
        cursor = db.cursor()
        cursor.execute(
            f'select * from RefreshToken where token_key="{account.get("refToken")}"')
        data = dict(cursor.fetchone())
        if int(time.time()) < data.get("expiration_time_stamp") and data.get("status"):
            jwt = UserToken.get_token(dict(userinfo=data.get("token_value")))
            return HttpResponse(json.dumps({'code': '重置令牌成功', 'data': jwt}),
                                content_type="application/json;charset=UTF-8")
        # 需要写一条更自定数据的指令（将token的状态变更为0）
        cursor.execute()
        db.commit()
        db.close()
        return HttpResponse(json.dumps(dict(code=404, msg="重置令牌失败")))
