import sqlalchemy
from .db_session import SqlAlchemyBase


class Movie(SqlAlchemyBase):
    __tablename__ = 'movies'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    genre = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    year = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    estimation = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
