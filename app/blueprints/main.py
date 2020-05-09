from app import *
from flask import render_template, redirect, Blueprint
from flask_login import current_user
from itsdangerous import URLSafeTimedSerializer
from app.data.users import User

blueprint = Blueprint('main_api', __name__, template_folder=app.template_folder)


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


@blueprint.route('/')
@blueprint.route('/<token>')
def main(token=''):
    if token:
        if confirm_token(token) == current_user.email:
            session = app.get_session()
            user = session.query(User).get(current_user.id)
            user.confirm = True
            session.commit()
            current_user.confirm = True  # для того что бы результат подтверждения был сразу
    return render_template('main.html', title='ABOUT MOVIES')


@blueprint.route("/index")
def index_page():
    return render_template("index.html", title="ABOUT MOVIES")
