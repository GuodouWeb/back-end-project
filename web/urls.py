# -*- coding: utf-8 -*-
from django.contrib import admin
from django.urls import path, include
from web.app.view import user, request
from web.app.view.request import http

urlpatterns = [
    path('get_userinfo', user.userInfo),
    path('ref_token', user.ref_token),
    path('request', http.request),
    # path('user/', include('web.urls.user')),
    path('user/', include([
        path('login', user.login),
        path('register', user.register),
        ], None)),
]
