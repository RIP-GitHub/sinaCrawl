# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SinacrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class UserItem(scrapy.Item):
    user_id = scrapy.Field()
    medium_type = scrapy.Field()
    user_name = scrapy.Field()
    user_url = scrapy.Field()
    user_avatar = scrapy.Field()
    user_desc = scrapy.Field()
    user_gender = scrapy.Field()
    user_location = scrapy.Field()
    user_verified = scrapy.Field()
    verified_reason = scrapy.Field()
    article_num = scrapy.Field()
    follow_num = scrapy.Field()
    fans_num = scrapy.Field()


class FollowerItem(scrapy.Item):
    user_id = scrapy.Field()
    follower_id = scrapy.Field()


class FansItem(scrapy.Item):
    user_id = scrapy.Field()
    fans_id = scrapy.Field()


class WeiboItem(scrapy.Item):
    user_id = scrapy.Field()
    weibo_id = scrapy.Field()
    weibo_url = scrapy.Field()
    content = scrapy.Field()
    publish_time = scrapy.Field()
    like_num = scrapy.Field()
    repost_num = scrapy.Field()
    comment_num = scrapy.Field()
    text = scrapy.Field()


class CommentItem(scrapy.Item):
    user_id = scrapy.Field()
    weibo_id = scrapy.Field()
    comment_user_id = scrapy.Field()
    comment_id = scrapy.Field()
    comment_text = scrapy.Field()
    comment_time = scrapy.Field()
    comment_like_num = scrapy.Field()
