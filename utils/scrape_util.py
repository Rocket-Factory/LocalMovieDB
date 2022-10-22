import os
import time
import requests
import json
from datetime import datetime

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Ailurus/68.0'}

DOUBAN_MOVIE_JSON_API = 'https://moviedb.8610000.xyz'
Q_FILE_PATH = './data/q.cache'


def q_file_exists():
    return os.path.exists(Q_FILE_PATH)


def q_file_expired():
    filemt = time.mktime(time.localtime(os.stat(Q_FILE_PATH).st_mtime))
    return time.time() - filemt > 18000


def download_q_file():
    r = requests.get(DOUBAN_MOVIE_JSON_API + '/q.json', headers=HEADERS)
    with open(Q_FILE_PATH, 'w') as f:
        f.write(r.text)


def read_q_file():
    with open(Q_FILE_PATH) as f:
        text = f.read()
    return json.loads(text)


def get_movie_info(mid):
    url = DOUBAN_MOVIE_JSON_API + '/data/{}.json'.format(mid)
    r = requests.get(url, headers=HEADERS)
    r.encoding = 'utf-8'
    info_json = json.loads(r.text)
    fanart = ''
    if 'extra' in info_json and 'backdrops' in info_json['extra']:
        try:
            fanart = info_json['extra']['backdrops'][0]
        except Exception:
            fanart = ''
    recommendations = get_movie_recommendations(mid)
    tags = []
    for tag in info_json['tags']:
        tags.append(tag['name'])
    
    if 'card_subtitle' in info_json:
        for tag in info_json['card_subtitle'].replace(' / ',' ').split(' '):
            if tag not in tags:
                tags.append(tag)
    return {
        'mid':mid,
        'title': info_json['title'],
        '_type': '剧集' if info_json['is_tv'] else '电影',
        'original_title': info_json['original_title'],
        'year': int(info_json['year']),
        'intro': info_json['intro'],
        'trailer': info_json['trailer']['video_url'] if info_json['trailer'] else '',
        'fanart': fanart,
        'update_date': datetime.now(),
        'douban_url': 'https://m.douban.com/movie/subject/{}/'.format(mid),
        'thumbnail_url': info_json['pic']['large'],
        'douban_rating': info_json['rating']['value'] if info_json['rating'] else -1,
        'desc_html': '',
        'tags': tags,
        'directors': [{'name': director['name'], 'info': json.dumps(director)} for director in info_json['directors']],
        'actors': [{'name': actor['name'], 'info': json.dumps(actor)} for actor in info_json['actors']],
        'recommendations': json.dumps(recommendations),
    }


def get_movie_id(q_movies, title, year):
    mid = None
    for movie in q_movies:
        if (movie['original_title'] == title or ''.join(movie['title'].split()) == ''.join(title.split())) and movie['year'] == year:
            mid = movie['id']
            break
    return mid


def get_movie_recommendations(mid):
    recommendations = []
    url = DOUBAN_MOVIE_JSON_API + '/recommendation/{}.json'.format(mid)
    r = requests.get(url, headers=HEADERS)
    if r.status_code != 404:
        r.encoding = 'utf-8'
        info_json = json.loads(r.text)
        
        for recommend in info_json['recommendations']:
            recommend['id'] = int(recommend['id'])
            recommendations.append(recommend)
            
    return recommendations
    