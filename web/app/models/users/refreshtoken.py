#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models


class Refreshtoken(models.Model):
    token_key = models.CharField(unique=True, max_length=64)
    token_value = models.CharField(max_length=64)
    expiration_time_stamp = models.IntegerField()
    status = models.IntegerField(blank=True, null=True)
    username = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'RefreshToken'
