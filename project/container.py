from project.dao import MoviesDAO, DirectorsDAO, GenresDAO, UserDAO
from project.services import MoviesService, DirectorsService, GenresService, UserService, AuthService
from project.setup.db import db

# DAO
movie_dao = MoviesDAO(db.session)
director_dao = DirectorsDAO(db.session)
genre_dao = GenresDAO(db.session)
user_dao = UserDAO(db.session)

# Services
movie_service = MoviesService(dao=movie_dao)
director_service = DirectorsService(dao=director_dao)
genre_service = GenresService(dao=genre_dao)
user_service = UserService(dao=user_dao)
auth_service = AuthService(user_service)
