import csv
import os

from datetime import date
from typing import List

from sqlalchemy import desc, asc

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from movie_app.domain.actor import Actor
from movie_app.domain.director import Director
from movie_app.domain.genre import Genre
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


def load_genres(session, data_path: str):
    genres = dict()
    with open(os.path.join(data_path, 'Data1000Movies.csv'), mode='r', encoding='utf-8-sig') as csv_file:
        movie_file_reader = csv.DictReader(csv_file)

        for row in movie_file_reader:
            for genre in row['Genre'].split(','):
                genre = genre.strip()
                if genre not in genres.keys():
                    g = Genre(genre)
                    genres[genre] = g
        session.commit()
    return genres


def load_actors(session, data_path: str):
    actors = dict()
