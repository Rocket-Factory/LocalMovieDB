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
def get_db_id(name, year):
    true_name = name
    # 处理特殊符号
    for index,s in enumerate(name):
        if s in [',', ':','(','[', ' ']:
            name = name[:index]
            break
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Ailurus/68.0'}
    url = 'https://alagorn.8610000.xyz/api/v1/movies/suggest_query?q={}'.format(name)
    r = requests.get(url, headers=headers)
    if 'code' in r.json():
        return None
    for movie_info in r.json():
        if (movie_info['title'] == true_name or ''.join(movie_info['title'].split()) == ''.join(true_name.split())) and movie_info['year'] == year:
            return movie_info['id']
    return None


@retry(stop_max_attempt_number=3, wait_fixed=1000)
def get_db_info(subject_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Ailurus/68.0'}
    url = 'https://alagorn.8610000.xyz/api/v1/movie/{}'.format(subject_id)
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


def get_movie(name, year):
    try:
        db_id = get_db_id(name, year)
    except Exception as e:
        db_id= None
    if not db_id:
        logging.error('获取豆瓣Subject ID出错\n')
        return None
    try:
        db_info = get_db_info(db_id)
    except Exception as e:
        db_info = None
        logging.error('获取豆瓣Subject Info出错\n')

    return db_info
