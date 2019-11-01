# -*- coding:utf-8 -*-

import pymysql
import traceback
from ..settings import *


class MysqlHandler(object):
    def __init__(self):
        self.mysql_host = MYSQL_HOST
        self.mysql_port = MYSQL_PORT
        self.mysql_user = MYSQL_USER
        self.mysql_passwd = MYSQL_PASSWD
        self.mysql_db = MYSQL_DB
        self.mysql_handler = None

    def create_mysql_connect(self):
        try:
            if self.mysql_handler is None:
                self.mysql_handler = pymysql.connect(
                    host=self.mysql_host,
                    port=self.mysql_port,
                    user=self.mysql_user,
                    passwd=self.mysql_passwd,
                    db=self.mysql_db,
                    use_unicode=True,
                    charset='utf8mb4'
                )
        except Exception:
            self.mysql_handler = None
            traceback.print_exc()

    def query_info(self, sql):
        self.create_mysql_connect()
        cursor = None
        try:
            if self.mysql_handler is not None:
                cursor = self.mysql_handler.cursor()
                if cursor is not None:
                    cursor.execute(sql)
                    get_row = cursor.fetchall()
                    self.mysql_handler.commit()
                    return get_row
                else:
                    if self.mysql_handler is not None:
                        self.mysql_handler.close()
                        self.mysql_handler = None
            if cursor is not None:
                cursor.close()
        except Exception:
            traceback.print_exc()
            if cursor is not None:
                cursor.close()
            if self.mysql_handler is not None:
                self.mysql_handler.close()
                self.mysql_handler = None

    def update_info(self, sql):
        self.create_mysql_connect()
        cursor = None
        try:
            if self.mysql_handler is not None:
                cursor = self.mysql_handler.cursor()
                if cursor is not None:
                    cursor.execute(sql)
                    self.mysql_handler.commit()
                else:
                    if self.mysql_handler is not None:
                        self.mysql_handler.close()
                        self.mysql_handler = None
            if cursor is not None:
                cursor.close()
        except Exception:
            traceback.print_exc()
            if cursor is not None:
                cursor.close()
            if self.mysql_handler is not None:
                self.mysql_handler.close()
                self.mysql_handler = None

    def insert_info(self, sql, user_info):
        self.create_mysql_connect()
        cursor = None
        try:
            if self.mysql_handler is not None:
                cursor = self.mysql_handler.cursor()
                if cursor is not None:
                    cursor.executemany(sql, user_info)
                    self.mysql_handler.commit()
                else:
                    if self.mysql_handler is not None:
                        self.mysql_handler.close()
                        self.mysql_handler = None
            if cursor is not None:
                cursor.close()
        except Exception:
            traceback.print_exc()
            if cursor is not None:
                cursor.close()
            if self.mysql_handler is not None:
                self.mysql_handler.close()
                self.mysql_handler = None
