# coding: utf-8
import os

from sqlalchemy import Column, INTEGER, TEXT, DATETIME, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import StaticPool

realpath = os.path.split(os.path.realpath(__file__))[0]
sql_path = os.path.join(realpath,'movies.db')
engine = create_engine('sqlite:///{}'.format(sql_path),
                       connect_args={'check_same_thread': False},
                       poolclass=StaticPool,
                       echo=False)
DBSession = sessionmaker(bind=engine)
Base = declarative_base()


class Movie(Base):
    __tablename__ = 'movie'

    id = Column(INTEGER, primary_key=True)
    type = Column(TEXT)  # 类型
    title = Column(TEXT)  # 标题
    original_title = Column(TEXT)  # 原标题
    year = Column(INTEGER)  # 年份
    update_date = Column(DATETIME)  # 更新日期
    uri = Column(TEXT)  # 资源路径
    douban_url = Column(TEXT)  # 豆瓣链接
    thumbnail_url = Column(TEXT)  # 缩略图
    douban_rating = Column(TEXT)  # 豆瓣评分
    intro = Column(TEXT) #简介
    viedo_files =  Column(TEXT)

    def __init__(self, title, _type, original_title, year, update_date, uri, douban_url, thumbnail_url,
                 douban_rating, intro, viedo_files):
        self.title = title
        self.type = _type
        self.original_title = original_title
        self.year = year
        self.update_date = update_date
        self.uri = uri
        self.douban_url = douban_url
        self.thumbnail_url = thumbnail_url
        self.douban_rating = douban_rating
        self.intro = intro
        self.viedo_files = viedo_files

    def __repr__(self):
        full_title = '{} {} （{}）'.format(self.title, self.type, self.original_title,
                                         self.year) if self.title != self.original_title \
            else '{} （{}）'.format(self.title, self.year)

        return 'Movie:{}'.format(full_title)

    def fullname(self):
        return '{} {} （{}）'.format(self.title, self.type, self.original_title,
                                   self.year) if self.title != self.original_title \
            else '{} （{}）'.format(self.title, self.year)

    def to_json(self):
        if hasattr(self, '__table__'):
            _json = {}
            for i in self.__table__.columns:
                if i.name == 'update_date':
                    _json[i.name] = str(getattr(self, i.name))[:10]
                    continue
                _json[i.name] = getattr(self, i.name)
            return _json
        raise AssertionError('<%r> does not have attribute for __table__' % self)


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
        raise AssertionError('<%r> does not have attribute for __table__' % self)


Base.metadata.create_all(engine)
