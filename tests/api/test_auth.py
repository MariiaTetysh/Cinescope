import datetime

import allure
import pytest
from pytest_check import check

from api.api_manager import ApiManager
from db_requester.models import UserDBModel
from models.model import (RegisterUserResponse, Roles, TestUser, User,
                          UserRegistration)
from resources.user_creds import AdminCreds, SuperAdminCreds


class TestAuthAPI:

    def test_register_user(
            self, api_manager: ApiManager, creation_user_data_with_pydantic
    ):
        response = api_manager.auth_api.register_user(
            user_data=creation_user_data_with_pydantic
        )
        register_user_response = RegisterUserResponse(**response.json())
        assert register_user_response.email == (
            creation_user_data_with_pydantic.email
        ), "Email не совпадает"

    @pytest.fixture
    def user(self, request):
        return request.getfixturevalue(request.param)

    @pytest.mark.parametrize("user, expected_status", [
        (('super_admin'), 201),
        (('admin'), 201),
        (('common_user'), 201),
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
        if response.status_code == 201:
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
            'email': registered_user.email,
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
            'password': registered_user.password
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

    def test_register_user_db_session(
        self, api_manager: ApiManager,
        test_user: TestUser, db_session
    ):
        """
        Тест на регистрацию пользователя с проверкой в базе данных.
        """
        # выполняем запрос на регистрацию нового пользователя
        response = api_manager.auth_api.register_user(test_user)
        register_user_response = RegisterUserResponse(**response.json())

        # Проверяем добавил ли сервис Auth нового пользователя в базу данных
        users_from_db = db_session.query(UserDBModel).filter(
            UserDBModel.id == register_user_response.id)
        print(users_from_db)

        # получили обьект из бзы данных и проверили что он действительно существует в единственном экземпляре
        assert users_from_db.count() == 1, "обьект не попал в базу данных"
        # Достаем первый и единственный обьект из списка полученных
        user_from_db = users_from_db.first()
        # можем осуществить проверку всех полей в базе данных например Email
        assert user_from_db.email == test_user.email, "Email не совпадает"
        # assert user_from_db['email'] == test_user.email, "Email не совпадает"

    def test_register_user_mock(self, api_manager: ApiManager, test_user: TestUser, mocker):
        # Ответ полученный из мок сервиса
        mock_response = RegisterUserResponse(  # Фиктивный ответ
            id="id",
            email="email@email.com",
            fullName="fullName",
            verified=True,
            banned=False,
            roles=[Roles.SUPER_ADMIN],
            createdAt=str(datetime.datetime.now())
        )

        # Мокаем метод register_user в auth_api
        mocker.patch.object(
            api_manager.auth_api,  # Объект, который нужно замокать
            'register_user',       # Метод, который нужно замокать
            return_value=mock_response  # Фиктивный ответ
        )
        # Вызываем метод, который должен быть замокан
        register_user_response = api_manager.auth_api.register_user(test_user)
        # Проверяем, что ответ соответствует ожидаемому
        assert register_user_response.email == mock_response.email, "Email не совпадает"

    @allure.title("Тест регистрации пользователя с помощью Mock")
    @allure.severity(allure.severity_level.MINOR)
    @allure.label("qa_name", "Ivan Petrovich")
    def test_register_user_mock_with_allure(self, api_manager: ApiManager, test_user: TestUser, mocker):
        with allure.step(" Мокаем метод register_user в auth_api"):
            mock_response = RegisterUserResponse(  # Фиктивный ответ
                id="id",
                email="email@email.com",
                fullName="fullName",
                verified=True,
                banned=False,
                roles=[Roles.SUPER_ADMIN],
                createdAt=str(datetime.datetime.now())
            )

            mocker.patch.object(
                api_manager.auth_api,  # Объект, который нужно замокать
                'register_user',       # Метод, который нужно замокать
                return_value=mock_response  # Фиктивный ответ
            )

        with allure.step("Вызываем метод, который должен быть замокан"):
            register_user_response = api_manager.auth_api.register_user(
                test_user)

        with allure.step("Проверяем, что ответ соответствует ожидаемому"):
            # обратите внимание на вложенность allure.step
            with allure.step("Проверка поля персональных данных"):
                with check:
                    # Строка ниже выдаст исклющение и но выполнение теста продолжится
                    check.equal(register_user_response.fullName,
                                "INCORRECT_NAME", "НЕСОВПАДЕНИЕ fullName")
                    check.equal(register_user_response.email,
                                mock_response.email)

            with allure.step("Проверка поля banned"):
                with check("Проверка поля banned"):  # можно использовать вместо allure.step
                    check.equal(register_user_response.banned,
                                mock_response.banned)
