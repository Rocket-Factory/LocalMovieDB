from flask import Flask, render_template, request, jsonify
from sqlalchemy.orm import aliased
from sqlalchemy.sql.expression import func
from database import Movie, Tag, MovieTag, DBSession
from sqlalchemy import text
from config import PAGE_TITLE, PRE_URI, BROWSER_LINK, AFTER_URI
import logging

app = Flask(__name__, static_url_path='',
            static_folder='static')

logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return render_template('index.html', title=PAGE_TITLE, pre_uri=PRE_URI, browser_link=BROWSER_LINK,
                           after_uri=AFTER_URI)

@app.route('/api/movies/random')
def get_random_movie():
    session = DBSession()
    movie = session.query(Movie).order_by(func.random()).limit(1)[1]
    return movie.to_json()

@app.route('/api/movies')
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