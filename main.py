from waitress import serve
from flask import Flask
from flask import render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = '_secret_key'


@app.route('/')
@app.route('/main_page')
def main():
    return render_template('index.html', title='ABOUT MOVIES')


@app.route('/registration')
def registration_form():
    return render_template('registration.html', title='Регистрация')


@app.route('/login')
def login_form():
    return render_template('login.html', title='Вход')


if __name__ == '__main__':
    serve(app, host='127.0.0.2', port=8080)
