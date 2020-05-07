from flask import Blueprint
from app.data import db_session
from app.data.users import *
from app.forms import *
from app import app
from app import get_session
from flask import render_template, redirect
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer

user_blueprint = Blueprint('user_api', __name__, template_folder=app.template_folder)
login_manager = LoginManager()
login_manager.init_app(app)


def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except:
        return False
    return email


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
        return redirect('/')
    return render_template('registration.html', title='Registration', form=form)


@user_blueprint.route('/login', methods=['POST', "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = get_session()
        user = session.query(User).filter(User.email == form.email.data).first()
        if user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Incorrect password",
                               form=form)
    return render_template('login.html', title='Login', form=form)


@user_blueprint.route('/')
@user_blueprint.route('/index')
@user_blueprint.route('/index/token')
def main(token=''):
    if token:
        if confirm_token(token) == current_user.email:
            session = db_session.create_session()
            user = session.query(User).get(current_user.id)
            user.confirm = True
            session.commit()
            current_user.confirm = True
    return render_template('index.html', title='ABOUT MOVIES')
