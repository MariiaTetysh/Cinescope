import pytest
import requests

from constants import BASE_URL_AUTH, USER_BASE_URL, REGISTER_ENDPOINT
from api.api_manager import ApiManager
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator
from entities.user import User
from resources.user_creds import SuperAdminCreds, AdminCreds
from enums.roles import Roles


@pytest.fixture(scope='function')
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": [Roles.USER.value]
    }


@pytest.fixture(scope="function")
def registered_user(requester, test_user):
    """
    Фикстура для регистрации и получения данных
    зарегистрированного пользователя.
    """
    response = requester.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user,
        expected_status=201
    )
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user


@pytest.fixture(scope="session")
def requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL_AUTH)


@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session, BASE_URL_AUTH)


@pytest.fixture(scope='function')
def test_movie():
    """
    Генерация случайного фильма для тестов.
    """
    random_film_name = DataGenerator.generate_random_film_name()
    random_price = DataGenerator.generate_random_price()

    return {
        "name": random_film_name,
        "imageUrl": "https://image.url",
        "price": random_price,
        "description": f"Film {random_film_name} description",
        "location": "SPB",
        "published": True,
        "genreId": 1
    }


@pytest.fixture(scope='function')
def test_movie_min_values():
    """
    Генерация случайного фильма для тестов
    с минимальным набором обязательных полей.
    """
    random_film_name = DataGenerator.generate_random_film_name()
    random_price = DataGenerator.generate_random_price()

    return {
        "name": random_film_name,
        "price": random_price,
        "description": f"Film {random_film_name} description",
        "location": "SPB",
        "published": True,
        "genreId": 1
    }


@pytest.fixture(scope='function')
def admin_user():
    """
    Фикстура пользователя с правами администратора для тестов.
    """
    return {
        'email': 'test-admin@mail.com',
        'password': 'KcLMmxkJMjBD1'
    }

@pytest.fixture
def user_session():
    user_pool = [] #Список для хранения всех созданных в тесте сессий

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session, base_url=USER_BASE_URL)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()

@pytest.fixture(scope="function")
def creation_user_data(test_user):
    updated_data = test_user.copy()
    updated_data.update({
        "verified": True,
        "banned": False
    })
    return updated_data

@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture
def admin(user_session):
    new_session = user_session()

    admin = User(
        AdminCreds.USERNAME,
        AdminCreds.PASSWORD,
        [Roles.ADMIN.value],
        new_session)

    admin.api.auth_api.authenticate(admin.creds)
    return admin


@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        [Roles.USER.value],
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user