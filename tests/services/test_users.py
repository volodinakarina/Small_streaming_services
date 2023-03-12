from unittest.mock import patch

import pytest

from project.exceptions import ItemNotFound
from project.models import User, Movie
from project.services import UserService


class TestUsersService:

    @pytest.fixture()
    @patch('project.dao.UserDAO')
    def users_dao_mock(self, dao_mock):
        dao = dao_mock()
        dao.get_by_email.return_value = User(
            id=1, email='user1_test@email.me', password='UBbzr6FvcqYGvujlFWZOF7WLQjMtDJR8ptM15jKufOE=',
            name='Ivan', surname='Ivanov', favourite_genre=''
        )
        dao.create.return_value = User(id=1, email='user2_test@email.me', password='password')
        dao.get_favorites.return_value = [Movie(title="Movie_1"), Movie(title="Movie_9")]
        return dao

    @pytest.fixture()
    def users_service(self, users_dao_mock):
        return UserService(dao=users_dao_mock)

    def test_get_by_email(self, users_service, users_dao_mock):
        users_dao_mock.get_by_email.return_value = None

        with pytest.raises(ItemNotFound):
            users_service.get_by_email('not_user@email')

    def test_create(self, app, users_service, users_dao_mock):
        user = users_dao_mock.create({'email': 'user2_test@email.me', 'password': 'password'})
        with app.app_context():
            assert users_service.compare_passwords('UBbzr6FvcqYGvujlFWZOF7WLQjMtDJR8ptM15jKufOE=', user.password)
            assert user.email == 'user2_test@email.me'

    def test_generate_hash(self, app, users_service):
        with app.app_context():
            hash_ = users_service.generate_hash('password')
            assert users_service.compare_passwords(hash_, 'password')

    def test_get_favorites(self, users_dao_mock):
        assert len(users_dao_mock.get_favorites(1)) == 2