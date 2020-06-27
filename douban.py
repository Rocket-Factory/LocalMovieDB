# coding: utf-8
import json
import re
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup

from config import DB_API_KEY

def get_db_id2(name,year):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:74.0) Gecko/20100101 Firefox/74.0'}
    url = 'https://movie.douban.com/j/subject_suggest?q={}'.format(name)
    for i in range(0,5):
        try:
            r = requests.get(url,headers=headers)
            r.encoding = 'utf-8'
            info_json = json.loads(r.text)
            for movie_info in info_json:
                if movie_info['title'] == name and movie_info['year'] == year:
                    return movie_info['id']
        except Exception:
            print('第{}次获取ID错误'.format(i))
    return None

def get_db_id(name, year):
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:74.0) Gecko/20100101 Firefox/74.0'}
    url = 'https://www.douban.com/search?cat=1002&q={}'.format(name)
    try:
        r = requests.get(url, headers=headers)
        html = r.text
        soup = BeautifulSoup(html, features="html.parser")
        results = soup.find('div', class_='result-list').find_all('div', class_='result')
    except AttributeError:
        time.sleep(3)
        r = requests.get(url, headers=headers)
        html = r.text
        soup = BeautifulSoup(html, features="html.parser")
        results = soup.find('div', class_='result-list').find_all('div', class_='result')

    for subject in results:
        subject_cast = subject.find('span', class_='subject-cast')
        subject_year = re.search('/ (\d{4})', subject_cast.text).group(1).strip()
        subject_name = subject.find('div', class_='title').h3.a.text.strip()

        if subject_name == name and subject_year == year:
            subject_url = subject.find('div', class_='title').h3.a.attrs['href']
            return re.search('%2Fsubject%2F(\d+)%2F', subject_url).group(1)

    return None


def get_db_info(subject_id, uri):
    url = 'https://api.douban.com/v2/movie/subject/{}?apikey={}'.format(subject_id, DB_API_KEY)
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:74.0) Gecko/20100101 Firefox/74.0'}
    for i in range(0,5):
        try:
            r = requests.get(url, headers=headers)
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

