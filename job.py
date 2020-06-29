import re
import os
import time
from database import DBSession, Movie, Tag, MovieTag
from config import MOVIE_DIR_RE, ROOT_DIR
from douban import get_db_id2, get_db_info, login

realpath = os.path.split(os.path.realpath(__file__))[0]

MOVIES = []

FAILED_MOVIES = []


def writeErrorLog():
    with open(os.path.join(realpath, 'error.log'), 'w') as f:
        for movie in FAILED_MOVIES:
            f.write(movie[0] + movie[1] + ': ' + movie[2] + '\n')


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
    target_movie = session.query(Movie).filter_by(**{'title': info['basic']['title'], 'year': info['basic']['year']}) \
        .first()
    if target_movie:
        target_movie.uri = info['basic']['uri']
        target_movie.update_date = info['basic']['update_date']

    else:
        new_movie = Movie(**info['basic'])
        session.add(new_movie)

        for tag in info['tags']:
            if session.query(Tag).filter(Tag.text == tag).count() > 0:
                tar_tag = session.query(Tag).filter(Tag.text == tag).first()
            else:
                tar_tag = Tag(tag)
                session.add(tar_tag)
                session.flush()
            new_movie_tag = MovieTag(new_movie.id, tar_tag.id)
            session.add(new_movie_tag)

    session.commit()
    session.close()


def run():
    search(ROOT_DIR)
    s = login()
    if s:
        print('豆瓣登录成功\n')
    else:
        print('豆瓣登录失败，正在退出...\n')
    for index, movie in enumerate(MOVIES):
        if movie_exists(movie):
            continue
        print(movie[2])
        time.sleep(1)

        db_id = get_db_id2(s, movie[0], movie[1])
        if not db_id:
            print('获取豆瓣Subject ID错误')
            FAILED_MOVIES.append(movie)
            continue
        db_info = get_db_info(s, db_id, movie[2][len(ROOT_DIR):])
        if not db_info:
            print('获取豆瓣Subject信息错误')
            FAILED_MOVIES.append(movie)
            continue
        update_or_insert(db_info)


run()
