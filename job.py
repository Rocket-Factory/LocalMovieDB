import re
import os
import time
from database import DBSession, Movie, Tag, MovieTag
from config import MOVIE_DIR_RE, ROOT_DIR
from douban import get_db_id, get_db_info

realpath = os.path.split(os.path.realpath(__file__))[0]


MOVIES = []

FAILED_MOVIES = []


def writeErrorLog():
    with open( os.path.join(realpath,'error.log'),'w') as f:
        for movie in FAILED_MOVIES:
            f.write(movie[0] + movie[1]+ ': ' + movie[2] + '\n')


def search(path):
    for file in os.listdir(path):
        if not os.path.isdir(os.path.join(path, file)):
            continue

        re_result = re.match(MOVIE_DIR_RE, file)
        if re_result and (re_result.group(1), re_result.group(2)) not in MOVIES:
            MOVIES.append((re_result.group(1), re_result.group(2), os.path.join(path, file)))
            continue
        search(os.path.join(path, file))


def movie_exists(movie):
    session = DBSession()
    target_movie = session.query(Movie).filter_by(
        **{'title': movie[0], 'year': movie[1], 'uri': movie[2][len(ROOT_DIR):]}).first()
    session.close()
    if target_movie:
        return True
    return False


def update_or_insert(info):
    session = DBSession()
    target_movie = session.query(Movie).filter_by(**{'title': info['basic']['title'], 'year': info['basic']['year']})\
        .first()
    if target_movie:
        target_movie.uri = info['basic']['uri']
        target_movie.update_date = info['basic']['update_date']

    else:
        new_movie = Movie(**info['basic'])
        session.add(new_movie)

        for tag in info['tags']:
            new_tag = Tag(tag)
            session.add(new_tag)
            session.flush()
            new_movie_tag = MovieTag(new_movie.id, new_tag.id)
            session.add(new_movie_tag)

    session.commit()
    session.close()


def run():
    search(ROOT_DIR)
    timeout = 0
    for index, movie in enumerate(MOVIES):
        if movie_exists(movie):
            continue
        print(movie[2])
        if timeout < 60:
            time.sleep(timeout + 2 * index)
        db_id = get_db_id(movie[0], movie[1])
        if not db_id:
            print('获取豆瓣Subject ID错误')
            FAILED_MOVIES.append(movie)
            continue
        db_info = get_db_info(db_id, movie[2][len(ROOT_DIR):])
        if not db_info:
            print('获取豆瓣Subject信息错误')
            FAILED_MOVIES.append(movie)
            continue
        update_or_insert(db_info)




run()
