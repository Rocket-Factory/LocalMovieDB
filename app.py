from flask import Flask, render_template, request, jsonify
from database import Movie, Tag, DBSession
from sqlalchemy import text
from config import PAGE_TITLE, PRE_URI, BROWSER_LINK,AFTER_URI

app = Flask(__name__, static_url_path='',
            static_folder='static')


@app.route('/')
def index():
    return render_template('index.html', title=PAGE_TITLE, pre_uri=PRE_URI, browser_link=BROWSER_LINK, after_uri=AFTER_URI)


@app.route('/api/movies')
def get_movies():
    page = 1
    limit = 10
    order_by = 'update_date'
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
    session = DBSession()
    if 'q' in args:
        if order_by == 'update_date':
            movies = session.query(Movie).filter(Movie.title.like('%{}%'.format(args['q']))).order_by(
                Movie.update_date).slice(
                (page - 1) * limit, page * limit).all()
        elif order_by == '-update_date':
            movies = session.query(Movie).filter(Movie.title.like('%{}%'.format(args['q']))).order_by(
                Movie.update_date.desc()).slice((page - 1) * limit, page * limit).all()
        else:
            movies = session.query(Movie).filter(Movie.title.like('%{}%'.format(args['q']))).order_by(
                text(order_by)).slice(
                (page - 1) * limit, page * limit).all()
    else:
        if order_by == 'update_date':
            movies = session.query(Movie).filter_by(**args).order_by(Movie.update_date).slice(
                (page - 1) * limit, page * limit).all()
        elif order_by == '-update_date':
            movies = session.query(Movie).filter_by(**args).order_by(Movie.update_date.desc()).slice(
                (page - 1) * limit,
                page * limit).all()
        else:
            movies = session.query(Movie).filter_by(**args).order_by(text(order_by)).slice((page - 1) * limit,
                                                                                           page * limit).all()

    result = [movie.to_json() for movie in movies]

    return jsonify(result)


@app.route('/api/tags')
def get_tags():
    page = 1
    limit = 100
    args = request.args.to_dict()
    if 'page' in args:
        page = int(args['page'])
        args.pop('page')
    if 'limit' in args:
        limit = int(args['limit'])
        args.pop('limit')

    session = DBSession()
    tags = session.query(Tag).order_by(Tag.text).slice((page - 1) * limit, page * limit).all()
    result = [tag.to_json() for tag in tags]

    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
