from flask import Flask, render_template, request, jsonify
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import func
from database import Movie, Tag, MovieTag, DBSession
from sqlalchemy import text
from datetime import timedelta
from config import PLAY_URI, USERS, SECRET_KEY, COMMENTS_ON
import logging
import requests
import json

app = Flask(__name__, static_url_path='',
            static_folder='static')

logging.basicConfig(level=logging.DEBUG)


# JWT
class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id


users = [User(*user) for user in USERS]
username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}


def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)


app.config['SECRET_KEY'] = SECRET_KEY
app.config['JWT_AUTH_URL_RULE'] = '/api/auth'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=3000000)
jwt = JWT(app, authenticate, identity)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/movies/random')
@jwt_required()
def get_random_movie():
    session = DBSession()
    movie = session.query(Movie).order_by(func.random()).limit(1)[1]
    return jsonify(movie.to_json())

@app.route('/api/movie/<int:mid>/comments', methods=['POST'])
@jwt_required()
def add_comments(mid):
    params = request.json
    if 'tg_post' in params:
        session = DBSession()
        movie = session.query(Movie).get(mid)
        movie.tg_post = params['tg_post']
        session.commit()
        session.close()
        return jsonify({'code':200, 'msg': 'success'}),200
    return jsonify({'code':400, 'msg': 'wrong request'}), 400


@app.route('/api/movie/<int:mid>')
@jwt_required()
def get_movie_api(mid):
    session = DBSession()
    query = session.query(Movie)
    movie = query.get(mid)
    dbid = movie.douban_url.split('/')[-2]
    
    movie_json = movie.to_json()
    movie_json['play_links'] = [
        PLAY_URI + video_file for video_file in movie_json['viedo_files'].split(',')]

    if COMMENTS_ON:
        movie_json['comments_on'] = True

    return jsonify(movie_json)


@app.route('/api/movies')
@jwt_required()
def get_movies():
    page = 1
    limit = 10
    order_by = '-update_date'
    args = request.args.to_dict()
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
        print(args['type'])
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
        movie_json = movie.to_json()
        movie_tags = session.query(Tag).join(MovieTag, MovieTag.tag_id == Tag.id).filter(
            MovieTag.movie_id == movie_json['id']).all()

        movie_json['tags'] = [tag_.text for tag_ in movie_tags]
        result.append(movie_json)

    return jsonify(result)


@app.route('/api/tags/top')
@jwt_required()
def get_tags():
    page = 1
    limit = 15
    args = request.args.to_dict()
    if 'page' in args:
        page = int(args['page'])
        args.pop('page')
    if 'limit' in args:
        limit = int(args['limit'])
        args.pop('limit')

    session = DBSession()
    tags = session.query(Tag.text, func.count(Tag.text)).join(MovieTag, Tag.id == MovieTag.tag_id).group_by(
        Tag.text).order_by(func.count(Tag.text).desc()).slice((page - 1) * limit, page * limit).all()

    return jsonify(tags)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
