#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models

class DjangoSession(models.Model):
    session_key = models.CharField(max_length=255, blank=True, null=True)
    session_data = models.CharField(max_length=255, blank=True, null=True)
    expire_date = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_session'