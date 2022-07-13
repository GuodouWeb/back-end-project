# -*- coding: utf-8 -*-
from django.urls import path
from web.app.apis.devices import android

urlpatterns = [
    path('get_devices', android.getDevices),
    path('get_Pkgname', android.getPkgname)
]