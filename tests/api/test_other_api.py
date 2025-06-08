import datetime
import random

import allure
import pytest
from pytz import timezone

from api.api_manager import ApiManager
from db_requester.models import AccountTransactionTemplate, MovieDBModel
from utils.data_generator import DataGenerator


class TestAPIDB:

    def test_create_delete_movie(
        self, api_manager: ApiManager, super_admin_token, db_session
    ):
        # как бы выглядел SQL запрос
        """SELECT id, "name", price, description, image_url, "location", published, rating, genre_id, created_at
            FROM public.movies
            WHERE name='Test Moviej1h8qss9s5';"""

        movie_name = f"Test Movie{DataGenerator.generate_random_str(10)}"
        movies_from_db = db_session.query(MovieDBModel).filter(
            MovieDBModel.name == movie_name)

        # проверяем что до начала тестирования фильма с таким названием нет
        assert movies_from_db.count() == 0, "В базе уже присутствует фильм с таким названием"

        movie_data = {
            "name": movie_name,
            "price": 500,
            "description": "Описание тестового фильма",
            "location": "MSK",
            "published": True,
            "genreId": 3
        }
        response = api_manager.movie_api.add_movie(
            movie_data=movie_data,
            headers={"Authorization": f"Bearer {super_admin_token}"}
        )
        assert response.status_code == 201, "Фильм должен успешно создаться"
        response = response.json()

        # проверяем после вызова api_manager.movies_api.create_movie в базе появился наш фильм
        movies_from_db = db_session.query(MovieDBModel).filter(
            MovieDBModel.name == movie_name)
        assert movies_from_db.count() == 1, "В базе уже присутствует фильм с таким названием"

        movie_from_db = movies_from_db.first()
        # можете обратить внимание что в базе данных етсь поле created_at которое мы не здавали явно
        # наш сервис сам его заполнил. проверим что он заполнил его верно с погрешностью в 5 минут
        assert movie_from_db.created_at >= (datetime.datetime.now(timezone('UTC')).replace(
            tzinfo=None) - datetime.timedelta(minutes=5)), "Сервис выставил время создания с большой погрешностью"

        # Берем айди фильма который мы только что создали и  удаляем его из базы через апи
        # Удаляем фильм
        delete_response = api_manager.movie_api.delete_movies_info(
            movie_id=response["id"], token=super_admin_token)
        assert delete_response.status_code == 200, "Фильм должен успешно удалиться"

        # проверяем что в конце тестирования фильма с таким названием действительно нет в базе
        movies_from_db = db_session.query(MovieDBModel).filter(
            MovieDBModel.name == movie_name)
        assert movies_from_db.count() == 0, "Фильм небыл удален из базы!"

    def test_delete_movie(
        self, api_manager: ApiManager, db_session, super_admin_token
    ):
        """
        Тест удаления фильма.
        """
        movie_id = 54
        movies_from_db = db_session.query(MovieDBModel).filter(
            MovieDBModel.id == movie_id)
        if movies_from_db.count() == 0:
            movie_data = {
                'id': 54,
                "name": "Название тестового фильма",
                "price": 500,
                "description": "Описание тестового фильма",
                "location": "MSK",
                "published": True,
                "genreId": 3
            }
            response = api_manager.movie_api.add_movie(
                movie_data=movie_data,
                headers={"Authorization": f"Bearer {super_admin_token}"}
            )
            assert response.status_code == 201, "Фильм должен успешно создаться"
        movies_from_db = db_session.query(MovieDBModel).filter(
            MovieDBModel.id == movie_id)
        assert movies_from_db.count() == 1

        delete_response = api_manager.movie_api.delete_movies_info(
            movie_id=movie_id,
            token=super_admin_token
        )
        movies_from_db = db_session.query(MovieDBModel).filter(
            MovieDBModel.id == movie_id)
        assert delete_response.status_code == 200, "Фильм должен успешно удалиться"
        assert movies_from_db.count() == 0

        api_manager.movie_api.get_movies_info(
            movie_id=movie_id, expected_status=404
        )


@allure.epic('Тестирование транзакций')
@allure.feature("Тестирование транзакций между счетами")
class TestAccountTransactionTemplate:
    @allure.story("Корректность перевода денег между двумя счетами")
    @allure.description("""
    Этот тест проверяет корректность перевода денег между двумя счетами.
    Шаги:
    1. Создание двух счетов: Stan и Bob.
    2. Перевод 200 единиц от Stan к Bob.
    3. Проверка изменения балансов.
    4. Очистка тестовых данных.
    """)
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.label("qa_name", "Ivan Petrovich")
    @allure.title("Тест перевода денег между счетами 200 рублей")
    def test_accounts_transaction_template(self, db_session):
        # ====================================================================== Подготовка к тесту
        # Создаем новые записи в базе данных (чтоб точно быть уверенными что в базе присутствуют данные для тестирования)
        with allure.step(
                "Создание тестовых данных в базе данных: счета Stan и Bob"):
            stan = AccountTransactionTemplate(
                user=f"Stan_{DataGenerator.generate_random_int(10)}",
                balance=1000
            )
            bob = AccountTransactionTemplate(
                user=f"Bob_{DataGenerator.generate_random_int(10)}",
                balance=500
            )
            # Добавляем записи в сессию
            db_session.add_all([stan, bob])
            # Фиксируем изменения в базе данных
            db_session.commit()

        @allure.step("Функция перевода денег: transfer_money")
        @allure.description("""
            функция выполняющая транзакцию, имитация вызова функции на стороне тестируемого сервиса
            и вызывая метод transfer_money, мы какбудтобы делем запрос в api_manager.movies_api.transfer_money
            """)
        def transfer_money(session, from_account, to_account, amount):
            # пример функции выполняющей транзакцию
            # представим что она написана на стороне тестируемого сервиса
            # и вызывая метод transfer_money, мы какбудтобы делем запрос в api_manager.movies_api.transfer_money
            """
            Переводит деньги с одного счета на другой.
            :param session: Сессия SQLAlchemy.
            :param from_account_id: ID счета, с которого списываются деньги.
            :param to_account_id: ID счета, на который зачисляются деньги.
            :param amount: Сумма перевода.
            """
            with allure.step(" Получаем счета"):
                from_account = session.query(
                    AccountTransactionTemplate).filter_by(user=from_account).one()
                to_account = session.query(
                    AccountTransactionTemplate).filter_by(user=to_account).one()

            with allure.step("Проверяем, что на счете достаточно средств"):
                if from_account.balance < amount:
                    assert stan.balance == 1000
                    assert stan.balance == 500
                    raise ValueError("Недостаточно средств на счете")

            with allure.step('Выполняем перевод'):
                from_account.balance -= amount
                to_account.balance += amount

            with allure.step('Сохраняем изменения'):
                session.commit()

        # ====================================================================== Тест
        with allure.step('Проверяем начальные балансы'):
            assert stan.balance == 1000
            assert bob.balance == 500

        try:
            with allure.step('Выполняем перевод 200 единиц от stan к bob'):
                transfer_money(db_session, from_account=stan.user,
                               to_account=bob.user, amount=200)

            with allure.step('Проверяем, что балансы изменились'):
                assert stan.balance == 800
                assert bob.balance == 700

        except Exception as e:
            with allure.step('Если произошла ошибка, откатываем транзакцию'):
                db_session.rollback()  # откат всех введеных нами изменений
            pytest.fail(f"Ошибка при переводе денег: {e}")

        finally:
            with allure.step("Удаляем данные для тестирования из базы"):
                db_session.delete(stan)
                db_session.delete(bob)
                # Фиксируем изменения в базе данных
                db_session.commit()

    @allure.title("Тест с перезапусками")
    @pytest.mark.flaky(reruns=3)
    def test_with_retries(delay_between_retries):
        with allure.step("Шаг 1: Проверка случайного значения"):
            result = random.choice([True, False])
            assert result, "Тест упал, потому что результат False"
