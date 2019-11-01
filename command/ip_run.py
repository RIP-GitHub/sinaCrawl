# -*- coding:utf-8 -*-


import sys
import time
import requests
import traceback
sys.path.append('../')
from sinaCrawl.core.mysql_handler import MysqlHandler


class Ip(object):
    def __init__(self):
        self.mysql = MysqlHandler()
        self.url = 'http://http.tiqu.alicdns.com/getip3?num=20&type=2&pro=&city=0&yys=0&port=1&pack=70023&ts=0&ys=0&cs=0&lb=1&sb=0&pb=45&mr=3&regions='

    def get_ip(self):
        try:
            response = requests.get(self.url).json()
            for item in response['data']:
                ip_info = [
                    (
                        item['ip'],
                        item['port']
                    )
                ]
                sql = 'INSERT INTO tb_ip_info(ip, port) VALUES (%s, %s);'
                self.mysql.insert_info(sql, ip_info)
        except Exception:
            traceback.print_exc()


if __name__ == '__main__':
    # while True:
    #     ip = Ip()
    #     ip.get_ip()
    #     time.sleep(5 * 60)

    ip = Ip()
    ip.get_ip()