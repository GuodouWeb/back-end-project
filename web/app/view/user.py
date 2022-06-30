# -*- coding: utf-8 -*-
import json
import time
import pymysql
from django.forms import model_to_dict
from django.http import HttpResponse
from web.app.models import models
from web.uilts.Jwt import UserToken
from web.locatsettings import Config


def login(request):
    if request.method == 'POST':
        if request.headers.get('Content-Type') == 'application/x-www-form-urlencoded':
            data = request.POST
        if request.headers.get('Content-Type') == 'application/json':
            data = json.loads(request.body)
        if data is None:
            return HttpResponse(json.dumps({'code': 500, 'msg': '无法获取数据'}),
                                content_type="application/json;charset"
                                             "=UTF-8")
        username = data.get('username')
        password = data.get('password')
        if username is None or password is None:
            return HttpResponse(json.dumps({'code': 404, 'msg': '账号密码不能为空'}),
                                content_type="application/json;charset"
                                             "=UTF-8")
        # user_object=models.UserInfo.objects.filter(username=username,password=password).exists()
        # 手机=phone and pwd=pwd  || email=email and pwd=pwd
        user_object = models.User.objects.filter(username=username, password=password).first()
        if not user_object:
            return HttpResponse(json.dumps({'code': 404, 'msg': '账号密码错误'}), content_type="application/json;charset"
                                                                                         "=UTF-8")
        user_info = model_to_dict(user_object)
        jwt = UserToken.get_token(user_info)
        refreshToken = UserToken.add_salt(user_object.username + str(time.time()))
        return HttpResponse(
            json.dumps({'code': 200, 'token': jwt, 'data': {'userinfo': user_info, 'refToken': refreshToken}}),
            content_type="application/json;charset=UTF-8")

    return HttpResponse(json.dumps({'code': 404, 'msg': '请求方式问题'}), content_type="application/json;charset"
                                                                                 "=UTF-8")


def register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        if data is not None:
            name = data.get('name')
            username = data.get('username')
            password = data.get('password')
            if username is None or password is None:
                return HttpResponse(json.dumps({'code': 404, 'msg': '注册的账号密码不能为空'}),
                                    content_type="application/json;charset"
                                                 "=UTF-8")
            user_object = models.User.objects.filter(username=username).first()
            if user_object:
                return HttpResponse(json.dumps({'code': 404, 'msg': "用户名已存在"}),
                                    content_type="application/json;charset=UTF-8")
            user_object = models.User.objects.create(
                name=name,
                username=username,
                password=password,
                role=0,
                login_platform="web",
                create_time=time.time()
            )
            if user_object:
                user_info = model_to_dict(user_object)
                jwt = UserToken.get_token(user_info)
                refreshToken = UserToken.add_salt(user_object.username + str(time.time()))
                return HttpResponse(
                    json.dumps({'code': 200, 'token': jwt, 'data': {'userinfo': user_info, 'refToken': refreshToken}}),
                    content_type="application/json;charset=UTF-8")
            return HttpResponse(json.dumps({'code': 404, 'msg': '创建账号失败'}),
                                content_type="application/json;charset"
                                             "=UTF-8")


def userInfo(request):
    if request.method == "GET":
        userinfo = UserToken.parse_token(request.headers.get('Token'))
        return HttpResponse(json.dumps({'data': userinfo}), content_type="application/json;charset"
                                                                         "=UTF-8")
    return HttpResponse(json.dumps({'code': 404, 'msg': '请求方式问题'}), content_type="application/json;charset"
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
