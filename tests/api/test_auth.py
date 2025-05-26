from api.api_manager import ApiManager


class TestAuthAPI:

    def test_register_user(self, api_manager: ApiManager, test_user):
        """
        Тест на регистрацию пользователя.
        """
        response = api_manager.auth_api.register_user(test_user)
        response_data = response.json()
        assert response_data['email'] == test_user['email'], (
            'Email не совпадает'
        )
        assert 'id' in response_data, 'ID пользователя отсутствует в ответе'
        assert 'roles' in response_data, (
            'Роли пользователя отсутствуют в ответе'
        )
        assert 'USER' in response_data['roles'], (
            'Роль USER должна быть у пользователя'
        )

    def test_register_and_login_user(
        self, api_manager: ApiManager, registered_user
    ):
        """
        Тест на регистрацию и авторизацию пользователя.
        """
        login_data = {
            'email': registered_user['email'],
            'password': registered_user['password']
        }
        response = api_manager.auth_api.login_user(
            login_data, expected_status=200
        )
        response_data = response.json()
        assert response_data['user']['email'] == login_data['email'], (
            'Email не совпадает'
        )
        assert 'accessToken' in response_data, (
            'Токен доступа пользователя отсутствует в ответе'
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
