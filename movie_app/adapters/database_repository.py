import csv
import os
from typing import List

from sqlalchemy.engine import Engine
from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack
from sqlalchemy.orm.exc import NoResultFound

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

    def add_director(self, director: Director):
        with self.__session_cm as scm:
            scm.session.add(director)
            scm.commit()

    def get_director(self, director) -> Director:
        director = None
        try:
            director = self.__session_cm.session.query(Director).filter(Director.__director_full_name == director).one()
        except NoResultFound:
            pass
        return director

    def add_genre(self, genre: Genre):
        with self.__session_cm as scm:
            scm.session.add(genre)
            scm.commit()

    def get_genres(self) -> List[Genre]:
        genre = None
        try:
            genre = self.__session_cm.session.query(Genre).filter(Genre.__genre_name == genre).one()
        except NoResultFound:
            pass
        return genre

    def add_actor(self, actor: Actor):
        with self.__session_cm as scm:
            scm.session.add(actor)
            scm.commit()

    def get_actor(self) -> [Actor]:
        actor = None
        try:
            actor = self.__session_cm.session.query(Genre).filter(Genre.__actor_name == actor).one()
        except NoResultFound:
            pass
        return actor

    def get_movies_by_rank(self, rank_list):
        movie = self.__session_cm.session.query(Movie).filter(Movie.__rank.in_(rank_list)).all()
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
             rank, title, genre, description, director, actors, release_year, runtime_minutes, rating, votes, revenue, metascore)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    cursor.executemany(insert_movies, movie_record_generator(os.path.join(data_path, 'Data1000Movies.csv')))

    conn.commit()
    conn.close()