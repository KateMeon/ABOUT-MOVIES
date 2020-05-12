from flask_restful import abort, Resource, reqparse
from flask import jsonify
from app.data.movie import Movie
from app import *


def abort_if_movie_not_found(movie_id):
    session = db_session.create_session()
    movie = session.query(Movie).get(movie_id)
    if not movie:
        abort(404)


class MovieResource(Resource):
    def get(self, movie_id):
        session = db_session.create_session()
        abort_if_movie_not_found(movie_id)
        movie = session.query(Movie).get(movie_id)
        return jsonify(
            {
                'movie': ''
            }
        )

    def delete(self, movie_id):
        session = db_session.create_session()
        abort_if_movie_not_found(movie_id)
        session.query(Movie).delete(movie_id)
        return jsonify(
            {
                'OK': "success"
            }
        )


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('genre', required=True)
parser.add_argument('year', required=True)
parser.add_argument('estimation', required=True)


class MovieListResource(Resource):
    def get(self):
        session = db_session.create_session()
        movie = session.query(Movie).all()
        return jsonify({'movie': [item.to_dict(
            only=('name', 'genre', 'year', 'estimation')) for item in movie]})

    def post(self):
        args = parser.parse_args()
        session = app.get_session()
        movie = Movie(
            name=args['name'],
            genre=args['genre'],
            year=args['year'],
            estimation=args['estimation']
        )
        session.add(movie)
        session.commit()
        return jsonify({'success': 'OK'})
