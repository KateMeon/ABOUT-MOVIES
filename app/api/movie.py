from flask_restful import abort, Resource
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
        session = app.get_session()
        abort_if_movie_not_found(movie_id)
        movie = session.query(Movie).get(movie_id)
        return jsonify(
            {
                'movie': ''
            }
        )

    def delete(self, movie_id):
        session = app.get_session()
        abort_if_movie_not_found(movie_id)
        session.query(Movie).delete(movie_id)
        return jsonify(
            {
                'OK': "success"
            }
        )
