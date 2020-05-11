from flask import Blueprint
from app.data import db_session
from flask_login import LoginManager, logout_user, login_required, login_user
from app.data.users import *
from app.forms import *
from app import app
from app import get_session
from flask import render_template, redirect, request

user_blueprint = Blueprint('user_api', __name__, template_folder=app.template_folder)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = get_session()
    return session.query(User).get(user_id)


@user_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@user_blueprint.route('/registration', methods=['POST', 'GET'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        session = get_session()
        user = User()
        user.email = form.email.data
        user.login = form.login.data
        user.hashed_password = generate_password_hash(form.password.data)
        session.add(user)
        session.commit()
        login_user(user, remember=True)
        return redirect('/')
    return render_template('registration.html', title='Registration', form=form)


@user_blueprint.route('/login', methods=['POST', "GET"])
def login():
    form = LoginForm()
    if request.method == "POST":
        session = get_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Incorrect password",
                               form=form)
    return render_template('login.html', title='Login', form=form)
