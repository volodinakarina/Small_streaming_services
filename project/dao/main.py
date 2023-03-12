from project.dao.base import BaseDAO
from project.models import Movie, Director, Genre


class MoviesDAO(BaseDAO[Movie]):
    __model__ = Movie


class DirectorsDAO(BaseDAO[Director]):
    __model__ = Director


class GenresDAO(BaseDAO[Genre]):
    __model__ = Genre