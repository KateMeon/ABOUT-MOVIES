from flask import Blueprint
from app import *

movie_blueprint = Blueprint('movie_api', __name__, template_folder=app.template_folder)
