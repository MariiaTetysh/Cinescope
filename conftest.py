import datetime
import time
import uuid

import pytest
import requests
from playwright.sync_api import sync_playwright
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from api.api_manager import ApiManager
from constants import BASE_URL_AUTH, REGISTER_ENDPOINT, USER_BASE_URL
from custom_requester.custom_requester import CustomRequester
from db_requester.models import UserDBModel
from entities.user import User
from enums.roles import Roles
from models.model import TestUser
from resources.db_creds import DBCreds
from resources.user_creds import AdminCreds, SuperAdminCreds
from utils.data_generator import DataGenerator

DEFAULT_UI_TIMEOUT = 130000


@pytest.fixture(scope='function')
def test_user() -> TestUser:
    # def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    # return {
    #     "email": random_email,
    #     "fullName": random_name,
    #     "password": random_password,
    #     "passwordRepeat": random_password,
    #     "roles": [Roles.USER.value]
    # }
    return TestUser(
        email=random_email,
        fullName=random_name,
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER.value]
    )


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
    # registered_user["id"] = response_data["id"]
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
    user_pool = []  # Список для хранения всех созданных в тесте сессий

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


@pytest.fixture(scope="function")
def creation_user_data_with_pydantic():
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return TestUser(
        email=random_email,
        fullName=random_name,
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER.value],
        verified=True,
        banned=False
    )


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
def super_admin_token(super_admin):
    response = super_admin.api.auth_api.authenticate(super_admin.creds)
    token = response["accessToken"]
    return token


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
def common_user(user_session, super_admin, creation_user_data_with_pydantic):
    new_session = user_session()

    common_user = User(
        creation_user_data_with_pydantic.email,
        creation_user_data_with_pydantic.password,
        [Roles.USER.value],
        new_session)

    super_admin.api.user_api.create_user(creation_user_data_with_pydantic)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user


# Создаем движок (engine) для подключения к базе данных
engine = create_engine(
    f"postgresql+psycopg2://{DBCreds.DB_USER}:{DBCreds.DB_PASSWORD}@{DBCreds.DB_HOST}:{DBCreds.DB_PORT}/{DBCreds.DB_NAME}")
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)  # Создаем фабрику сессий

# @pytest.fixture(scope="module")
# def db_session():
#     """
#     Фикстура, которая создает и возвращает сессию для работы с базой данных.
#     После завершения теста сессия автоматически закрывается.
#     """
#     # Создаем новую сессию
#     db_session = SessionLocal()
#     # Возвращаем сессию в тест
#     yield db_session
#     # Закрываем сессию после завершения теста
#     db_session.close()


@pytest.fixture(scope="module")
def db_session():
    """
    Фикстура с областью видимости module.
    Тестовые данные создаются один раз для всех тестов в модуле.
    """
    session = SessionLocal()

    # Создаем тестовые данные
    test_user = UserDBModel(
        id=f'{uuid.uuid4()}',
        email=DataGenerator.generate_random_email(),
        full_name=DataGenerator.generate_random_name(),
        password=DataGenerator.generate_random_password(),
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
        verified=False,
        banned=False,
        roles="{USER}"
    )
    session.add(test_user)  # добавляем обьект в базу данных
    session.commit()  # сохраняем изменения для всех остальных подключений

    yield session  # можете запустить тесты в дебаг режиме и поставить тут брекпойнт
    # зайдите в базу и убедитесь что нывй обьект был создан

    # код ниже выполнится после всех запущеных тестов
    session.delete(test_user)  # Удаляем тестовые данные
    session.commit()  # сохраняем изменения для всех остальных подключений
    session.close()  # завершем сессию (отключаемся от базы данных)


@pytest.fixture
def delay_between_retries():
    time.sleep(2)  # Задержка в 2 секунды\ это не обязательно но
    yield          # нужно понимать что такая возможность имеется


# Браузер запускается один раз для всей сессии

@pytest.fixture(scope='session')
def browser(playwright):
    # headless=True для CI/CD, headless=False для локальной разработки
    browser = playwright.chromium.launch(headless=False)
    yield browser  # yield возвращает значение фикстуры, выполнение теста продолжится после yield
    browser.close()  # Браузер закрывается после завершения всех тестов


@pytest.fixture(scope='function')  # Контекст создается для каждого теста
def context(browser):
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True,
                          sources=True)  # Трассировка для отладки
    # Установка таймаута по умолчанию
    context.set_default_timeout(DEFAULT_UI_TIMEOUT)
    yield context  # yield возвращает значение фикстуры, выполнение теста продолжится после yield
    context.close()  # Контекст закрывается после завершения теста


@pytest.fixture(scope="function")  # Страница создается для каждого теста
def page(context):
    page = context.new_page()
    yield page  # yield возвращает значение фикстуры, выполнение теста продолжится после yield
    page.close()  # Страница закрывается после завершения теста
