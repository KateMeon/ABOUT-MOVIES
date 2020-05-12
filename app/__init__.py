from os.path import abspath
from app.data.__all_models import *
from app.data import db_session
import os
from flask import Flask
from flask_restful import Api

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, 'templates')
app = Flask(__name__, template_folder=template_path)
API = Api(app)
app.config['SECRET_KEY'] = 'GmWFab*Y2GK%B5%NTE=&6pF6&^Gbw*P2$HcG-gtPX&JKNw&!3ad'

db_session.global_init(abspath('app/db/data.sqlite'))


def get_session():
    return db_session.create_session()


from app.api.movie import MovieResource, MovieListResource

API.add_resource(MovieListResource, '/api/movies')
API.add_resource(MovieResource, '/api/movie/<int:movie_id>')

from app.blueprints import user
from app.blueprints import main
from app.blueprints import movie

app.register_blueprint(user.user_blueprint)
app.register_blueprint(main.blueprint)
app.register_blueprint(movie.movie_blueprint)
