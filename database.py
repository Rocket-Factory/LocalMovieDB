# coding: utf-8
import os

import bcrypt
from sqlalchemy import Column, INTEGER, TEXT, DATETIME, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import StaticPool
from sqlalchemy.sql.sqltypes import Boolean


realpath = os.path.split(os.path.realpath(__file__))[0]
sql_path = os.path.join(realpath, './data/movies.db')
engine = create_engine('sqlite:///{}'.format(sql_path),
                       connect_args={'check_same_thread': False},
                       poolclass=StaticPool,
                       echo=False)
DBSession = sessionmaker(bind=engine)
Base = declarative_base()


class Setting(Base):
    __tablename__ = 'setting'
    key = Column(TEXT, primary_key=True)
    value = Column(TEXT)

    """
    root_dir
    job_interval
    movie_dir_re
    inited
    """

    def __init__(self, key, value):
        self.key = key
        self.value = value


class User(Base):
    __tablename__ = 'user'

    id = Column(INTEGER, primary_key=True)
    username = Column(TEXT)
    passwd = Column(TEXT)
    admin = Column(Boolean)

    def __init__(self, username, passwd, admin=False):
        self.username = username
        self.passwd = passwd
        self.admin = admin

    def verify_password(self, password):
        pwhash = bcrypt.hashpw(password.encode('utf-8'), self.passwd)
        return self.passwd == pwhash

    def to_json(self):
        return {'username': self.username, 'admin': self.admin}


class UserMovie(Base):
    __tablename__ = 'user_movie'

    id = Column(INTEGER, primary_key=True)
    user_id = Column(INTEGER)
    movie_id = Column(INTEGER)
    watch_status = Column(INTEGER)  # 0:None 1:Towatch 2: Watched
    comment = Column(TEXT)
    rating = Column(INTEGER)  # -1:No rating

    def __init__(self, user_id, movie_id, watch_status=0, comment='', rating=-1):
        self.user_id = user_id
        self.movie_id = movie_id
        self.watch_status = watch_status
        self.comment = comment
        self.rating = rating

    def to_json(self):
        if hasattr(self, '__table__'):
            _json = {}
            for i in self.__table__.columns:
                if i.name == 'id' or i.name == 'user_id' or i.name == 'movie_id':
                    continue
                _json[i.name] = getattr(self, i.name)
            return _json
        raise AssertionError(
            '<%r> does not have attribute for __table__' % self)


class Movie(Base):
    __tablename__ = 'movie'

    id = Column(INTEGER, primary_key=True)
    mid = Column(TEXT)
    type = Column(TEXT)
    title = Column(TEXT)
    original_title = Column(TEXT)
    year = Column(INTEGER)
    update_date = Column(DATETIME)
    fanart = Column(TEXT)
    trailer = Column(TEXT)
    uri = Column(TEXT)
    douban_url = Column(TEXT)
    thumbnail_url = Column(TEXT)
    douban_rating = Column(TEXT)
    intro = Column(TEXT)
    video_files = Column(TEXT)
    desc_html = Column(TEXT)
    recommendations = Column(TEXT)

    def __init__(self, mid, title, _type, original_title, year, update_date, trailer, fanart, uri, douban_url, thumbnail_url,
                 douban_rating, intro, video_files, desc_html, recommendations):
        self.mid = mid
        self.title = title
        self.type = _type
        self.original_title = original_title
        self.year = year
        self.update_date = update_date
        self.trailer = trailer
        self.fanart = fanart
        self.uri = uri
        self.douban_url = douban_url
        self.thumbnail_url = thumbnail_url
        self.douban_rating = douban_rating
        self.intro = intro
        self.video_files = video_files
        self.desc_html = desc_html
        self.recommendations = recommendations

    def __repr__(self):
        full_title = '{} {} （{}）'.format(self.title, self.type, self.original_title,
                                         self.year) if self.title != self.original_title \
            else '{} （{}）'.format(self.title, self.year)

        return 'Movie:{}'.format(full_title)

    def to_json(self):
        if hasattr(self, '__table__'):
            _json = {}
            for i in self.__table__.columns:
                if i.name == 'update_date':
                    _json[i.name] = str(getattr(self, i.name))[:10]
                    continue
                _json[i.name] = getattr(self, i.name)
            return _json
        raise AssertionError(
            '<%r> does not have attribute for __table__' % self)

    def basic_json(self):
        if hasattr(self, '__table__'):
            _json = {}
            for i in self.__table__.columns:
                if i.name not in ['id', 'mid', 'title', 'type', 'original_title', 'year', 'update_date', 'thumbnail_url', 'douban_rating', 'intro']:
                    continue
                if i.name == 'update_date':
                    _json[i.name] = str(getattr(self, i.name))[:10]
                    continue
                _json[i.name] = getattr(self, i.name)
            return _json
        raise AssertionError(
            '<%r> does not have attribute for __table__' % self)


class MovieTag(Base):
    __tablename__ = 'movie_tag'

    id = Column(INTEGER, primary_key=True)
    movie_id = Column(INTEGER)
    tag_id = Column(INTEGER)

    def __init__(self, movie_id, tag_id):
        self.movie_id = movie_id
        self.tag_id = tag_id


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(INTEGER, primary_key=True)
    text = Column(TEXT)

    def __init__(self, text):
        self.text = text

    def to_json(self):
        if hasattr(self, '__table__'):
            _json = {}
            for i in self.__table__.columns:
                _json[i.name] = getattr(self, i.name)
            return _json
        raise AssertionError(
            '<%r> does not have attribute for __table__' % self)


class MovieActor(Base):
    __tablename__ = 'movie_actor'
    id = Column(INTEGER, primary_key=True)
    movie_id = Column(INTEGER)
    actor_id = Column(INTEGER)

    def __init__(self, movie_id, actor_id):
        self.movie_id = movie_id
        self.actor_id = actor_id


class MovieDirector(Base):
    __tablename__ = 'movie_director'
    id = Column(INTEGER, primary_key=True)
    movie_id = Column(INTEGER)
    director_id = Column(INTEGER)

    def __init__(self, movie_id, director_id):
        self.movie_id = movie_id
        self.director_id = director_id


class Role(Base):
    __tablename__ = 'role'
    id = Column(INTEGER, primary_key=True)
    rid = Column(TEXT)
    name = Column(TEXT)
    info = Column(TEXT)

    def __init__(self, rid, name, info):
        self.rid = rid
        self.info = info
        self.name = name

    def to_json(self):
        if hasattr(self, '__table__'):
            _json = {}
            for i in self.__table__.columns:
                _json[i.name] = getattr(self, i.name)
            return _json
        raise AssertionError(
            '<%r> does not have attribute for __table__' % self)


Base.metadata.create_all(engine)
