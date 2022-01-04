# coding: utf-8
import json
import re
from datetime import datetime
import requests
import logging


def get_db_info(subject_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Ailurus/68.0'}
    url = 'https://douban.8610000.xyz/data/{}.json'.format(subject_id)
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'
    info_json = json.loads(r.text)
    fanart = ''
    if 'extra' in info_json and 'backdrops' in info_json['extra']:
        fanart = info_json['extra']['backdrops'][0]
    result = {'basic': {
        'title': info_json['title'],
        '_type': '剧集' if info_json['is_tv'] else '电影',
        'original_title': info_json['original_title'],
        'year': int(info_json['year']),
        'intro': info_json['intro'],
        'trailer': info_json['trailer']['video_url'] if info_json['trailer'] else '',
        'fanart': fanart,
        'update_date': datetime.now(),
        'douban_url': 'https://m.douban.com/movie/subject/{}/'.format(subject_id),
        'thumbnail_url': info_json['pic']['large'],
        'douban_rating': info_json['rating']['value'] if info_json['rating'] else -1,
        'desc_html': ''
        },
        'tags': [tag['name'] for tag in info_json['tags']],
        'directors': [{'name': director['name'],'info': json.dumps(director)} for director in info_json['directors']],
        'actors': [{'name': actor['name'],'info': json.dumps(actor)} for actor in info_json['actors']],
    }
    return result


def get_movie(q_movies,name, year):
    db_id = None
    for movie in q_movies:
        if (movie['original_title'] == name or ''.join(movie['title'].split()) == ''.join(name.split())) and movie['year'] == year:
            db_id = movie['id']
            break
    if not db_id:
        logging.error('获取豆瓣ID出错，数据库可能尚未收录。详见: https://douban.8610000.xyz\n')
        return None
    db_info = get_db_info(db_id)

    return db_info