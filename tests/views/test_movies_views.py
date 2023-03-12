import pytest

from project.models import Movie


class TestMoviesView:
    @pytest.fixture
    def movie(self, db):
        obj = Movie(**{
            "title": "Омерзительная восьмерка",
            "description": "США после Гражданской войны....",
            "trailer": "https://www.youtube.com/watch?v=lmB9VWm0okU",
            "year": 2015,
            "rating": 7.8,
            "genre_id": 4,
            "director_id": 2
        })
        db.session.add(obj)
        db.session.commit()
        return obj

    def test_many(self, client, movie):
        response = client.get("/movies/")
        assert response.status_code == 200
        assert type(response.json) == list
        assert {"id", "title", "description", "trailer", "year",
                "rating", "genre_id", "director_id", "genre", "director"} <= response.json[0].keys()

    def test_movie(self, client, movie):
        response = client.get("/movies/1/")
        assert response.status_code == 200
        assert {"id", "title", "description", "trailer", "year",
                "rating", "genre_id", "director_id", "genre", "director"} <= response.json.keys()

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

    def test_movies_without_pages(self, client, movies):
        response = client.get("/movies/")
        assert response.status_code == 200
        assert len(response.json) == 14

    def test_movies_pages(self, client, movies):
        response = client.get("/movies/?page=1")
        assert response.status_code == 200
        assert len(response.json) == 12

        response = client.get("/movies/?page=2")
        assert response.status_code == 200
        assert len(response.json) == 2

    def test_movies_status(self, client, movies):
        response = client.get("/movies/?page=1&status=new")
        assert response.status_code == 200
        assert len(response.json) == 12

        movie1, movie2 = response.json[0], response.json[1]
        assert movie1["year"] == 2022 and movie2["year"] == 2011

    def test_movies(self, client, movies):
        response = client.get("/movies/14/")
        assert response.status_code == 200
        assert response.json["id"] == 14
        assert response.json["title"] == "Movie_14"
        assert response.json["year"] == 2011

    def test_movie_not_found(self, client, movies):
        response = client.get("/movies/15/")
        assert response.status_code == 404