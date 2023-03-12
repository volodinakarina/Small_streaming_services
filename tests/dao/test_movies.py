import pytest

from project.dao import MoviesDAO
from project.models import Movie


class TestMoviesDAO:

    @pytest.fixture
    def movies_dao(self, db):
        return MoviesDAO(db.session)

    @pytest.fixture
    def movie_1(self, db):
        movie = Movie(title="Movie_1")
        db.session.add(movie)
        db.session.commit()
        return movie

    @pytest.fixture
    def movie_2(self, db):
        movie = Movie(title="Movie_2")
        db.session.add(movie)
        db.session.commit()
        return movie

    @pytest.fixture
    def movies(self, db):
        objects = [
            Movie(title="Movie_1", year=1999),
            Movie(title="Movie_2", year=2000),
            Movie(title="Movie_3", year=2001),
            Movie(title="Movie_4", year=2002),
            Movie(title="Movie_5", year=2003),
            Movie(title="Movie_6", year=2004),
            Movie(title="Movie_7", year=2022),
            Movie(title="Movie_8", year=2005),
            Movie(title="Movie_9", year=2006),
            Movie(title="Movie_10", year=2007),
            Movie(title="Movie_11", year=2008),
            Movie(title="Movie_12", year=2009),
            Movie(title="Movie_13", year=2010),
            Movie(title="Movie_14", year=2011)
        ]
        db.session.add_all(objects)
        db.session.commit()
        return objects

    def test_get_movie_by_id(self, movie_1, movies_dao):
        assert movies_dao.get_by_id(movie_1.id) == movie_1

    def test_get_movie_by_id_not_found(self, movies_dao):
        assert not movies_dao.get_by_id(1)

    def test_get_all_movies(self, movies_dao, movie_1, movie_2):
        assert movies_dao.get_all(page=None, status=None) == [movie_1, movie_2]

    def test_get_movies_by_page(self, app, movies_dao, movies):
        app.config['ITEMS_PER_PAGE'] = 12
        assert movies_dao.get_all(page=1, status=None) == movies[:12]
        assert movies_dao.get_all(page=2, status=None) == movies[12:]
        assert movies_dao.get_all(page=3, status=None) == []

    def test_get_movies_by_status(self, app, movies_dao, movies):
        app.config['ITEMS_PER_PAGE'] = 12
        assert movies_dao.get_all(page=1, status='new') == [movies[6], *movies[13:6:-1], *movies[5:1:-1]]
        assert movies_dao.get_all(page=2, status='new') == [*movies[1::-1]]
        assert movies_dao.get_all(page=3, status='new') == []