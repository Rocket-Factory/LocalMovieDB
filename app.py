from flask import Flask, render_template, request, jsonify, redirect
from flask_jwt_extended.utils import create_access_token, current_user
from flask_jwt_extended.view_decorators import jwt_required
from flask_jwt_extended.jwt_manager import JWTManager

from utils import sql_util, nginx_util
import job

import logging
import os
import shutil
from threading import Thread


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(threadName)s %(filename)s %(message)s")

ROOT_DIR = '/mnt/media'
MOVIE_DIR_RE = '(.*?)（(\d{4})）'
JOB_INTERVAL = 1800
URL_PREFIX = '/share/'


if not os.path.exists('./data/secret'):
    shutil.copy('./.secret', './data/secret')
if not os.path.exists('./data/secure_password'):
    shutil.copy('./.secure_password', './data/secure_password')


c = job.UpdateTask()


app = Flask(__name__, static_url_path='',
            static_folder='static')


app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 1728000

with open('./data/secret') as f:
    secret_key = f.read()

app.config["JWT_SECRET_KEY"] = secret_key

jwt = JWTManager(app)


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return sql_util.get_user_or_none_by_id(identity)


@app.route("/api/user/login", methods=["POST"])
def login():
    if not request.json:
        return jsonify(status='error', msg='Wrong request'), 400
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    user = sql_util.get_valified_user_or_none(username, password)
    if not user:
        return jsonify(status='error', msg="Wrong username or password"), 401

    access_token = create_access_token(identity=user)
    return jsonify(access_token=access_token)


@app.route('/')
def index():
    if not sql_util.get_setting_value('inited'):
        return redirect('/init_page')
    return render_template('index.html')


@app.route('/init_page')
def init_app_page():
    if sql_util.get_setting_value('inited'):
        return redirect('/')
    return render_template('init.html')


@app.route("/api/user/whoiam", methods=["GET"])
@jwt_required()
def who_i_am():
    return jsonify(
        id=current_user.id,
        username=current_user.username,
        admin=current_user.admin
    )


@app.route("/api/user/new", methods=["POST"])
@jwt_required()
def add_user():
    if not current_user.admin:
        return jsonify(status='error', msg='Not allowed'), 400
    if not request.json:
        return jsonify(status='error', msg='Wrong request'), 400
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    if not username or not password:
        return jsonify(status='error', msg='Wrong request'), 400
    user = sql_util.add_user(username, password)
    if not user:
        return jsonify(status='error', msg='Username exists'), 400
    return jsonify(user)


@app.route("/api/user/movies")
@jwt_required()
def get_user_movies():
    user_id = current_user.id
    movies_json = sql_util.get_user_movies_json(user_id)
    return jsonify(movies_json)


@app.route("/api/user/movie/mark", methods=['POST'])
@jwt_required()
def mark_user_movie():
    if not request.json:
        return jsonify(status='error', msg='Wrong request'), 400
    mid = request.json.get("mid", None)
    watch_status = request.json.get("watch_status", None)
    comment = request.json.get("comment", '')
    rating = request.json.get("rating", -1)
    user_id = current_user.id
    user_movie_json = sql_util.mark_user_movie(
        user_id, mid, watch_status, comment, rating)
    if not user_movie_json:
        return jsonify(status='error', msg='Wrong request'), 400
    return jsonify(user_movie_json)


@app.route('/api/movie/<int:mid>')
@jwt_required()
def get_movie_api(mid):
    user_id = current_user.id
    movie_json = sql_util.get_movie_json_by_id(mid, user_id)
    url_prefix = URL_PREFIX
    secure_passwd = nginx_util.get_secure_passwd()
    movie_json['play_links'] = nginx_util.gen_movie_links(
        url_prefix, secure_passwd, movie_json['video_files'])
    return jsonify(movie_json)


@app.route('/api/movie/<int:mid>/recommendations')
@jwt_required()
def get_movie_recommendations_api(mid):
    recommendations_json = sql_util.get_movie_recommendations_json_by_id(mid)
    return jsonify(recommendations_json)


@app.route('/api/movie/db/<int:douban_id>/videos')
@jwt_required()
def get_db_movie_videos(douban_id):
    video_files_str = sql_util.get_movie_video_files_by_douban_id(
        str(douban_id))
    if video_files_str != '':
        url_prefix = URL_PREFIX
        secure_passwd = nginx_util.get_secure_passwd()
        video_links = nginx_util.gen_movie_links(
            url_prefix, secure_passwd, video_files_str)
        return jsonify(video_links)
    else:
        return jsonify(status='error', msg='Not found'), 404


@app.route('/api/movie/db/<int:douban_id>/id')
@jwt_required()
def get_db_movie_id(douban_id):
    id_info = sql_util.get_movie_id_by_douban_id(douban_id)
    return jsonify(id_info)


@app.route('/api/movies')
@jwt_required()
def get_movies():
    args = request.args.to_dict()
    movies_json = sql_util.get_movies_json(args)
    return jsonify(movies_json)


@app.route('/api/role/<int:rid>')
@jwt_required()
def get_role_info(rid):
    role_json = sql_util.get_role_json_by_id(rid)
    return jsonify(role_json)


@app.route('/api/tags/top')
@jwt_required()
def get_tags():
    args = request.args.to_dict()
    tag_list = sql_util.get_top_tags(args)
    return jsonify(tag_list)


@app.route('/api/app/init', methods=["POST"])
def init():
    if not request.json:
        return jsonify(status='error', msg='Wrong request'), 400
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    root_dir = request.json.get("root_dir", ROOT_DIR)
    movie_dir_re = request.json.get("movie_dir_re", MOVIE_DIR_RE)
    job_interval = request.json.get("job_interval", JOB_INTERVAL)
    if not username or not password:
        return jsonify(status='error', msg='Wrong request'), 400
    result = sql_util.init_database(username, password, root_dir,
                                    movie_dir_re, job_interval)
    if result:
        return jsonify(status='success', msg='App init finished'), 200
    else:
        return jsonify(status='error', msg='Wrong request, app has already inited'), 400


@app.route('/api/app/movie_data/update', methods=["GET"])
@jwt_required()
def update_data_immediatlly():
    if not current_user.admin:
        return jsonify(status='error', msg='Wrong request'), 400
    if c.is_running:
        return jsonify(status='error', msg='Update job is running now'), 400

    t = Thread(target=c.update_movie_data)
    t.start()
    return jsonify(status='success', msg='Update job started'), 200


@app.route('/api/app/movie_data/update/progress', methods=["GET"])
@jwt_required()
def get_update_progress():
    if not current_user.admin:
        return jsonify(status='error', msg='Wrong request'), 400
    return jsonify(status='success', msg=c.get_current_msg())


@app.route('/api/app/movie_data/update/log', methods=["GET"])
@jwt_required()
def get_update_log():
    if not current_user.admin:
        return jsonify(status='error', msg='Wrong request'), 400
    return jsonify(status='success', msg=c.messages)


if __name__ == '__main__':
    os.system('service nginx restart')
    t = Thread(target=c.run, args=(1800,))
    t.start()
    app.run(host='0.0.0.0', port=5006)
