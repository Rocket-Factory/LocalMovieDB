import re
import os
import time
from database import DBSession, Movie, Tag, MovieTag, MovieDirector, MovieActor, Role, Config
from douban import get_movie
from push import run as push_run
import logging
import requests

realpath = os.path.split(os.path.realpath(__file__))[0]
logging.basicConfig(level=logging.INFO)


try:
    session = DBSession()
    config = session.query(Config).get(1)
    MOVIE_DIR_RE = config.movie_dir_re
    ROOT_DIR = config.root_dir
    session.close()
except Exception as e:
    exit(0)


# 从数据库删除路径不存在的电影
def remove_movies():
    session = DBSession()
    movies = session.query(Movie).all()
    for movie in movies:
        dirpath = os.path.join(ROOT_DIR,movie.uri[1:])
        if not os.path.exists(dirpath) or os.listdir(dirpath) == []:
            session.query(Movie).filter(Movie.id==movie.id).delete()
            session.query(MovieTag).filter(MovieTag.movie_id==movie.id).delete()
    session.commit()
    session.close()


#遍历路径搜索视频文件 
def search_video_files(path, files):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):   
            if file.split('.')[-1] in ['mp4', 'mkv', 'ts','flv']:
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
            if video_files_str!='' and (re_result.group(1), re_result.group(2), os.path.join(path, file), video_files_str) not in movies:
                movies.append((re_result.group(1), re_result.group(2), os.path.join(path, file), video_files_str))
        search_movie(os.path.join(path, file), movies)


# 数据库中是否存在
def movie_exists(movie):
    session = DBSession()
    target_movie = session.query(Movie).filter_by(
        **{'title': movie[0], 'year': movie[1], 'uri': movie[2][len(ROOT_DIR):], 'viedo_files': movie[3]}).first()
    session.close()
    if target_movie:
        return True
    return False


# 更新电影信息或插入到数据库
def update_or_insert(info):
    session = DBSession()
    target_movie = session.query(Movie).filter_by(**{'title': info['basic']['title'], 'year': info['basic']['year']}) \
        .first()
    if target_movie:
        target_movie.uri = info['basic']['uri']
        target_movie.update_date = info['basic']['update_date']
        target_movie.viedo_files = info['basic']['viedo_files']

    else:
        new_movie = Movie(**info['basic'])
        session.add(new_movie)
        # 推送新电影信息
        session.flush()
        push_run(info,new_movie.id)

        # 更新Tag
        for tag in info['tags']:
            if session.query(Tag).filter(Tag.text == tag).count() > 0:
                tar_tag = session.query(Tag).filter(Tag.text == tag).first()
            else:
                tar_tag = Tag(tag)
                session.add(tar_tag)
                session.flush()
            new_movie_tag = MovieTag(new_movie.id, tar_tag.id)
            session.add(new_movie_tag)
        
        # 更新导演信息
        for director in info['directors']:
            if session.query(Role).filter(Role.name == director['name']).count() > 0:
                tar_role = session.query(Role).filter(Role.name == director['name']).first()
            else:
                tar_role = Role(director['name'],director['info'])
                session.add(tar_role)
                session.flush()
            new_movie_director = MovieDirector(new_movie.id, tar_role.id)
            session.add(new_movie_director)

        # 更新演员信息
        for actor in info['actors']:
            if session.query(Role).filter(Role.name == actor['name']).count() > 0:
                tar_role = session.query(Role).filter(Role.name == actor['name']).first()
            else:
                tar_role = Role(actor['name'],actor['info'])
                session.add(tar_role)
                session.flush()
            new_movie_director = MovieActor(new_movie.id, tar_role.id)
            session.add(new_movie_director)


    session.commit()
    session.close()


# 获取API简要电影信息(标题、年份、ID等)
def get_q_movie_json():
    url = 'https://douban.8610000.xyz/q.json'
    r = requests.get(url)
    return r.json()


# 脚本入口
def run():
    logging.info('获取API电影数据...')
    q_movies = get_q_movie_json()
    logging.info('已获取，共{}条电影数据'.format(len(q_movies)))
    movies = []
    search_movie(ROOT_DIR, movies)
    for index, movie in enumerate(movies):
        if movie_exists(movie):
            continue
        logging.info('[{}/{}]获取电影: {}'.format(index,len(movies),movie[2]))
        db_info = get_movie(q_movies, movie[0], movie[1])
        if not db_info:
            continue
        db_info['basic']['uri'] =  movie[2][len(ROOT_DIR):]
        db_info['basic']['viedo_files'] =  movie[3]
        db_info['basic']['title'] = movie[0]
        update_or_insert(db_info)
        time.sleep(1)
    # 删除已不存在的电影数据
    remove_movies()


if __name__ =='__main__':
    run()