from flask import Flask, render_template, request, jsonify, redirect,url_for,Response
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from werkzeug.security import safe_str_cmp
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import func
from database import Movie, Tag, MovieTag, MovieActor, MovieDirector, Role, Config, DBSession
from sqlalchemy import text
from datetime import timedelta
from functools import wraps
import logging
import requests
import json
import os
import psutil


app = Flask(__name__, static_url_path='',
            static_folder='static')

logging.basicConfig(level=logging.DEBUG)


app.config["JWT_SECRET_KEY"] = os.environ['SECRET_KEY'] 
USER = os.environ['USER'] 
PASSWORD = os.environ['PASSWORD'] 
jwt = JWTManager(app)


def check_auth(username, password):
    if username == USER and password == PASSWORD:
        return True

    return False


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'})


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/api/auth", methods=["POST"])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    session = DBSession()
    config = session.query(Config).get(1)
    if username != config.user.split(':')[0] or password != config.user.split(':')[1]:
        return jsonify({"msg": "Bad username or password"}), 401
    session.close()
    expires = timedelta(days=365)
    access_token = create_access_token(identity=username, expires_delta=expires)
    return jsonify(access_token=access_token)


@app.route('/api/movies/random')
@jwt_required()
def get_random_movie():
    session = DBSession()
    movie = session.query(Movie).order_by(func.random()).limit(1)[1]
    return jsonify(movie.to_json())


@app.route('/api/movie/<int:mid>')
@jwt_required()
def get_movie_api(mid):
    session = DBSession()
    query = session.query(Movie)
    movie = query.get(mid)
    movie_json = movie.to_json()

    tags = session.query(Tag).join(MovieTag, MovieTag.tag_id==Tag.id).filter(MovieTag.movie_id==mid)
    movie_json['tags'] = [tag.to_json() for tag in tags]
    
    actors = session.query(Role).join(MovieActor, MovieActor.actor_id==Role.id).filter(MovieActor.movie_id==mid)
    movie_json['actors_json'] = [json.loads(actor.info) for actor in actors]

    directors = session.query(Role).join(MovieDirector, MovieDirector.director_id==Role.id).filter(MovieDirector.movie_id==mid)
    movie_json['directors_json'] = [json.loads(director.info) for director in directors]

    movie_json['play_links'] = ['/' + video_file for video_file in movie_json['viedo_files'].split(',/')]
    movie_json['user'] = USER
    movie_json['password'] = PASSWORD
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


@app.route('/api/role/<int:rid>')
@jwt_required()
def get_role_info(rid):
    session = DBSession()
    role = session.query(Role).get(rid)
    role_json = json.loads(role.info)
    actor_movies = session.query(Movie).join(MovieActor,Movie.id==MovieActor.movie_id).filter(MovieActor.actor_id==rid)
    movies_json = [movie.to_json() for movie in actor_movies]
    director_movies = session.query(Movie).join(MovieDirector,Movie.id==MovieDirector.movie_id).filter(MovieDirector.director_id==rid)
    for movie in director_movies:
        movies_json.append(movie.to_json())
    role_json['related_movies'] = movies_json
    return jsonify(role_json)


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


@app.route('/api/job')
@requires_auth
def run_job():
    for p in psutil.process_iter():
        if len(p.cmdline()) >1 and p.cmdline()[1]== 'job.py':
            return 'Already started', 200
    os.popen('python3 job.py')
    return 'running',200


def init():
    session = DBSession()
    if session.query(Config).filter().count() == 0:
        user = USER +':'+ PASSWORD
        movie_dir_re = os.environ['MOVIE_DIR_RE']
        tg_push_on = True if os.environ['TG_ON']=='true' else False
        tg_chatid = os.environ['TG_CHATID']
        tg_bot_token = os.environ['TG_BOT_TOKEN']
        bark_push_on = True if os.environ['BARK_ON']=='true' else False
        bark_tokens = os.environ['BARK_TOKENS']
        server_cyann_on = True if os.environ['SERVER_CYANN']=='true' else False
        server_cyann_token = os.environ['SERVER_CYANN_TOKEN']
        proxy_on = True if os.environ['PROXY_ON']=='true' else False
        proxy_url = os.environ['PROXY_URL']
        config = Config(user=user,root_dir='/mnt/media',movie_dir_re=movie_dir_re ,tg_push_on=tg_push_on,tg_chatid=tg_chatid,tg_bot_token=tg_bot_token,bark_push_on=bark_push_on,bark_tokens=bark_tokens,server_cyann_on=server_cyann_on,server_cyann_token=server_cyann_token,proxy_on=proxy_on,proxy_url=proxy_url)
        session.add(config)
        session.commit()
        session.close()


if __name__ == '__main__':
    init()
    app.run(host='0.0.0.0', port=5006)
