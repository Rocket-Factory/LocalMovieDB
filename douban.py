# coding: utf-8
import json
import re
from datetime import datetime
import requests
from retrying import retry
import logging


@retry(stop_max_attempt_number=3, wait_fixed=1000)
def get_desc_html(subject_id):
    r = requests.get('https://www.douban.com/doubanapp/h5/movie/{}/desc'.format(subject_id), headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101'})
    r.encoding = 'utf-8'
    return r.text


@retry(stop_max_attempt_number=3, wait_fixed=1000)
def get_db_info(subject_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Ailurus/68.0'}
    url = 'https://douban.8610000.xyz/data/{}.json'.format(subject_id)
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'
    info_json = json.loads(r.text)
    desc_html = get_desc_html(subject_id)
    result = {'basic': {
        'title': info_json['title'],
        '_type': '剧集' if info_json['is_tv'] else '电影',
        'original_title': info_json['original_title'],
        'year': int(info_json['year']),
        'intro': info_json['intro'],
        'update_date': datetime.now(),
        'douban_url': 'https://m.douban.com/movie/subject/{}/'.format(subject_id),
        'thumbnail_url': info_json['pic']['large'],
        'douban_rating': info_json['rating']['value'] if info_json['rating'] else -1,
        'desc_html': desc_html
        },
        'tags': [tag['name'] for tag in info_json['tags']]
    }
    return result


def get_movie(q_movies,name, year):
    db_id = None
    true_name = name
    for movie in q_movies:
        if (movie['title'] == name or ''.join(movie['title'].split()) == ''.join(name.split())) and movie['year'] == year:
            db_id = movie['id']
            break
    if not db_id:
        logging.error('获取豆瓣Subject ID出错，数据库可能尚未收录\n')
        return None
    try:
        db_info = get_db_info(db_id)
    except Exception as e:
        db_info = None
        logging.error('获取豆瓣Subject Info出错\n')

    return db_info
