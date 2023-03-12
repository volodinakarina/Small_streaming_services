import pytest

from project.dao import GenresDAO
from project.models import Genre


class TestGenresDAO:

    @pytest.fixture
    def genres_dao(self, db):
        return GenresDAO(db.session)

    @pytest.fixture
    def genre_1(self, db):
        genre = Genre(name="Боевик")
        db.session.add(genre)
        db.session.commit()
        return genre

    @pytest.fixture
    def genre_2(self, db):
        genre = Genre(name="Комедия")
        db.session.add(genre)
        db.session.commit()
        return genre

    def test_get_genre_by_id(self, genre_1, genres_dao):
        assert genres_dao.get_by_id(genre_1.id) == genre_1

    def test_get_genre_by_id_not_found(self, genres_dao):
        assert not genres_dao.get_by_id(1)

    def test_get_all_genres(self, genres_dao, genre_1, genre_2):
        assert genres_dao.get_all(page=None, status=None) == [genre_1, genre_2]

    def test_get_genres_by_page(self, app, genres_dao, genre_1, genre_2):
        app.config['ITEMS_PER_PAGE'] = 1
        assert genres_dao.get_all(page=1, status=None) == [genre_1]
        assert genres_dao.get_all(page=2, status=None) == [genre_2]
        assert genres_dao.get_all(page=3, status=None) == []
