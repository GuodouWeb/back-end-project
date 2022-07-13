# -*- coding: utf-8 -*-
from django.urls import path, include
from web.app.apis import user
from web.app.apis.request import http

urlpatterns = [
    path('user/', include('web.Urls.user')),
    path('devices/', include('web.Urls.devices.Android')),
    path('ref_token', user.ref_token),
    path('request', http.request),
]
