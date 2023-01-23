import json
import logging
import time
from datetime import datetime

from database import User, Movie, UserMovie, Tag, MovieTag, MovieActor, MovieDirector, Role, Setting, DBSession

from sqlalchemy.exc import NoResultFound
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import func
from sqlalchemy import text
import bcrypt


def get_setting_value(key):
    session = DBSession()
    setting = session.query(Setting).get(key)
    session.close()
    if not setting:
        return None
    return setting.value


def add_setting_pair(key, value):
    session = DBSession()
    new_pair = Setting(key=key, value=value)
    session.add(new_pair)
    session.commit()
    session.close()


def init_database(username, password, root_dir, movie_dir_re, job_interval):
    session = DBSession()
    if session.query(Setting).filter_by(key='inited').count() > 0:
        session.close()
        return False
    session.close()
    add_user(username, password, True)
    add_setting_pair('root_dir', root_dir)
    add_setting_pair('movie_dir_re', movie_dir_re)
    add_setting_pair('job_interval', job_interval)
    add_setting_pair('inited', '1')
    return True


def get_valified_user_or_none(username, passwd):
    session = DBSession()
    target_user = session.query(User).filter_by(
        username=username).one_or_none()
    session.close()
    if not target_user:
        return None
    if target_user.verify_password(passwd):
        return target_user
    return None


def get_user_or_none_by_id(id):
    session = DBSession()
    target_user = session.query(User).filter_by(id=id).one_or_none()
    session.close()
    return target_user


def add_user(username, passwd, admin=False):
    session = DBSession()
    if session.query(User).filter_by(username=username).count() > 0:
        session.close()
        return False
    hashed = bcrypt.hashpw(passwd.encode('utf-8'), bcrypt.gensalt())
    new_user = User(username, hashed, admin)
    session.add(new_user)
    session.commit()
    session.flush()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    return user.to_json()


def get_user_movies_json(user_id):
    session = DBSession()
    user_movies = session.query(UserMovie).filter_by(user_id=user_id)
    movies_json = []
    for user_movie in user_movies:
        if user_movie.watch_status == 0:
            continue
        movie = session.query(Movie).get(user_movie.movie_id)
        movie_json = movie.basic_json()
        movie_json['user_status'] = user_movie.to_json()
        movies_json.append(movie_json)
    session.close()
    return movies_json


def mark_user_movie(user_id, mid, watch_status, comment, rating):
    session = DBSession()
    if session.query(Movie).filter_by(id=mid).count() == 0:
        session.close()
        return None
    if not isinstance(watch_status, int) or not isinstance(rating, int):
        session.close()
        return None
    user_movie = session.query(UserMovie).filter_by(
        user_id=user_id, movie_id=mid).one_or_none()
    if not user_movie:
        new_user_movie = UserMovie(user_id=user_id, movie_id=mid,
                                   watch_status=watch_status, comment=comment, rating=rating)
        session.add(new_user_movie)
        session.flush()
        user_movie_json = new_user_movie.to_json()
        session.commit()
        session.close()
    else:
        user_movie.watch_status = watch_status
        user_movie.comment = comment
        user_movie.rating = rating
        session.flush()
        user_movie_json = user_movie.to_json()
        session.commit()
        session.close()
    return user_movie_json


def get_user_movie_status_json(user_id, mid):
    session = DBSession()
    try:
        user_movie = session.query(UserMovie).filter_by(
            user_id=user_id, movie_id=mid).one()
    except MultipleResultsFound:
        return None
    except NoResultFound:
        return {'watch_status': 0, 'comment': '', 'rating': -1}
    return user_movie.to_json()


def update_or_insert_user_movie(user_id, movie_id, data):
    session = DBSession()
    target = session.query(UserMovie).filter_by(
        user_id=user_id, movie_id=movie_id).one_or_none()
    if not target:
        new_user_movie = UserMovie(user_id, movie_id, **data)
        session.add(new_user_movie)
    else:
        for attr in data:
            target.setattr(attr, data[attr])

    session.commit()
    session.close()


def get_movies_json(args):
    page = 1
    limit = 10
    order_by = '-update_date'
    if 'page' in args:
        page = int(args['page'])
        args.pop('page')
    if 'limit' in args:
        limit = int(args['limit'])
        args.pop('limit')
    if 'order_by' in args:
        order_by = args['order_by']
        args.pop('order_by')
    tags = []
    if 'tags' in args:
        if args['tags'] != '':
            tags = args['tags'].split(',')
        args.pop('tags')
    session = DBSession()
    query = session.query(Movie)

    if 'q' in args:
        query = query.filter(Movie.title.like('%{}%'.format(args['q'])))

    if 'type' in args and args['type'] != '':
        query = query.filter(Movie.type == args['type'])
        args.pop('type')

    if len(tags) > 0:
        alaised_movie_tag = dict()
        alaised_tag = dict()
        for i, tag in enumerate(tags):
            if i > 5:
                break
            alaised_movie_tag[i] = aliased(MovieTag)
            alaised_tag[i] = aliased(Tag)
            query = query.join(alaised_movie_tag[i], Movie.id == alaised_movie_tag[i].movie_id) \
                .join(alaised_tag[i], alaised_movie_tag[i].tag_id == alaised_tag[i].id) \
                .filter(alaised_tag[i].text == tag)

    if order_by == 'update_date':
        query = query.order_by(Movie.update_date.asc())
    elif order_by == '-update_date':
        query = query.order_by(Movie.update_date.desc())
    else:
        query = query.order_by(text(order_by))

    movies = query.slice((page - 1) * limit, page * limit).all()
    result = []
    for movie in movies:
        movie_json = movie.basic_json()
        movie_tags = session.query(Tag).join(MovieTag, MovieTag.tag_id == Tag.id).filter(
            MovieTag.movie_id == movie_json['id']).all()

        movie_json['tags'] = [tag_.text for tag_ in movie_tags]
        result.append(movie_json)

    session.close()
    return result


def get_movie_json_by_id(mid, user_id):
    session = DBSession()
    query = session.query(Movie)
    movie = query.get(mid)
    movie_json = movie.to_json()
    movie_json.pop('recommendations')

    user_movie_json = get_user_movie_status_json(user_id, mid)
    movie_json['user_status'] = user_movie_json

    tags = session.query(Tag).join(
        MovieTag, MovieTag.tag_id == Tag.id).filter(MovieTag.movie_id == mid)
    movie_json['tags'] = [tag.to_json() for tag in tags]

    actors = session.query(Role).join(
        MovieActor, MovieActor.actor_id == Role.id).filter(MovieActor.movie_id == mid)
    movie_json['actors_json'] = [json.loads(actor.info) for actor in actors]

    directors = session.query(Role).join(
        MovieDirector, MovieDirector.director_id == Role.id).filter(MovieDirector.movie_id == mid)
    movie_json['directors_json'] = [json.loads(
        director.info) for director in directors]

    session.close()
    return movie_json


def get_movie_recommendations_json_by_id(mid):
    session = DBSession()
    query = session.query(Movie)
    movie = query.get(mid)
    movie_json = movie.to_json()
    recommendations = []
    for movie in json.loads(movie_json['recommendations']):
        if session.query(Movie).filter(Movie.mid == movie['id']).count() > 0:
            movie['id'] = session.query(Movie).filter(
                Movie.mid == movie['id']).first().id
            recommendations.append(movie)
    session.close()
    return recommendations


def get_movie_video_files_by_douban_id(douban_id):
    session = DBSession()
    target_movie = session.query(Movie).filter(Movie.mid == douban_id).first()
    video_files_str = ''
    if target_movie:
        video_files_str = target_movie.video_files
    session.close()
    return video_files_str


def get_movie_id_by_douban_id(douban_id):
    session = DBSession()
    target_movie = session.query(Movie).filter(Movie.mid == douban_id).first()
    movie_id_info = {}
    if target_movie:
        movie_id_info = {'id': target_movie.id}
    session.close()
    return movie_id_info


def get_top_tags(args):
    page = 1
    limit = 20
    if 'page' in args:
        page = int(args['page'])
        args.pop('page')
    if 'limit' in args:
        limit = int(args['limit'])
        args.pop('limit')

    session = DBSession()
    tags = session.query(Tag.text, func.count(Tag.text)).join(MovieTag, Tag.id == MovieTag.tag_id).group_by(
        Tag.text).order_by(func.count(Tag.text).desc()).slice((page - 1) * limit, page * limit).all()

    tag_list = [[tag[0], tag[1]] for tag in tags]
    session.close()
    return tag_list


def get_role_json_by_id(rid):
    session = DBSession()
    role = session.query(Role).get(rid)
    role_json = json.loads(role.info)
    actor_movies = session.query(Movie).join(
        MovieActor, Movie.id == MovieActor.movie_id).filter(MovieActor.actor_id == rid)
    movies_json = [movie.basic_json() for movie in actor_movies]
    director_movies = session.query(Movie).join(
        MovieDirector, Movie.id == MovieDirector.movie_id).filter(MovieDirector.director_id == rid)
    for movie in director_movies:
        movies_json.append(movie.basic_json())
    role_json['related_movies'] = movies_json

    session.close()
    return role_json


def update_or_insert_movie(info):
    session = DBSession()
    target_movie = session.query(Movie).filter_by(**{'title': info['title'], 'year': info['year']}) \
        .first()
    
    if target_movie:
        # 跳过文件和评分无变化的
        if target_movie.video_files == info['video_files'] and  target_movie.douban_rating == str(info['douban_rating']):
            session.close()
            return
        # 删除原数据以便更新
        session.delete(target_movie)
        session.commit()
    session.close()

    session = DBSession()
    basic_info = info.copy()
    basic_info.pop('tags')
    basic_info.pop('directors')
    basic_info.pop('actors')
    new_movie = Movie(**basic_info)
    session.add(new_movie)
    session.flush()

    for tag in info['tags']:
        if session.query(Tag).filter(Tag.text == tag).count() > 0:
            tar_tag = session.query(Tag).filter(Tag.text == tag).first()
        else:
            tar_tag = Tag(tag)
            session.add(tar_tag)
            session.flush()
        new_movie_tag = MovieTag(new_movie.id, tar_tag.id)
        session.add(new_movie_tag)
        session.flush()

    for director in info['directors']:
        director_info = json.loads(director['info'])
        if 'id' in director_info and session.query(Role).filter(Role.rid == director_info['id']).count() > 0:
            tar_role = session.query(Role).filter(
                Role.rid == director_info['id']).first()
        elif session.query(Role).filter(Role.name == director['name']).count() > 0:
            tar_role = session.query(Role).filter(
                Role.name == director['name']).first()
        else:
            if 'id' in director['info']:
                tar_role = Role(
                    director_info['id'], director['name'], director['info'])
            else:
                tar_role = Role(
                    str(-datetime.timestamp(datetime.now())), director['name'], director['info'])
                time.sleep(1)
            session.add(tar_role)
            session.flush()
        new_movie_director = MovieDirector(new_movie.id, tar_role.id)
        session.add(new_movie_director)

    for actor in info['actors']:
        actor_info = json.loads(actor['info'])
        if 'id' in actor_info and session.query(Role).filter(Role.rid == actor_info['id']).count() > 0:
            tar_role = session.query(Role).filter(
                Role.rid == actor_info['id']).first()
        elif session.query(Role).filter(Role.name == actor['name']).count() > 0:
            tar_role = session.query(Role).filter(
                Role.name == actor['name']).first()
        else:
            if 'id' in actor['info']:
                tar_role = Role(
                    actor_info['id'], actor['name'], actor['info'])
            else:
                tar_role = Role(
                    str(-datetime.timestamp(datetime.now())), actor['name'], actor['info'])
                time.sleep(1)
            session.add(tar_role)
            session.flush()
        new_movie_director = MovieActor(new_movie.id, tar_role.id)
        session.add(new_movie_director)

    session.commit()
    session.close()


def movie_exists(year, uri, video_files_str):
    session = DBSession()
    target_movie = session.query(Movie).filter_by(
        **{'year': year, 'uri': uri, 'video_files': video_files_str}).first()
    session.close()
    if target_movie and target_movie.douban_rating != '-1':
        return True
    return False


def remove_deleted_movies(path_list):
    session = DBSession()
    for movie in session.query(Movie):
        if movie.uri not in path_list:
            session.delete(movie)
            session.commit()

    session.close()
