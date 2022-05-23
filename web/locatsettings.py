# -*- coding: utf-8 -*-
import os


class Config:
    GUEST = 0
    MANAGER = 1
    ADMIN = 2
    LOGS_NAME = os.path.abspath(os.curdir)+"\\logs\\log"

    @staticmethod
    def get_Sqlsettins():
        return MySqlSettings()


class MySqlSettings:
    host = "114.115.164.26"
    user = "root"
    password = "lx!24172024"
    db = "test_db"
    port = 3306
    charset = 'utf8'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 默认
        'NAME': MySqlSettings.db,  # 连接的数据库  #一定要存在的数据库名
        'HOST': MySqlSettings.host,  # mysql的ip地址
        'PORT': MySqlSettings.port,  # mysql的端口
        'USER': MySqlSettings.user,  # mysql的用户名
        'PASSWORD': MySqlSettings.password  # mysql的密码
    }
}
