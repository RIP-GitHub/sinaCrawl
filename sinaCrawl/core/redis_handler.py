# -*- coding:utf-8 -*-

import redis
import traceback
from ..settings import *


class RedisHandler(object):
    def __init__(self):
        self.redis_host = REDIS_HOST
        self.redis_port = REDIS_PORT
        self.redis_password = REDIS_PARAMS['password']
        self.redis_dbindex = REDIS_DB
        self.redis_expire = REDIS_EXPIRE
        self.redis_pool = None

    def create_redis_connection(self):
        try:
            if self.redis_pool is None:
                self.redis_pool = redis.ConnectionPool(
                    host=self.redis_host,
                    port=self.redis_port,
                    password=self.redis_password,
                    db=self.redis_dbindex
                )
            r = redis.Redis(connection_pool=self.redis_pool)
            if r is not None:
                return r
            else:
                self.redis_pool = None
        except Exception:
            traceback.print_exc()
            return None

    def lpush_to_redis(self, redis_key, redis_value):
        try:
            r = self.create_redis_connection()
            if r is not None:
                v = r.lpush(redis_key, redis_value)
                if v is None:
                    print('push----key: {} value: {} failed'.format(redis_key, redis_value))
                else:
                    print('push----key: {} value: {} success, after {} seconds delete'.format(redis_key, redis_value, self.redis_expire))
                    r.expire(redis_key, self.redis_expire)
        except Exception:
            self.redis_pool = None
            traceback.print_exc()
            print('push----key: {} value: {} failed'.format(redis_key, redis_value))


