from flask import Flask
from flask import render_template, redirect
from flask_login import current_user, LoginManager, logout_user, login_required
import os
from data import db_session
from data.users import *
from forms import RegistrationForm

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, './templates')
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
@app.route('/main_page')
def main():
    return render_template('index.html', title='ABOUT MOVIES')


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.login == form.login.data).first():
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")

        message_error = check_password(form.password.data)
        if message_error != 'ок':
            return render_template('registration.html', title='Регистрация',
                                   form=form,
                                   message=message_error)
        user = User()
        user.login = form.login.data
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/login', methods=['POST', "GET"])
def login():
    return render_template('login.html', title='Авторизация')


def check_password(password):
    if len(password) < 5:
        return 'Пароль слишком короткий'
    s_letter = False
    b_letter = False
    number = False
    for symbol in password:
        if symbol.isdigit():
            number = True
        elif symbol.isalpha():
            if symbol.upper() == symbol:
                b_letter = True
            elif symbol.lower() == symbol:
                s_letter = True
    if not number or not s_letter or not b_letter:
        return 'Пароль недостаточно сложный. Добавьте цифры, строчные и прописные буквы'
    return 'ок'


db_session.global_init("db/movies.sqlite")
app.run(port=8080, host='127.0.0.1')
