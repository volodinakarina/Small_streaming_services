from unittest.mock import patch

import pytest

from project.exceptions import ItemNotFound
from project.models import Movie
from project.services import MoviesService


class TestMoviesService:

    @pytest.fixture()
    @patch('project.dao.MoviesDAO')
    def movies_dao_mock(self, dao_mock):
        dao = dao_mock()
        dao.get_by_id.return_value = Movie(id=1, title='test_movie')
        movies = [
            Movie(id=1, title='test_movie_1', year=2010),
            Movie(id=2, title='test_movie_2', year=1999),
            Movie(id=3, title='test_movie_3', year=2000),
        ]
        dao.get_all.return_value = movies
        return dao

    @pytest.fixture()
    def movies_service(self, movies_dao_mock):
        return MoviesService(dao=movies_dao_mock)

    @pytest.fixture
    def movie(self, db):
        obj = Movie(title="movie")
        db.session.add(obj)
        db.session.commit()
        return obj

    def test_get_movie(self, movies_service, movie):
        assert movies_service.get_item(movie.id)

    def test_movie_not_found(self, movies_dao_mock, movies_service):
        movies_dao_mock.get_by_id.return_value = None

        with pytest.raises(ItemNotFound):
            movies_service.get_item(15)

    @pytest.mark.parametrize('page', (1, 2), ids=['with 1 page', 'without page'])
    def test_get_all_movies(self, movies_dao_mock, movies_service, page):
        movies = movies_service.get_all(page=page, status=None)
        assert len(movies) == 3
        assert movies == movies_dao_mock.get_all.return_value
        movies_dao_mock.get_all.assert_called_with(page=page, status=None)