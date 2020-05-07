from os.path import abspath
from app.data.__all_models import *
from app.data import db_session
import os
from flask import Flask
from flask_mail import Message, Mail

project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, 'templates')
app = Flask(__name__, template_folder=template_path)
app.config['SECRET_KEY'] = 'GmWFab*Y2GK%B5%NTE=&6pF6&^Gbw*P2$HcG-gtPX&JKNw&!3ad'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = 'flaskmail10@gmail.com'
app.config['MAIL_DEFAULT_SENDER'] = 'aboutmovies.servies@gmail.com'
app.config['MAIL_PASSWORD'] = 'GmWFab709ghk'
app.config['SECURITY_PASSWORD_SALT'] = "0"
app.config['UPLOAD_FOLDER'] = './tmp'
mail = Mail(app)

db_session.global_init(abspath('app/db/data.sqlite'))


def get_session():
    return db_session.create_session()


def send_email(subject, recipients, text_body):
    msg = Message(subject, sender=app.config["MAIL_DEFAULT_SENDER"], recipients=[recipients])
    msg.body = text_body
    with app.app_context():
        mail.send(msg)


from app.blueprints import user

app.register_blueprint(user.user_blueprint)
