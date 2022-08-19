#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models


class User(models.Model):
    name = models.CharField(max_length=32)
    phone = models.IntegerField(unique=True)
    email = models.IntegerField(unique=True)
    username = models.CharField(unique=True, max_length=32)
    password = models.CharField(max_length=64)
    role = models.IntegerField()
    login_platform = models.CharField(max_length=16)
    create_time = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user'
        app_label = 'web'