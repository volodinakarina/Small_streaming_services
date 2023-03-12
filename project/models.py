from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from project.setup.db import models


class Movie(models.Base):
    __tablename__ = 'movies'

    title = Column(String(100), unique=True, nullable=False)
    description = Column(String(5000))
    trailer = Column(String(200))
    year = Column(Integer())
    rating = Column(Float())
    genre_id = Column(Integer(), ForeignKey("genres.id"))
    genre = relationship("Genre")
    director_id = Column(Integer(), ForeignKey("directors.id"))
    director = relationship("Director")


class Director(models.Base):
    __tablename__ = 'directors'

    name = Column(String(100), unique=True, nullable=False)


class Genre(models.Base):
    __tablename__ = 'genres'

    name = Column(String(100), unique=True, nullable=False)


class User(models.Base):
    __tablename__ = 'users'

    email = Column(String(200), unique=True, nullable=False)
    password = Column(String(200), nullable=False)
    name = Column(String(100))
    surname = Column(String(200))
    favourite_genre = Column(String(200))


class Favorite(models.Base):
    __tablename__ = 'favorites'

    user_id = Column(Integer(), ForeignKey("users.id"))
    user = relationship("User")
    movie_id = Column(Integer(), ForeignKey("movies.id"))
    movie = relationship("Movie")
