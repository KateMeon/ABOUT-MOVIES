from flask import Blueprint, redirect, url_for
from app import *
from flask_login import LoginManager, current_user
from flask import render_template

movie_blueprint = Blueprint('movie_api', __name__, template_folder=app.template_folder)
login_manager = LoginManager()
login_manager.init_app(app)


@movie_blueprint.route('/about_movie/<movie_id>')
def about_movie():
    if not current_user.is_authenticated:
        return redirect(url_for('registration'))
    return render_template('about_movie.html', title="ABOUT MOVIES")
