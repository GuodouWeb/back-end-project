# -*- coding: utf-8 -*-
from django.urls import path, include
from web.app.apis import user
from web.app.apis.request import http

urlpatterns = [
    path('get_userinfo', user.userInfo),
    path('ref_token', user.ref_token),
    path('request', http.request),
    path('login', user.login),
    path('register', user.register),
]