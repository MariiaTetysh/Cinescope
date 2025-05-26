import pytest
import requests

from constants import BASE_URL_AUTH, REGISTER_ENDPOINT
from api.api_manager import ApiManager
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator


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
        "roles": ["USER"]
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
