from sqlalchemy import (
    MetaData, Table, Column, String, Integer, Float, Text
)
from sqlalchemy.orm import mapper

from movie_app.domain.movie import Movie


metadata = MetaData()

movies = Table(
    'movies', metadata,
    Column('rank', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=True),
    Column('genre', String(255), nullable=True),
    Column('description', Text, nullable=True),
    Column('director', String(255), nullable=True),
    Column('actors', String(255), nullable=True),
    Column('release_year', Integer, nullable=True),
    Column('runtime_minutes', Integer, nullable=True),
    Column('rating', Float, nullable=True),
    Column('votes', Integer, nullable=True),
    Column('revenue', Float, nullable=True),
    Column('metascore', Integer, nullable=True),
)


def map_model_to_tables():
    mapper(Movie, movies, properties={
        '_rank': movies.c.rank,
        '_title': movies.c.title,
        '_genre': movies.c.genre,
        '_description': movies.c.description,
        '_director': movies.c.director,
        '_actors': movies.c.actors,
        '_release_year': movies.c.release_year,
        '_runtime_minutes': movies.c.runtime_minutes,
        '_rating': movies.c.rating,
        '_votes': movies.c.votes,
        '_revenue:': movies.c.revenue,
        '_metascore': movies.c.metascore
    })
