import pytest

from models.model import User, UserRegistration
from resources.user_creds import AdminCreds, SuperAdminCreds

from api.api_manager import ApiManager


class TestAuthAPI:

    def test_register_user(self, api_manager: ApiManager, test_user):
        """
        Тест на регистрацию пользователя c валидацей данных.
        """
        UserRegistration(**test_user)
        response = api_manager.auth_api.register_user(test_user).json()
        user = User(**response)
        assert user.email == test_user['email'], ('Email не совпадает')
        assert user.id, 'ID пользователя отсутствует в ответе'
        assert user.roles, ('Роли пользователя отсутствуют в ответе')
        assert user.roles == ['USER'], ('Роль USER должна быть у пользователя')

    @pytest.fixture
    def user(self, request):
        return request.getfixturevalue(request.param)

    @pytest.mark.parametrize("user, expected_status", [
        (('super_admin'), 200),
        (('admin'), 200),
        (('common_user'), 200),
        # ("test_login1@email.com", "asdqwe123Q!", 401),  # Сервис не может обработать логин по незареганному юзеру
        # ("", "password", 401),
    ],
        indirect=['user'],
        ids=[
            "SuperAdmin login", "Admin login", "Valid user"
            # "Invalid user", "Empty username"
    ])
    def test_login(self, user, expected_status):
        login_data = {
            "email": user.creds[0],
            "password": user.creds[1]
        }
        response = user.api.auth_api.login_user(
            login_data=login_data, expected_status=expected_status
        )
        response_data = response.json()
        if response.status_code == 200:
            assert response_data['user']['email'] == login_data['email'], (
                'Email не совпадает'
            )
            assert 'accessToken' in response_data, (
                'Токен доступа пользователя отсутствует в ответе'
            )
        else:
            assert 'message' in response_data, (
                'В ответе должно быть сообщение об ошибке'
            )

    def test_register_and_login_with_incorrect_password(
        self, api_manager: ApiManager, registered_user
    ):
        """
        Тест на регистрацию и авторизацию пользователя с некорректным паролем.
        """
        login_data = {
            'email': registered_user['email'],
            'password': 'Password1'
        }
        response = api_manager.auth_api.login_user(
            login_data, expected_status=401
        )
        response_data = response.json()
        assert 'message' in response_data, (
            'В ответе должно быть сообщение об ошибке'
        )

    def test_register_and_login_with_incorrect_email(
        self, api_manager: ApiManager, registered_user
    ):
        """
        Тест на регистрацию и авторизацию пользователя с некорректным email.
        """
        login_data = {
            'email': 'testingbookings@gmail.com',
            'password': registered_user['password']
        }
        response = api_manager.auth_api.login_user(
            login_data, expected_status=401
        )
        response_data = response.json()
        assert 'message' in response_data, (
            'В ответе должно быть сообщение об ошибке'
        )

    def test_login_with_empty_data(self, api_manager: ApiManager):
        """
        Тест на авторизацию пользователя с пустыми данными.
        """
        login_data = {}
        response = api_manager.auth_api.login_user(
            login_data, expected_status=401
        )
        response_data = response.json()
        assert 'message' in response_data, (
            'В ответе должно быть сообщение об ошибке'
        )

    def test_register_twice_user(
        self, api_manager: ApiManager, registered_user
    ):
        """
        Тест на повторную регистрацию с тем же email.
        """
        response = api_manager.auth_api.register_user(
            registered_user, expected_status=409
        )
        response_data = response.json()
        assert 'message' in response_data, (
            'В ответе должно быть сообщение об ошибке'
        )
