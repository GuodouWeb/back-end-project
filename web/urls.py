# -*- coding: utf-8 -*-
from django.contrib import admin
from django.urls import path, include
from web.app.view import user

urlpatterns = [
    path('login', user.login),
    path('get_userinfo', user.userInfo),
    path('ref_token', user.ref_token),
]