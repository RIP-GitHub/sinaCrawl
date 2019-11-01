# -*- coding:utf-8 -*-

import sys
sys.path.append('../')
from scrapy import cmdline
from sinaCrawl.settings import USER_SPIDER_NAME


if __name__ == '__main__':
    cmdline.execute(['scrapy', 'crawl', USER_SPIDER_NAME])
