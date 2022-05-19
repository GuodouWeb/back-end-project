# -*- coding: utf-8 -*-


class Config:
    GUEST = 0
    MANAGER = 1
    ADMIN = 2

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
    cursorclass = ""

    @classmethod
    def Cursorclass(cls, pymysql_cursors):
        cls.cursorclass = pymysql_cursors
        return cls.cursorclass


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 默认
        'NAME': 'test_db',  # 连接的数据库  #一定要存在的数据库名
        'HOST': '114.115.164.26',  # mysql的ip地址
        'PORT': 3306,  # mysql的端口
        'USER': 'root',  # mysql的用户名
        'PASSWORD': 'lx!24172024'  # mysql的密码
    }
}
