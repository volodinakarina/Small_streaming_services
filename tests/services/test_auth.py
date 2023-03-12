import time
from unittest.mock import patch

import pytest

from project.models import User
from project.services import AuthService, UserService


class TestAuthService:

    @pytest.fixture()
    @patch('project.dao.UserDAO')
    def auth_dao_mock(self, dao_mock):
        dao = dao_mock()
        dao.get_by_email.return_value = User(
            id=1, email='user1_test@email.me', password='UBbzr6FvcqYGvujlFWZOF7WLQjMtDJR8ptM15jKufOE=',
            name='Ivan', surname='Ivanov', favourite_genre=''
        )
        return dao

    @pytest.fixture()
    def auth_service(self, auth_dao_mock):
        return AuthService(user_service=UserService(auth_dao_mock))

    def test_generate_and_check_tokens(self, app, auth_service):
        with app.app_context():
            tokens = auth_service.generate_tokens('user1_test@email.me', 'password', is_refresh=False)
            refresh_token = tokens['refresh_token']

            assert 'access_token' in tokens and 'refresh_token' in tokens

            time.sleep(1)

            new_tokens = auth_service.approve_refresh_token(refresh_token)

            assert 'access_token' in new_tokens and 'refresh_token' in new_tokens
            assert refresh_token != new_tokens['refresh_token']