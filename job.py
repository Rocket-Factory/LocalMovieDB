import re
import os
import time
from database import DBSession, Movie, Tag, MovieTag
from config import MOVIE_DIR_RE, ROOT_DIR
from douban import get_movie
import logging
realpath = os.path.split(os.path.realpath(__file__))[0]

logging.basicConfig(level=logging.INFO)


#遍历路径搜索视频文件 
def search_video_files(path, files):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):   
            if file.split('.')[-1] in ['mp4', 'mkv', 'ts']:
                files.append(os.path.join(path, file))
            continue
        search_video_files(os.path.join(path, file),files)
        
        

# 遍历路径搜索电影
def search_movie(path, movies):
    for file in os.listdir(path):
        if not os.path.isdir(os.path.join(path, file)):
            continue
        re_result = re.match(MOVIE_DIR_RE, file)
        if re_result:
            video_files = []
            search_video_files(os.path.join(path, file), video_files)
            video_files.sort()
            video_files = [video_file[len(ROOT_DIR):] for video_file in video_files]
            video_files_str = ','.join(video_files)
            logging.debug('找到视频文件: {}'.format(video_files_str))
            if (re_result.group(1), re_result.group(2), os.path.join(path, file), video_files_str) not in movies:
                movies.append((re_result.group(1), re_result.group(2), os.path.join(path, file), video_files_str))
        search_movie(os.path.join(path, file), movies)


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
    movies = []
    search_movie(ROOT_DIR, movies)
    for index, movie in enumerate(movies):
        if movie_exists(movie):
            continue
        logging.info('[{}/{}]获取电影: {}'.format(index,len(movies),movie[2]))
        db_info = get_movie(movie[0], movie[1] )
        if not db_info:
            continue
        db_info['basic']['uri'] =  movie[2][len(ROOT_DIR):]
        db_info['basic']['viedo_files'] =  movie[3]
        update_or_insert(db_info)
        time.sleep(1)


if __name__ =='__main__':
    run()