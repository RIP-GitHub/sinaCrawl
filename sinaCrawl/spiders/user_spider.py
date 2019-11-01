# -*- coding:utf-8 -*-

import math
from ..items import *
from lxml import etree
from ..settings import *
from scrapy.http import Request
from ..core.tools_handler import *
from scrapy_redis.spiders import RedisSpider


class UserSpider(RedisSpider):
    def __init__(self, *kargs, **kwargs):
        super(UserSpider, self).__init__(*kargs, **kwargs)

    name = USER_SPIDER_NAME
    allowd_domains = []
    redis_key = USER_SPIDER_KEY

    def parse(self, response):
        try:
            user_info = json.loads(response.text)['data']['userInfo']
            user_id = user_info['id']
            medium_type = 'weibo'
            user_name = user_info['screen_name']
            user_url = 'https://m.weibo.cn/u/{}'.format(user_info['id'])
            user_avatar = user_info['profile_image_url']
            user_desc = user_info['description']
            user_gender = judge_gender(user_info['gender'])
            user_location = ''
            user_verified = judge_verified(user_info['verified'])
            verified_reason = user_info.get('verified_reason')
            article_num = user_info['statuses_count']
            follow_num = user_info['follow_count']
            fans_num = user_info['followers_count']
            user_item = UserItem(
                user_id=user_id,
                medium_type=medium_type,
                user_name=user_name,
                user_url=user_url,
                user_avatar=user_avatar,
                user_desc=user_desc,
                user_gender=user_gender,
                user_location=user_location,
                user_verified=user_verified,
                verified_reason=verified_reason,
                article_num=article_num,
                follow_num=follow_num,
                fans_num=fans_num
            )
            yield user_item
            # 最多可获取 10(page) * 20(count) = 200 条关注信息
            if user_item['follow_num'] > 200:
                follow_page = 11
            else:
                follow_page = int(math.ceil(user_item['follow_num'] / 20.0))
            for page_num in range(1, follow_page):
                yield Request(
                    url='https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{}&page={}'.format(user_item['user_id'], page_num),
                    callback=self.parse_follow,
                    dont_filter=True
                )
                break
            # 最多可获取 250(page) * 20(count) = 5000 条粉丝信息
            if user_item['fans_num'] > 200:
                fans_page = 251
            else:
                fans_page = int(math.ceil(user_item['fans_num'] / 20.0))
            for page_num in range(1, fans_page):
                yield Request(
                    url='https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{}&since_id={}'.format(user_item['user_id'], page_num),
                    callback=self.parse_fans,
                    dont_filter=True
                )
                break
            # 最多可获取全部微博信息
            for page_num in range(1, int(math.ceil(user_item['article_num'] / 10.0))):
                yield Request(
                    url='https://m.weibo.cn/api/container/getIndex?containerid=107603{}&page={}'.format(user_item['user_id'], page_num),
                    callback=self.parse_one_page_weibo,
                    dont_filter=True,
                )
                break
        except Exception:
            traceback.print_exc()

    # def parse(self, response):
    #     try:
    #         user_id = re.findall(r'cn/(\d+)/info', response.url)[0]
    #         medium_type = 'weibo'
    #         user_name = judge_empty(re.findall('昵称:(.*?)<br/>', response.text))
    #         user_url = 'https://m.weibo.cn/u/{}'.format(user_id)
    #         user_avatar = judge_empty(response.xpath('//div[@class="c"]/img/@src').extract())
    #         user_desc = judge_empty(re.findall('简介:(.*?)<br/>', response.text))
    #         user_gender = judge_gender(judge_empty(re.findall('性别:(.*?)<br/>', response.text)))
    #         user_location = judge_empty(re.findall('地区:(.*?)<br/>', response.text))
    #         verified_reason = judge_empty(re.findall('认证:(.*?)<br/>', response.text))
    #         user_verified = get_user_verified(verified_reason)
    #
    #         user_item = UserItem(
    #             user_id=user_id,
    #             medium_type=medium_type,
    #             user_name=user_name,
    #             user_url=user_url,
    #             user_avatar=user_avatar,
    #             user_desc=user_desc,
    #             user_gender=user_gender,
    #             user_location=user_location,
    #             user_verified=user_verified,
    #             verified_reason=verified_reason,
    #             article_num=0,
    #             follow_num=0,
    #             fans_num=0
    #         )
    #         request_meta = response.meta
    #         request_meta['item'] = user_item
    #         yield Request(
    #             url='https://weibo.cn/u/{}'.format(user_id),
    #             callback=self.parse_further_user,
    #             meta=request_meta,
    #             dont_filter=True,
    #             priority=1
    #         )
    #     except Exception:
    #         traceback.print_exc()
    #
    # def parse_further_user(self, response):
    #     try:
    #         user_item = response.meta['item']
    #         user_item['article_num'] = standardize_num(re.findall(r'微博\[(\d+)\]', response.text))
    #         user_item['follow_num'] = standardize_num(re.findall(r'关注\[(\d+)\]', response.text))
    #         user_item['fans_num'] = standardize_num(re.findall(r'粉丝\[(\d+)\]', response.text))
    #         yield user_item
    #
    #         # 最多可获取 10(page) * 20(count) = 200 条关注信息
    #         if user_item['follow_num'] > 200:
    #             follow_page = 11
    #         else:
    #             follow_page = int(math.ceil(user_item['follow_num'] / 20.0))
    #         for page_num in range(1, follow_page):
    #             yield Request(
    #                 url='https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{}&page={}'.format(user_item['user_id'], page_num),
    #                 callback=self.parse_follow,
    #                 dont_filter=True
    #             )
    #             # break
    #
    #         # 最多可获取 250(page) * 20(count) = 5000 条粉丝信息
    #         if user_item['fans_num'] > 200:
    #             fans_page = 251
    #         else:
    #             fans_page = int(math.ceil(user_item['fans_num'] / 20.0))
    #         for page_num in range(1, fans_page):
    #             yield Request(
    #                 url='https://m.weibo.cn/api/container/getIndex?containerid=231051_-_fans_-_{}&since_id={}'.format(user_item['user_id'], page_num),
    #                 callback=self.parse_fans,
    #                 dont_filter=True
    #             )
    #             # break
    #
    #         # 最多可获取全部微博信息
    #         for page_num in range(1, int(math.ceil(user_item['article_num'] / 10.0))):
    #             yield Request(
    #                 url='https://m.weibo.cn/api/container/getIndex?containerid=107603{}&page={}'.format(user_item['user_id'], page_num),
    #                 callback=self.parse_one_page_weibo,
    #                 dont_filter=True,
    #             )
    #             # break
    #     except Exception:
    #         traceback.print_exc()

    def parse_follow(self, response):
        try:
            data = json.loads(response.text)
            user_id = int(re.findall(r'=231051_-_followers_-_(\d+)&', response.url)[0])
            if data['data']['cards']:
                if int(re.findall(r'&page=(\d+)$', response.url)[0]) == 1:
                    index = -1
                else:
                    index = 0
                for item in data['data']['cards'][index]['card_group']:
                    follower_item = FollowerItem(
                        user_id=user_id,
                        follower_id=item['user']['id']
                    )
                    yield follower_item
        except Exception:
            traceback.print_exc()

    def parse_fans(self, response):
        try:
            data = json.loads(response.text)
            user_id = int(re.findall(r'=231051_-_fans_-_(\d+)&', response.url)[0])
            if data['data']['cards']:
                if int(re.findall(r'&since_id=(\d+)$', response.url)[0]) == 1:
                    index = -1
                else:
                    index = 0
                for item in data['data']['cards'][index]['card_group']:
                    fans_item = FansItem(
                        user_id=user_id,
                        fans_id=item['user']['id']
                    )
                    yield fans_item
        except Exception:
            traceback.print_exc()

    def parse_one_page_weibo(self, response):
        try:
            data = json.loads(response.text)
            for item in data['data']['cards']:
                if item['card_type'] == 9:
                    yield Request(
                        url='https://m.weibo.cn/detail/{}'.format(item['mblog']['id']),
                        callback=self.parse_one_weibo,
                        dont_filter=True
                    )
                    yield Request(
                        url='https://weibo.cn/comment/{}?page=1'.format(item['mblog']['bid']),
                        callback=self.parse_comment,
                        meta={'weibo_id': item['mblog']['id'], 'user_id': item['mblog']['user']['id']},
                        dont_filter=True
                    )
        except Exception:
            traceback.print_exc()

    def parse_one_weibo(self, response):
        try:
            if '打开微博客户端，查看全文' in response.text:
                pass
            else:
                data = json.loads(extract_response(response))
                user_id = data['status']['user']['id']
                weibo_id = data['status']['id']
                weibo_url = response.url
                publish_time = standardize_time(data['status']['created_at'])
                like_num = data['status']['attitudes_count']
                repost_num = data['status']['reposts_count']
                comment_num = data['status']['comments_count']
                content, text = get_content(data['status'])
                weibo_item = WeiboItem(
                    user_id=user_id,
                    weibo_id=weibo_id,
                    weibo_url=weibo_url,
                    content=content,
                    publish_time=publish_time,
                    like_num=like_num,
                    repost_num=repost_num,
                    comment_num=comment_num,
                    text=text
                )
                yield weibo_item
        except Exception:
            traceback.print_exc()

    def parse_comment(self, response):
        try:
            tree_node = etree.HTML(response.body)
            comment_nodes = tree_node.xpath('//div[@class="c" and contains(@id,"C_")]')
            for comment_node in comment_nodes:
                comment_user_url = comment_node.xpath('.//a[contains(@href,"/u/")]/@href')
                if not comment_user_url:
                    continue
                user_id = response.meta['user_id']
                weibo_id = response.meta['weibo_id']
                comment_user_id = re.search(r'/u/(\d+)', comment_user_url[0]).group(1)
                comment_id = comment_node.xpath('./@id')[0].replace('C_', '')
                comment_text = extract_comment_content(etree.tostring(comment_node, encoding='unicode'))
                comment_time = standardize_time(comment_node.xpath('.//span[@class="ct"]/text()')[0].split('\xa0')[0])
                comment_like_num = comment_node.xpath('.//a[contains(text(),"赞[")]/text()')[-1][-2]

                comment_item = CommentItem(
                    user_id=user_id,
                    weibo_id=weibo_id,
                    comment_user_id=comment_user_id,
                    comment_id=comment_id,
                    comment_text=comment_text,
                    comment_time=comment_time,
                    comment_like_num=comment_like_num,
                )
                yield comment_item
        except Exception:
            traceback.print_exc()
