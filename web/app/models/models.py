# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
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


class DjangoSession(models.Model):
    session_key = models.CharField(max_length=255, blank=True, null=True)
    session_data = models.CharField(max_length=255, blank=True, null=True)
    expire_date = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_session'


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
