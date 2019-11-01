# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from .items import *
from .core.mysql_handler import MysqlHandler


class SinacrawlPipeline(object):
    def __init__(self):
        self.mysql = MysqlHandler()

    def process_item(self, item, spider):
        if isinstance(item, UserItem):
            print(
                '用户ID: {}\n用户平台: {}\n用户昵称: {}\n用户主页: {}\n用户头像: {}\n用户简介: {}\n用户性别: {}\n'
                '用户位置: {}\n用户验证: {}\n验证原因: {}\n博文数: {}\n关注数: {}\n粉丝数: {}\n'.format(
                    item['user_id'], item['medium_type'], item['user_name'], item['user_url'], item['user_avatar'],
                    item['user_desc'], item['user_gender'], item['user_location'], item['user_verified'],
                    item['verified_reason'], item['article_num'], item['follow_num'], item['fans_num']
                )
            )
            user_info = [
                (
                    item['user_id'],
                    item['medium_type'],
                    item['user_name'],
                    item['user_url'],
                    item['user_avatar'],
                    item['user_desc'],
                    item['user_gender'],
                    item['user_location'],
                    item['user_verified'],
                    item['verified_reason'],
                    item['article_num'],
                    item['follow_num'],
                    item['fans_num']
                )
            ]
            sql = 'INSERT INTO tb_kol_user_info (user_id, medium_type, user_name, user_url, user_avatar, user_desc, ' \
                  'user_gender, user_location, user_verified, verified_reason, article_num, follower_num, fans_num) ' \
                  'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE ' \
                  'user_id = VALUES (user_id), medium_type = VALUES (medium_type), user_name = VALUES (user_name), ' \
                  'user_url = VALUES (user_url), user_desc = VALUES (user_desc), user_gender = VALUES (user_gender), ' \
                  'user_location = VALUES (user_location), user_verified = VALUES (user_verified), ' \
                  'verified_reason = VALUES (verified_reason), article_num = VALUES (article_num), ' \
                  'follower_num = VALUES (follower_num), fans_num = VALUES (fans_num);'
            self.mysql.insert_info(sql, user_info)
        if isinstance(item, FollowerItem):
            print('{} 关注了 {}\n'.format(item['user_id'], item['follower_id']))
            follower_info = [
                (
                    item['user_id'],
                    item['follower_id']
                )
            ]
            sql = 'INSERT INTO tb_follower_relationship (user_id, follower_id) VALUES (%s, %s) ON DUPLICATE KEY ' \
                  'UPDATE user_id = VALUES (user_id), follower_id = VALUES (follower_id);'
            self.mysql.insert_info(sql, follower_info)
        if isinstance(item, FansItem):
            print('{} 关注了 {}\n'.format(item['fans_id'], item['user_id']))
            fans_info = [
                (
                    item['user_id'],
                    item['fans_id']
                )
            ]
            sql = 'INSERT INTO tb_fans_relationship (user_id, fans_id) VALUES (%s, %s) ON DUPLICATE KEY ' \
                  'UPDATE user_id = VALUES (user_id), fans_id = VALUES (fans_id);'
            self.mysql.insert_info(sql, fans_info)
        if isinstance(item, WeiboItem):
            print(
                '博文ID: {}\n用户ID: {}\n博文内容: {}\n博文封面: {}\n发布时间: {}\n点赞数: {}\n转发数: {}\n收藏数: {}\n'
                '评论数: {}\n阅读数: {}\n'.format(item['weibo_id'], item['user_id'], item['content'],  '',
                    item['publish_time'], item['like_num'], item['repost_num'], 0, item['comment_num'], 0
                )
            )
            article_info = [
                (
                    item['weibo_id'],
                    item['user_id'],
                    item['content'],
                    '',
                    item['publish_time'],
                    item['text']
                )
            ]
            article_sql = 'INSERT INTO tb_kol_article_info (article_id, user_id, content, cover_image, publish_time, ' \
                          'text) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE ' \
                          'article_id = VALUES (article_id), user_id = VALUES (user_id), content = VALUES (content), ' \
                          'cover_image = VALUES (cover_image), publish_time = VALUES (publish_time), ' \
                          'text = VALUES (text);'
            self.mysql.insert_info(article_sql, article_info)
            num_info = [
                (
                    item['weibo_id'],
                    item['like_num'],
                    item['repost_num'],
                    0,
                    item['comment_num'],
                    0
                )
            ]
            num_sql = 'INSERT INTO tb_kol_num_info (article_id, like_num, repost_num, collect_num, comment_num, ' \
                      'read_num) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE ' \
                      'article_id = VALUES (article_id), like_num = VALUES (like_num), ' \
                      'repost_num = VALUES (repost_num), collect_num = VALUES (collect_num), ' \
                      'comment_num = VALUES (comment_num), read_num = VALUES (read_num);'
            self.mysql.insert_info(num_sql, num_info)
        if isinstance(item, CommentItem):
            print(
                '博文ID: {}\n用户ID: {}\n评论用户ID: {}\n评论ID: {}\n评论内容: {}\n评论时间: {}\n评论点赞数: {}\n'.format(
                    item['weibo_id'], item['user_id'], item['comment_user_id'], item['comment_id'],
                    item['comment_text'], item['comment_time'], item['comment_like_num']
                )
            )
            comment_info = [
                (
                    item['user_id'],
                    item['weibo_id'],
                    item['comment_user_id'],
                    item['comment_id'],
                    item['comment_text'],
                    item['comment_time'],
                    item['comment_like_num']
                )
            ]
            sql = 'INSERT INTO tb_kol_comment_info (user_id, article_id, comment_user_id, comment_id, comment_text, ' \
                  'comment_time, comment_like_num) VALUES (%s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE ' \
                  'user_id = VALUES (user_id), article_id = VALUES (article_id), ' \
                  'comment_user_id = VALUES (comment_user_id), comment_id = VALUES (comment_id), ' \
                  'comment_text = VALUES (comment_text), comment_time = VALUES (comment_time), ' \
                  'comment_like_num = VALUES (comment_like_num);'
            self.mysql.insert_info(sql, comment_info)
