from waitress import serve
from flask import Flask
from flask import render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = '_secret_key'


@app.route('/')
@app.route('/main_page')
def main():
    return render_template('index.html')


@app.route('/registration')
def registration_form():
    return render_template('registration.html')


if __name__ == '__main__':
    serve(app, host='127.0.0.2', port=8080)
