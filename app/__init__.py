from os.path import abspath
from app.data.__all_models import *
from app.data import db_session


db_session.global_init(abspath('app/db/data.sqlite'))


def get_session():
    return db_session.create_session()
