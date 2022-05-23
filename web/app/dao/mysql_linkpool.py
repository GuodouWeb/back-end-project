# -*- coding: utf-8 -*-
from web.locatsettings import Config
from web.uilts.logger import Log
import pymysql

from dbutils.persistent_db import PersistentDB
from dbutils.pooled_db import PooledDB

mysqlSettings = Config.get_Sqlsettins()
TEXT_DB = {"host": mysqlSettings.host, "port": 3306, "user": mysqlSettings.user, "password": mysqlSettings.password,
           "database": mysqlSettings.db, "cursorclass": pymysql.cursors.DictCursor}


class MysqlUtility:
    __pool = None

    def __init__(self, mincached=10, maxcached=20, maxshared=10, maxconnections=200, blocking=True,
                 maxusage=100, setsession=None, reset=True, data_info=None):
        """

        :param mincached:连接池中空闲连接的初始数量
        :param maxcached:连接池中空闲连接的最大数量
        :param maxshared:共享连接的最大数量
        :param maxconnections:创建连接池的最大数量
        :param blocking:超过最大连接数量时候的表现，为True等待连接数量下降，为false直接报错处理
        :param maxusage:单个连接的最大重复使用次数
        :param setsession:optional list of SQL commands that may serve to prepare
            the session, e.g. ["set datestyle to ...", "set time zone ..."]
        :param reset:how connections should be reset when returned to the pool
            (False or None to rollback transcations started with begin(),
            True to always issue a rollback for safety's sake)
        """
        if not self.__pool:
            self.data_info = data_info if data_info else TEXT_DB
            # self.__class__.__pool = PooledDB(creator=pymysql,  **self.data_info)
            self.__class__.__pool = PersistentDB(creator=pymysql, **self.data_info)

    def get_conn(self):
        conn = self.__pool.connection()  # 从连接池获取一个链接
        cursor = conn.cursor()
        return conn, cursor

    @staticmethod
    def select(sql, cursor):
        try:
            cursor.execute(sql)
            # data = cursor.fetchall()
            data = cursor.fetchone()
            return data
        except Exception as e:
            Log().error(f"执行select语句异常：{e}")

    def execute(self, sql, cursor):
        return self._execute_db(sql=sql, cursor=cursor, execute_type=1)

    def executemany(self, sql, cursor):
        return self._execute_db(sql=sql, cursor=cursor, execute_type=2)

    @staticmethod
    def _execute_db(sql, cursor, execute_type, data=None):
        try:
            if execute_type == 1:
                rows = cursor.execute(sql)
            elif execute_type == 2:
                rows = cursor.executemany(sql, data)
            else:
                raise ValueError(f"没有类型为{execute_type}的执行方法")
            return rows
        except Exception as e:
            Log().error(f"执行语句异常：{e}")

    @staticmethod
    def commit(conn):
        conn.commit()

    @staticmethod
    def close(conn, cursor):
        cursor.close()
        conn.close()

    @staticmethod
    def rollback(conn):
        conn.rollback()



