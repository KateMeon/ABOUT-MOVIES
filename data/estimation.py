import sqlalchemy
from .db_session import SqlAlchemyBase


class EstimationFilms(SqlAlchemyBase):
    __tablename__ = 'estimation_films'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    id_user = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    id_film = sqlalchemy.Column(sqlalchemy.String, sqlalchemy.ForeignKey('movies.id'))
    estimation = sqlalchemy.Column(sqlalchemy.String, nullable=True)
