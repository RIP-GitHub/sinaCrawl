# -*- coding:utf-8 -*-

import sys
import time
import traceback
sys.path.append('../')
from sinaCrawl.settings import *
from sinaCrawl.core.mysql_handler import MysqlHandler
from sinaCrawl.core.redis_handler import RedisHandler


class Push(object):
    def __init__(self):
        self.mysql = MysqlHandler()
        self.redis = RedisHandler()

    def push(self):
        try:
            sql = 'SELECT user_id FROM tb_user_info WHERE user_url LIKE \'%weibo%\';'
            row = self.mysql.query_info(sql)
            for item in row:
                # self.redis.lpush_to_redis(USER_SPIDER_KEY, 'https://weibo.cn/{}/info'.format(item[0]))
                self.redis.lpush_to_redis(USER_SPIDER_KEY, 'https://m.weibo.cn/api/container/getIndex?type=uid&value={}&containerid=100505{}'.format(item[0], item[0]))
                break
        except Exception:
            traceback.print_exc()


if __name__ == '__main__':
    while True:
        push = Push()
        push.push()
        time.sleep(24 * 60 * 60)

