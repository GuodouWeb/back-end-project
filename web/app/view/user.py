# -*- coding: utf-8 -*-
import json
import time
import pymysql
from web.app.dao.mysql_linkpool import MysqlUtility
from django.http import HttpResponse
from web.uilts.Jwt import UserToken
from web.locatsettings import Config


def login(request):
    if request.method == 'POST':
        account = json.loads(request.body)
        if account.get("username") == "" or account.get("password") == "":
            return HttpResponse(json.dumps({'code': 404, 'msg': '账号密码不能为空'}), content_type="application/json;charset"
                                                                                           "=UTF-8")
        msql = MysqlUtility()
        conn, cur = msql.get_conn()
        data = msql.select(
            f'select id, username from user where '
            f'username="{account.get("username")}" and password="{account.get("password")}"', cur)
        jwt = UserToken.get_token(data)
        refreshToken = UserToken.add_salt(data.get("username") + str(time.time()))
        msql.close(conn, cur)
        return HttpResponse(
            json.dumps({'code': 200, 'token': jwt, 'data': {'userinfo': data, 'refToken': refreshToken}}),
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
                             cursorclass=pymysql.cursors.DictCursor)
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
