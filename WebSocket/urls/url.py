# -*- coding: utf-8 -*-
# chat/Urls.py
from django.urls import path

from .. import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.room, name='room'),
]
