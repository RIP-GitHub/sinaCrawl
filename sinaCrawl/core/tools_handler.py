# -*- coding:utf-8 -*-

import re
import json
import datetime
import traceback


def judge_verified(data):
    try:
        if data:
            return 1
        else:
            return 0
    except Exception:
        traceback.print_exc()


def judge_gender(data):
    try:
        if data == '女':
            return -1
        elif data == '男':
            return 1
        else:
            return 0
    except Exception:
        traceback.print_exc()


def judge_empty(data):
    try:
        if data and data[0]:
            return data[0].replace(u'\xa0', '')
    except Exception:
        traceback.print_exc()


def get_user_verified(verified_reason):
    try:
        if verified_reason:
            return 1
        else:
            return -1
    except Exception:
        traceback.print_exc()


def standardize_num(num):
    try:
        if num:
            return int(num[0])
    except Exception:
        traceback.print_exc()


def parse_content(response):
    try:
        weibo_id = re.findall(r'name=(\d+) target', response.text)[0]
        print(response.meta)
        print(weibo_id)
    except Exception:
        traceback.print_exc()


def standardize_time(time_string):
    try:
        now_time = datetime.datetime.now()
        if '分钟前' in time_string:
            minutes = re.search(r'^(\d+)分钟', time_string).group(1)
            created_at = now_time - datetime.timedelta(minutes=int(minutes))
            return created_at.strftime('%Y-%m-%d %H:%M') + ':00'

        if '小时前' in time_string:
            minutes = re.search(r'^(\d+)小时', time_string).group(1)
            created_at = now_time - datetime.timedelta(hours=int(minutes))
            return created_at.strftime('%Y-%m-%d %H:%M') + ':00'

        if '今天' in time_string and ':' not in time_string:
            return time_string.replace('今天', now_time.strftime('%Y-%m-%d')) + ' 00:00:00'

        if '月' in time_string:
            time_string = time_string.replace('月', '-').replace('日', '')
            time_string = str(now_time.year) + '-' + time_string
            return time_string + ':00'

        if '+0800' in time_string:
            date = time_string.split(' ')
            month = {
                'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12',
            }
            created_at = '{}-{}-{} {}'.format(date[5], month[date[1]], date[2], date[3])
            return created_at

        if '今天' in time_string and ':' in time_string:
            return time_string.replace('今天', now_time.strftime('%Y-%m-%d')) + ':00'

        return time_string
    except Exception:
        traceback.print_exc()


def extract_response(response):
    try:
        data = response.xpath('//script/text()').extract()[1]
        html = data[data.find('"status":'):]
        html = html[:html.rfind('"hotScheme"')]
        html = html[:html.rfind(',')]
        html = '{' + html + '}'
        return html
    except Exception:
        traceback.print_exc()


def get_content(weibo_info):
    try:
        text = standardize_content_text(weibo_info)
        if weibo_info.get('retweeted_status'):
            retweet_text = standardize_content_text(weibo_info['retweeted_status'])
        else:
            retweet_text = []

        img = standardize_content_img(weibo_info)
        if weibo_info.get('retweeted_status'):
            retweet_img = standardize_content_img(weibo_info['retweeted_status'])
        else:
            retweet_img = []

        video, link = standardize_content_video_link(weibo_info)
        if weibo_info.get('retweeted_status'):
            retweet_video, retweet_link = standardize_content_video_link(weibo_info['retweeted_status'])
        else:
            retweet_video, retweet_link = {}, {}

        content = []
        for item in text + retweet_text:
            content.append({'type': 'text', 'data': item})
        for item in img + retweet_img:
            content.append({'type': 'img', 'data': item})
        for item in [video, retweet_video]:
            content.append({'type': 'video', 'data': item})
        for item in [link, retweet_link]:
            content.append({'type': 'link', 'data': item})
        str_content = json.dumps(content, ensure_ascii=False)
        str_text = ''
        for item in content:
            if item['type'] == 'text':
                str_text += item['data']
        return str_content, str_text
    except Exception:
        traceback.print_exc()


def standardize_content_text(status):
    try:
        if status.get('text'):
            text_body = status['text']
            content = re.sub(r'<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>', '', text_body)
            content = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', content)
            content = re.sub(r'<\/?span.*?>', '', content)
            content = re.sub(r'<\/?strong.*?>', '', content)
            content = re.sub(r'<img.*?>', '', content)
            content = re.sub(r'<\/?a.*?>', '', content)
            text = content.split('<br />')
        else:
            text = []
        return text
    except Exception:
        traceback.print_exc()


def standardize_content_img(status):
    try:
        if status.get('pics'):
            pic_info = status['pics']
            img = [pic['large']['url'] for pic in pic_info]
        else:
            img = []
        return img
    except Exception:
        traceback.print_exc()


def standardize_content_video_link(status):
    try:
        video, link = {}, {}
        if status.get('page_info'):
            page_info = status['page_info']
            if page_info['type'] == 'video':
                if page_info.get('media_info'):
                    cover_image = page_info['page_pic']['url']
                    original_url = page_info['media_info']['stream_url']
                    qiniu_url = original_url
                    video = {
                        'cover_image': cover_image,
                        'original_url': original_url,
                        'qiniu_url': qiniu_url
                    }
            elif page_info['type'] == 'article':
                link_url = page_info['page_url']
                page_title = page_info['page_title']
                content1 = page_info['content1']
                pic_url = ''
                if page_info.get('content2'):
                    content2 = page_info['content2']
                else:
                    content2 = ''
                link = {
                    'link_url': link_url,
                    'pic_url': pic_url,
                    'page_title': page_title,
                    'content1':  content1,
                    'content2': content2
                }
            else:
                video, link = {}, {}
        else:
            video, link = {}, {}
        return video, link
    except Exception:
        traceback.print_exc()


def extract_comment_content(comment_html):
    try:
        keyword_re = re.compile('<span class="kt">|</span>|原图|<!-- 是否进行翻译 -->|')
        emoji_re = re.compile('<img alt="|" src="//h5\.sinaimg(.*?)/>')
        white_space_re = re.compile('<br />')
        div_re = re.compile('</div>|<div>')
        image_re = re.compile('<img(.*?)/>')
        url_re = re.compile('<a href=(.*?)>|</a>')
        s = comment_html
        if 'class="ctt">' in s:
            s = s.split('class="ctt">', maxsplit=1)[1]
        s = s.split('举报', maxsplit=1)[0]
        s = emoji_re.sub('', s)
        s = keyword_re.sub('', s)
        s = url_re.sub('', s)
        s = div_re.sub('', s)
        s = image_re.sub('', s)
        s = white_space_re.sub(' ', s)
        s = s.replace('\xa0', '').replace('评论配图', '')
        s = s.strip(':')
        s = s.strip()
        return s
    except Exception:
        traceback.print_exc()
