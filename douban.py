# coding: utf-8
import json
from datetime import datetime
import requests
from config import DB_API_KEY, DB_NAME, DB_PASSWORD
import re

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
    for i in range(0, 3):
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



def get_db_info2(s,subject_id, uri, title):
    url = 'https://movie.douban.com/subject/{}/'.format(subject_id)
    headers = {'User-Agent': UA}
    for i in range(0,3):
        try:
            r0 = s.get(url, headers=headers)
            r0.encoding = 'utf-8'
            html = r0.text
            imdb_id = re.search('>(tt\d+)<',html).group(1)
            api_url = 'https://api.douban.com/v2/movie/imdb/{}?apikey={}'.format(imdb_id,DB_API_KEY)
            r1 = s.get(api_url, headers=headers)
            r1.encoding = 'utf-8'
            info_json = json.loads(r1.text)
            result = {'basic': {
                'title': title,
                '_type': '剧集' if 'episodes' in info_json['attrs'] else '电影',
                'original_title': info_json['attrs']['title'][0],
                'year': int(info_json['attrs']['year'][0]),
                'update_date': datetime.now(),
                'uri': uri,
                'douban_url': info_json['mobile_link'],
                'thumbnail_url': info_json['image'],
                'douban_rating': info_json['rating']['average']},
                'tags': [tag['name'] for tag in info_json['tags']]}
            return result
            
        except Exception:
            print('第{}次获取info错误'.format(i))
    return None

def get_db_info(s,subject_id, uri, title):
    url = 'https://api.douban.com/v2/movie/subject/{}?apikey={}'.format(subject_id, DB_API_KEY)
    headers = {'User-Agent': UA}
    for i in range(0, 3):
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
            print('第{}次获取info错误'.format(i))
    print('尝试从IMDB API获取info...')
    result = get_db_info2(s,subject_id, uri, title)
    return result
