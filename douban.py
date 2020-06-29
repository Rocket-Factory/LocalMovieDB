# coding: utf-8
import json
from datetime import datetime
import requests
from config import DB_API_KEY, DB_NAME, DB_PASSWORD

UA = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0)'


def login():
    url_basic = 'https://accounts.douban.com/j/mobile/login/basic'
    url = 'https://www.douban.com/'
    ua_headers = {"User-Agent": UA}
    data = {
        'ck': '',
        'name': DB_NAME,
        'password': DB_PASSWORD,
        'remember': 'True',
        'ticket': ''
    }

    s = requests.session()
    r0 = s.get(url=url_basic, headers=ua_headers)
    r1 = s.post(url=url_basic, headers=ua_headers, data=data)
    r2 = s.get(url=url, headers=ua_headers)

    if json.loads(r1.text)['status'] == 'success':
        return s
    else:
        return None


def get_db_id2(s,name, year):
    headers = {'User-Agent': UA}
    url = 'https://movie.douban.com/j/subject_suggest?q={}'.format(name)
    for i in range(0, 5):
        try:
            r = s.get(url, headers=headers)
            r.encoding = 'utf-8'
            info_json = json.loads(r.text)
            for movie_info in info_json:
                if movie_info['title'] == name and movie_info['year'] == year:
                    return movie_info['id']
        except Exception:
            print('第{}次获取ID错误'.format(i))
    return None


def get_db_info(s,subject_id, uri):
    url = 'https://api.douban.com/v2/movie/subject/{}?apikey={}'.format(subject_id, DB_API_KEY)
    headers = {'User-Agent': UA}
    for i in range(0, 5):
        try:
            r = s.get(url, headers=headers)
            r.encoding = 'utf-8'
            info_json = json.loads(r.text)
            result = {'basic': {
                'title': info_json['title'],
                '_type': '剧集' if info_json['episodes_count'] else '电影',
                'original_title': info_json['original_title'],
                'year': int(info_json['year']),
                'update_date': datetime.now(),
                'uri': uri,
                'douban_url': info_json['share_url'],
                'thumbnail_url': info_json['images']['medium'],
                'douban_rating': info_json['rating']['average']},
                'tags': info_json['tags']}
            return result
        except Exception:
            print('第{}次获取ID错误'.format(i))
    return None
