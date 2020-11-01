import csv
import os

from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from movie_app.domain.movie import Movie
from movie_app.adapters.repository import AbstractRepository


class SessionContextManager:

    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SQLAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self.__session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self.__session_cm.close_current_session()

    def reset_session(self):
        self.__session_cm.reset_session()

    def get_movie(self, id):
        movie = self.__session_cm.session.query(Movie).filter(Movie.__id == id).first()
        return movie


def movie_record_generator(filename: str):
    with open(filename, mode='r', encoding='utf-8-sig') as csvfile:
        movie_file_reader = csv.reader(csvfile)

        for row in movie_file_reader:
            movie = row
            movie = [item.strip() for item in movie]
            yield movie


def populate(engine: Engine, data_path: str):
    conn = engine.raw_connection()
    cursor = conn.cursor()

    global tags
    tags = dict()

    insert_movies = """
            INSERT INTO movies (
             rank, title, genre, description, director, actors, year, runtime, rating, votes, revenue, metascore)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    cursor.executemany(insert_movies, movie_record_generator(os.path.join(data_path, 'Data1000Movies.csv')))
