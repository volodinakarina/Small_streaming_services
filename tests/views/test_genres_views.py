import pytest

from project.models import Genre


class TestGenresView:
    @pytest.fixture
    def genre(self, db):
        obj = Genre(name="genre")
        db.session.add(obj)
        db.session.commit()
        return obj

    def test_many(self, client, genre):
        response = client.get("/genres/")
        assert response.status_code == 200
        assert response.json == [{"id": genre.id, "name": genre.name}]

    def test_genre(self, client, genre):
        response = client.get("/genres/1/")
        assert response.status_code == 200
        assert response.json == {"id": genre.id, "name": genre.name}

    @pytest.fixture
    def genres(self, db):
        objects = [
            Genre(name="genre1"), Genre(name="genre2"), Genre(name="genre3"),
            Genre(name="genre4"), Genre(name="genre5"), Genre(name="genre6"),
            Genre(name="genre7"), Genre(name="genre8"), Genre(name="genre9"),
            Genre(name="genre10"), Genre(name="genre11"), Genre(name="genre12"),
            Genre(name="genre13"), Genre(name="genre14"), Genre(name="genre15")
        ]
        db.session.add_all(objects)
        db.session.commit()
        return objects

    def test_genres_without_pages(self, client, genres):
        response = client.get("/genres/")
        assert response.status_code == 200
        assert len(response.json) == 15

    def test_genres_pages(self, client, genres):
        response = client.get("/genres/?page=1")
        assert response.status_code == 200
        assert len(response.json) == 12

        response = client.get("/genres/?page=2")
        assert response.status_code == 200
        assert len(response.json) == 3

    def test_genres(self, client, genres):
        response = client.get("/genres/15/")
        assert response.status_code == 200
        assert response.json == {"id": 15, "name": "genre15"}

    def test_genre_not_found(self, client, genres):
        response = client.get("/genres/16/")
        assert response.status_code == 404