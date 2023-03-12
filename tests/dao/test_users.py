import pytest
from sqlalchemy.exc import IntegrityError

from project.dao import UserDAO
from project.models import User, Movie


class TestUserDAO:

    @pytest.fixture
    def users_dao(self, db):
        return UserDAO(db.session)

    @pytest.fixture
    def user_1(self, db):
        user = User(
            email="me@email.me", password="UBbzr6FvcqYGvujlFWZOF7WLQjMtDJR8ptM15jKufOE",
            name="Ivan", surname="Ivanov", favourite_genre=""
        )
        db.session.add(user)
        db.session.commit()
        return user

    @pytest.fixture
    def user_2(self, db):
        user = User(
            email="second@email.me", password="UBbzr6FvcqYGvujlFWZOF7WLQjMtDJR8ptM15jKufOE",
            name="Michael", surname="Myers", favourite_genre=6
        )
        db.session.add(user)
        db.session.commit()
        return user

    @pytest.fixture
    def movie_1(self, db):
        movie = Movie(title="Карты, деньги, два ствола")
        db.session.add(movie)
        db.session.commit()
        return movie

    def test_get_user_by_email(self, user_2, users_dao):
        assert users_dao.get_by_email(user_2.email) == user_2

    def test_get_user_by_email_not_found(self, users_dao):
        assert not users_dao.get_by_email(1)

    def test_create_new_user(self, users_dao):
        new_user = {"email": "test@email.me", "password": "password"}

        assert users_dao.create(new_user)

        with pytest.raises(IntegrityError):
            users_dao.create(new_user)

    def test_update_user_data(self, user_1, users_dao):
        user_1.name = "Mikhail"
        users_dao.update(user_1)
        user_1 = users_dao.get_by_email(user_1.email)

        assert user_1.name == "Mikhail" and user_1.surname == "Ivanov"

    def test_add_favorite(self, user_1, movie_1, users_dao):
        users_dao.add_favorite(user_1.id, movie_1.id)
        fav_movie = users_dao.get_favorites(user_1.id)

        assert len(fav_movie) == 1
        assert fav_movie[0].title == "Карты, деньги, два ствола"

    def test_delete_favorite(self, user_1, movie_1, users_dao):
        users_dao.add_favorite(user_1.id, movie_1.id)
        users_dao.delete_favorite(user_1.id, movie_1.id)

        assert len(users_dao.get_favorites(user_1.id)) == 0