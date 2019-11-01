# -*- coding:utf-8 -*-

import sys
import time
import traceback
sys.path.append('../')
from sinaCrawl.core.mysql_handler import MysqlHandler
from sinaCrawl.core.login_handler import LoginHandler


class Login(object):
    def __init__(self):
        self.mysql = MysqlHandler()

    def login(self):
        try:
            sql = 'SELECT * FROM tb_account_info WHERE status != 1;'
            row = self.mysql.query_info(sql)
            for item in row:
                cookie = LoginHandler(item[0], item[1]).run()
                if cookie:
                    print('=========={}==========\n获取cookie成功\nCookie: {}'.format(item[0], cookie))
                    sql = 'UPDATE tb_account_info SET status = 1, cookie = \'{}\' WHERE username = \'{}\';'.format(cookie, item[0])
                    self.mysql.update_info(sql)
                else:
                    print('=========={}==========\n获取cookie失败\n请检查账号密码信息'.format(item[0]))
                    sql = 'UPDATE tb_account_info SET status = -1 WHERE username = \'{}\';'.format(item[0])
                    self.mysql.update_info(sql)
        except Exception:
            traceback.print_exc()


if __name__ == '__main__':
    while True:
        login = Login()
        login.login()
        time.sleep(24 * 60 * 60)