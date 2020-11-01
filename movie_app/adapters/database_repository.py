import csv
import os

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


def load_actors(session, data_path: str):
    actors = dict()
    with open(os.path.join(data_path, 'Data1000Movies.csv'), mode='r', encoding='utf-8-sig') as csv_file:
        file_reader = csv.DictReader(csv_file)

        for row in file_reader:
            for actor in row['Actor'].split(','):
                actor = actor.strip()
                if actor not in actors.keys():
                    a = Actor(actor)
                    actors[actor] = a
        session.commit()
    return actor


def load_directors(session, data_path: str):
    directors = dict()
    with open(os.path.join(data_path, 'Data1000Movies.csv'), mode='r', encoding='utf-8-sig') as csv_file:
        file_reader = csv.DictReader(csv_file)

        for row in file_reader:
            for director in row['Director'].split(','):
                director = director.strip()
                if director not in directors.keys():
                    d = Director(director)
                    directors[director] = d
                    session.add(director)
        session.commit()
    return directors


def load_genres(session, data_path: str):
    genres = dict()
    with open(os.path.join(data_path, 'Data1000Movies.csv'), mode='r', encoding='utf-8-sig') as csv_file:
        file_reader = csv.DictReader(csv_file)

        for row in file_reader:
            for genre in row['Genre'].split(','):
                genre = genre.strip()
                if genre not in genres.keys():
                    g = Genre(genre)
                    genres[genre] = g
        session.commit()
    return genres


def load_movies(session, data_path: str):
    g = load_genres(session, data_path)
    d = load_directors(session. datapath)
    a = load_actors(session, data_path)
    with open(os.path.join(data_path, 'Data1000Movies.csv'), mode='r', encoding='utf-8-sig') as csv_file:
        file_reader = csv.DictReader(csv_file)

        for row in file_reader:
            rank = int(row['Rank'].strip())
            title = row['Title']
            release_year = int(row['Year'].strip())
            actors = [a.get(actor.strip()) for actor in row['Actor'].split(',')]
            genres = [g.get(genre.strip()) for genre in row['Genre'].split(',')]
            description = row['Description'].strip()
            director = [d.get(director.strip()) for director in row['Director'].split(',')]
            runtime_minutes = int(row['Runtime (Minutes)'].strip())
            rating = float(row['Rating'].strip()) if row['Rating'].strip() != 'N/A' else row['Rating'].strip()
            votes = int(row['Votes'].strip()) if row['Votes'].strip() != 'N/A' else row['Votes'].strip()
            revenue = float(row['Revenue (Millions)'].strip()) \
                if row['Revenue (Millions)'].strip() != 'N/A' else row['Revenue (Millions)'].strip()
            metascore = int(row['Metascore'].strip()) \
                if row['Metascore'].strip() != 'N/A' else row['Metascore'].strip()

            movie = Movie(title, release_year)
            movie.rank = rank
            movie.actors = actors
            movie.genres = genres
            movie.description = description
            movie.director = director
            movie.runtime_minutes = runtime_minutes
            movie.rating = rating
            movie.votes = votes
            movie.revenue = revenue
            movie.metascore = metascore

            yield movie


def populate(session_factory, data_path):
    session = session_factory()
    file_reader = load_movies(session, data_path)
    for movie in file_reader:
        session.add(movie)
    session.commit()
