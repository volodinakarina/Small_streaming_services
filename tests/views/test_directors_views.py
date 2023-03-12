import pytest

from project.models import Director


class TestDirectorsView:
    @pytest.fixture
    def director(self, db):
        obj = Director(name="director")
        db.session.add(obj)
        db.session.commit()
        return obj

    def test_many(self, client, director):
        response = client.get("/directors/")
        assert response.status_code == 200
        assert response.json == [{"id": director.id, "name": director.name}]

    def test_director(self, client, director):
        response = client.get("/directors/1/")
        assert response.status_code == 200
        assert response.json == {"id": director.id, "name": director.name}

    @pytest.fixture
    def directors(self, db):
        objects = [
            Director(name="director1"), Director(name="director2"), Director(name="director3"),
            Director(name="director4"), Director(name="director5"), Director(name="director6"),
            Director(name="director7"), Director(name="director8"), Director(name="director9"),
            Director(name="director10"), Director(name="director11"), Director(name="director12"),
            Director(name="director13"), Director(name="director14")
        ]
        db.session.add_all(objects)
        db.session.commit()
        return objects

    def test_directors_without_pages(self, client, directors):
        response = client.get("/directors/")
        assert response.status_code == 200
        assert len(response.json) == 14

    def test_directors_pages(self, client, directors):
        response = client.get("/directors/?page=1")
        assert response.status_code == 200
        assert len(response.json) == 12

        response = client.get("/directors/?page=2")
        assert response.status_code == 200
        assert len(response.json) == 2

    def test_directors(self, client, directors):
        response = client.get("/directors/14/")
        assert response.status_code == 200
        assert response.json == {"id": 14, "name": "director14"}

    def test_director_not_found(self, client, directors):
        response = client.get("/directors/15/")
        assert response.status_code == 404