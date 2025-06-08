from datetime import datetime

import pytest

from constants import VALID_MOVIE_ID
from models.model import Movie, MovieCreation


class TestMoviesAPI:

    @pytest.fixture
    def user(self, request):
        return request.getfixturevalue(request.param)

    @pytest.mark.slow
    def test_pagination_movie_posters(self, common_user):
        """
        Тест на наличие пагинации на странице информации об афишах фильмов.
        """
        response = common_user.api.movie_api.get_movie_posters_info().json()
        assert 'page' in response, 'Поле "page" отсутствует'
        assert 'pageSize' in response, 'Поле "pageSize" отсутствует'
        assert 'pageCount' in response, 'Поле "pageCount" отсутствует'
        assert isinstance(response['page'], int), (
            '"page" должно быть целым числом'
        )
        assert isinstance(response['pageSize'], int), (
            '"pageSize" должно быть целым числом'
        )
        assert isinstance(response['pageCount'], int), (
            '"pageCount" должно быть целым числом'
        )
        assert response['page'] >= 1, (
            '"page" должно быть больше или равно 1'
        )
        assert response['pageSize'] >= 1, (
            '"pageSize" должно быть больше или равно 1'
        )
        assert response['pageCount'] >= 1, (
            '"pageCount" должно быть больше или равно 1'
        )

    @pytest.mark.slow
    def test_info_and_types_movie_posters(self, common_user):
        """
        Тест на получение полной информации об афишах фильмов и
        проверку типов данных и структуры информации о фильмах.
        """
        response = common_user.api.movie_api.get_movie_posters_info().json()
        assert 'movies' in response, (
            'Список фильмов отсутствует в ответе'
        )
        assert 'count' in response, (
            'Количество афиш фильмов отсутствует в ответе'
        )
        assert response['count'] > 0, (
            'Количество афиш фильмов должно быть больше 0'
        )
        assert isinstance(response['count'], int), (
            '"count" должен быть целым числом'
        )
        assert isinstance(response['movies'], list), (
            '"movies" должен быть списком'
        )
        for movie in response['movies']:
            Movie(**movie)

    @pytest.mark.parametrize('param, value, expected_status', [
        ('genreId', 1, 200),
        ('genreId', 5, 200),
        ('locations', 'SPB', 200),
        ('locations', 'MSK', 200),
        ('page', 5, 200),
        ('pageSize', 5, 200),
        ('minPrice', 500, 200),
        ('maxPrice', 1500, 200)
    ],
        ids=[
        'genreId=1', 'genreId=5', 'location=SPB', 'location=MSK', 'page=5',
        'pageSize=5', 'minPrice=500', 'maxPrice=1500'
    ])
    def test_get_movie_posters_info_with_filter(
        self, param, value, common_user, expected_status
    ):
        """
        Тест на получение информации об афишах фильмов с одинарными фильтрами.
        """
        params = {param: value}
        response = common_user.api.movie_api.get_movie_posters_info(
            params=params, expected_status=expected_status
        ).json()
        for movie in response['movies']:
            Movie(**movie)
        assert 'count' in response, (
            'Количество фильмов отсутствует в ответе'
        )
        assert response['count'] >= 0, (
            'Количество фильмов c учетом фильтра должно быть больше или равно 0'
        )
        if param == 'page' or param == 'pageSize':
            assert response[param] == params[param], (
                f'Неверный {param} для фильма '
            )
        for i in range(len(response['movies'])):
            if param == 'genreId' or param == 'published':
                assert response['movies'][i][param] == params[param], (
                    f'Неверный {param} для фильма '
                )
            if param == 'locations':
                assert response['movies'][i]['location'] == params[param], (
                    f'Неверный {param} для фильма '
                )
            if param == 'minPrice':
                assert response['movies'][i]['price'] >= params[param], (
                    f'Неверный {param} для фильма '
                )
            if param == 'maxPrice':
                assert response['movies'][i]['price'] <= params[param], (
                    f'Неверный {param} для фильма '
                )

    @pytest.mark.parametrize(
        'pageSize, page, minPrice, maxPrice, '
        'locations, published, genreId, createdAt, expected_status', [
            (None, None, 100, 500, 'MSK', None, 1, None, 200),
            (15, 1, 500, 1000, 'SPB', 1, 2, 'asc', 200),
            (None, None, None, None, None, None, None, None, 200)
        ],
        ids=[
            'composite_filter',
            'composite_filter_with_all_data',
            'composite_filter_with_no_data'
        ])
    def test_get_movie_posters_info_with_composite_filter(
        self, pageSize, page, minPrice, maxPrice, locations, published,
        genreId, createdAt, common_user, expected_status
    ):
        """
        Тест на получение информации об афишах фильмов с составными фильтрами.
        """
        params = {
            'pageSize': pageSize,
            'page': page,
            'minPrice': minPrice,
            'maxPrice': maxPrice,
            'locations': locations,
            'published': published,
            'genreId': genreId,
            'createdAt': createdAt,
        }
        response = common_user.api.movie_api.get_movie_posters_info(
            params=params, expected_status=expected_status
        ).json()

        if pageSize is not None:
            assert response['pageSize'] == pageSize
        if page is not None:
            assert response['page'] == page

        for movie in response['movies']:
            Movie(**movie)
            if minPrice is not None:
                assert movie['price'] >= minPrice
            if maxPrice is not None:
                assert movie['price'] <= maxPrice
            if locations is not None:
                assert movie['location'] == locations
            if published is not None:
                assert movie['published'] == published
            if genreId is not None:
                assert movie['genreId'] == genreId
            if createdAt is not None:
                dates = [
                    movie['createdAt'] for movie in response['movies']
                ]
                parsed_dates = [datetime.fromisoformat(
                    date.replace('Z', '+00:00')
                ) for date in dates]

                if createdAt == 'asc':
                    assert parsed_dates == sorted(parsed_dates), (
                        "Даты не отсортированы по возрастанию!"
                    )
                elif createdAt == 'desc':
                    assert parsed_dates == sorted(
                        parsed_dates, reverse=True
                    ), ("Даты не отсортированы по убыванию!")

    def test_add_movie(self, super_admin, test_movie):
        """
        Тест на создание фильма с валидными данными.
        """
        response = super_admin.api.movie_api.add_movie(
            test_movie
        ).json()
        movie = Movie(**response)
        movie_id = movie.id

        assert movie.name == test_movie['name'], (
            'Заданное имя не совпадает'
        )
        assert movie.price == test_movie['price'], (
            'Заданная цена не совпадает'
        )
        assert movie.published, (
            'Фильм должен быть опубликован после создания'
        )

        response = super_admin.api.movie_api.get_movies_info(movie_id).json()
        movie = Movie(**response)
        assert movie.location == test_movie['location'], (
            'Заданное местоположение не совпадает'
        )
        assert movie.description == test_movie['description'], (
            'Заданное описание не совпадает'
        )

    def test_add_movie_with_min_values(
        self, super_admin, test_movie_min_values
    ):
        """
        Тест на создание фильма с минимальным набором обязательных полей.
        """
        response = super_admin.api.movie_api.add_movie(
            test_movie_min_values
        ).json()
        movie = Movie(**response)
        movie_id = movie.id

        assert movie.name == test_movie_min_values['name'], (
            'Заданное имя не совпадает'
        )
        assert movie.price == test_movie_min_values['price'], (
            'Заданная цена не совпадает'
        )
        assert movie.published, (
            'Фильм должен быть опубликован после создания'
        )

        response = super_admin.api.movie_api.get_movies_info(movie_id).json()
        movie = Movie(**response)
        assert movie.location == test_movie_min_values['location'], (
            'Заданное местоположение не совпадает'
        )
        assert movie.description == test_movie_min_values['description'], (
            'Заданное описание не совпадает'
        )

    @pytest.mark.parametrize(
        'user, expected_status_delete, expected_status_get', [
            (('super_admin'), 200, 404),
            (('admin'), 200, 404),
            (('common_user'), 403, 200),
        ],
        indirect=['user'],
        ids=[
            "SuperAdmin", "Admin", "Common User"
        ]
    )
    def test_delete_movies_info(
        self, user, test_movie, super_admin,
        expected_status_delete, expected_status_get
    ):
        """
        Тест на удаление фильма с валидным ID.
        """
        response = super_admin.api.movie_api.add_movie(test_movie)
        movie_id = response.json()['id']
        response = user.api.movie_api.delete_movies_info(
            movie_id, expected_status_delete
        )
        response_data = response.json()

        response = user.api.movie_api.get_movies_info(
            movie_id, expected_status_get
        )
        response_data = response.json()
        if response.status_code == 404:
            assert 'message' in response_data, (
                'Сообщения об ошибке нет в ответе'
            )
            assert response_data['message'] == 'Фильм не найден', (
                'Нет подтверждения удаления фильма'
            )
            assert response_data['error'] == 'Not Found', (
                'Нет подтверждения удаления фильма'
            )

    @pytest.mark.slow
    def test_get_movies_info(self, common_user):
        """
        Тест на получение информации о фильме с валидным Id.
        """
        response = common_user.api.movie_api.get_movies_info(
            movie_id=VALID_MOVIE_ID
        )
        response_data = response.json()
        assert response_data['id'] == VALID_MOVIE_ID, (
            'Заданный Id фильма не совпадает'
        )
        assert 'name' in response_data, (
            'Название фильма отсутствует в ответе'
        )
        assert 'price' in response_data, (
            'Цена фильма отсутствует в ответе'
        )

    def test_partial_update_movies_info(self, test_movie, super_admin):
        """
        Тест на частичное изменение информации о фильме.
        """
        updated_data = {
            "price": 1500
        }
        response = super_admin.api.movie_api.add_movie(test_movie)
        movie_id = response.json()['id']
        response = super_admin.api.movie_api.partial_update_movies_info(
            movie_id, updated_data
        )
        response_data = response.json()
        assert response_data['price'] == updated_data['price'], (
            'Заданная цена не изменилась'
        )
        assert response_data['name'] == test_movie['name'], (
            'Заданное название изменилось'
        )

    def test_add_movie_with_invalid_role(self, common_user, test_movie):
        """
        Тест на создание фильма с валидными данными и невалидной ролью - USER.
        """
        response = common_user.api.movie_api.add_movie(
            test_movie, expected_status=403
        )
        response_data = response.json()

        assert 'message' in response_data, (
            'Поле "message" отсутствует в ответе'
        )
        assert response_data['message'] == 'Forbidden resource', (
            'Значение поля "message" не равняется "Forbidden resource"'
        )
