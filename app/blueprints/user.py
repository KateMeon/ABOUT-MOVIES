from flask import Flask
from flask import render_template, redirect
from flask_login import current_user, LoginManager, logout_user, login_required
import os
from os.path import abspath
from werkzeug.security import generate_password_hash
from app.data import db_session
from app.data.users import *
from app.forms import *

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, 'templates')
app = Flask(__name__, template_folder=template_path)
app.config['SECRET_KEY'] = '_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
@app.route('/index')
def main():
    return render_template('index.html', title='ABOUT MOVIES')


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = User()
        user.login = form.login.data
        user.password = form.password.data
        session.add(user)
        session.commit()
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/login', methods=['POST', "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = User()
        user.login = form.login.data
        user.hashed_password = generate_password_hash(form.password.data)
        session.add(user)
        session.commit()
    return render_template('login.html', title='Авторизация', form=form)
