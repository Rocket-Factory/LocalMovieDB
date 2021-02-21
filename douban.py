# coding: utf-8
import json
import re
from datetime import datetime
import requests
from retrying import retry
import logging
from config import PROXY_URL, PROXY

TMDB_API_KEY = '594d85b1258209191e56353c08bd2101'


@retry(stop_max_attempt_number=3, wait_fixed=2000)
def get_fanart(imdb_id, is_tv):
    if imdb_id == '':
        return ''
    if PROXY:
        r0 = requests.get('https://api.themoviedb.org/3/find/{}?api_key={}&external_source=imdb_id'.format(imdb_id,TMDB_API_KEY), proxies={'http': PROXY_URL, 'https': PROXY_URL})
    else:
        r0 = requests.get('https://api.themoviedb.org/3/find/{}?api_key={}&external_source=imdb_id'.format(imdb_id,TMDB_API_KEY))
 
    
    # 剧集  
    if is_tv and r0.json()['tv_results'] != []:
        result = r0.json()['tv_results'][0]
        if 'backdrop_path' in result and result['backdrop_path']:
            return result['backdrop_path']
    # 电影
    elif not is_tv and r0.json()['movie_results'] != []:
        result = r0.json()['movie_results'][0]
        if 'backdrop_path' in result and result['backdrop_path']:
            return result['backdrop_path']
    # 其它
    else:
        return ''
    
    tmdb_id = result['show_id'] if 'show_id' in result else result['id']
    if is_tv:
        if PROXY:
            r1 = requests.get('https://api.themoviedb.org/3/tv/{}/images?api_key={}'.format(tmdb_id,TMDB_API_KEY), proxies={'http': PROXY_URL, 'https': PROXY_URL})
        else:
            r1 = requests.get('https://api.themoviedb.org/3/tv/{}/images?api_key={}'.format(tmdb_id,TMDB_API_KEY))
    else:
        if PROXY:
            r1 = requests.get('https://api.themoviedb.org/3/movie/{}/images?api_key={}'.format(tmdb_id,TMDB_API_KEY), proxies={'http': PROXY_URL, 'https': PROXY_URL})
        else:
            r1 = requests.get('https://api.themoviedb.org/3/movie/{}/images?api_key={}'.format(tmdb_id,TMDB_API_KEY))
    
    if r1.json()['backdrops'] != []:
        return 'https://www.themoviedb.org/t/p/original/' + sorted(r1.json()['backdrops'], key=lambda x: x['height']* x['width'])[-1]['file_path']
    return ''


@retry(stop_max_attempt_number=3, wait_fixed=2000)
def get_desc_html(subject_id):
    r = requests.get('https://ptgen.rhilip.info/?url=https://douban.com/movie/{}'.format(subject_id), headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'})
    imdb_id = r.json()['imdb_id'] if 'imdb_id' in r.json() else ''
    return r.text, imdb_id


@retry(stop_max_attempt_number=3, wait_fixed=2000)
def get_db_info(subject_id):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Ailurus/68.0'}
    url = 'https://douban.8610000.xyz/data/{}.json'.format(subject_id)
    r = requests.get(url, headers=headers)
    r.encoding = 'utf-8'
    info_json = json.loads(r.text)
    desc_html, imdb_id = get_desc_html(subject_id)
    fanart = get_fanart(imdb_id,info_json['is_tv'])
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
        'desc_html': desc_html
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
