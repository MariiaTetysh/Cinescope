from constants import VALID_MOVIE_ID
import pytest
from datetime import datetime


class TestMoviesAPI:

    @pytest.fixture
    def user(self, request):
        return request.getfixturevalue(request.param)

    @pytest.mark.slow
    def test_get_movie_posters_info(self, common_user):
        """
        Тест на получение полной информации об афишах фильмов.
        """
        response = common_user.api.movie_api.get_movie_posters_info()
        response_data = response.json()
        assert 'movies' in response_data, (
            'Список фильмов отсутствует в ответе'
        )
        assert 'count' in response_data, (
            'Количество афиш фильмов отсутствует в ответе'
        )
        assert response_data['count'] > 0, (
            'Количество афиш фильмов должно быть больше 0'
        )
        assert isinstance(response_data['count'], int), (
            '"count" должен быть целым числом'
        )
        assert isinstance(response_data['movies'], list), (
            '"movies" должен быть списком'
        )

    @pytest.mark.slow
    def test_pagination_movie_posters(self, common_user):
        """
        Тест на наличие пагинации на странице информации об афишах фильмов.
        """
        response = common_user.api.movie_api.get_movie_posters_info()
        response_data = response.json()
        assert 'page' in response_data, 'Поле "page" отсутствует'
        assert 'pageSize' in response_data, 'Поле "pageSize" отсутствует'
        assert 'pageCount' in response_data, 'Поле "pageCount" отсутствует'
        assert isinstance(response_data['page'], int), (
            '"page" должно быть целым числом'
        )
        assert isinstance(response_data['pageSize'], int), (
            '"pageSize" должно быть целым числом'
        )
        assert isinstance(response_data['pageCount'], int), (
            '"pageCount" должно быть целым числом'
        )
        assert response_data['page'] >= 1, (
            '"page" должно быть больше или равно 1'
        )
        assert response_data['pageSize'] >= 1, (
            '"pageSize" должно быть больше или равно 1'
        )
        assert response_data['pageCount'] >= 1, (
            '"pageCount" должно быть больше или равно 1'
        )

    @pytest.mark.slow
    def test_info_types_movie_posters(self, common_user):
        """
        Тест на проверку типов данных и структуры информации о фильмах.
        """
        response = common_user.api.movie_api.get_movie_posters_info()
        response_data = response.json()
        first_movie = response_data['movies'][0]
        assert 'movies' in response_data, 'Список фильмов отсутствует в ответе'
        assert isinstance(response_data['movies'], list), (
            '"movies" должен быть списком'
        )
        assert 'id' in first_movie, 'ID фильма отсутствует'
        assert 'name' in first_movie, 'Название фильма отсутствует'
        assert 'price' in first_movie, 'Цена фильма отсутствует'
        assert 'description' in first_movie, 'Описание фильма отсутствует'
        assert 'imageUrl' in first_movie, 'URL изображения отсутствует'
        assert 'location' in first_movie, 'Местоположение фильма отсутствует'
        assert 'published' in first_movie, 'Поле "published" отсутствует'
        assert 'genreId' in first_movie, 'ID жанра отсутствует'
        assert 'genre' in first_movie, 'Информация о жанре отсутствует'
        assert 'createdAt' in first_movie, 'Дата создания отсутствует'
        assert 'rating' in first_movie, 'Рейтинг отсутствует'

        assert isinstance(first_movie['id'], int), (
            'ID фильма должно быть целым числом'
        )
        assert isinstance(first_movie['name'], str), (
            'Название фильма должно быть строкой'
        )
        assert isinstance(first_movie['price'], int), (
            'Цена фильма должна быть целым числом'
        )
        assert isinstance(first_movie['description'], str), (
            'Описание фильма должно быть строкой'
        )
        assert isinstance(first_movie['imageUrl'], str), (
            'URL изображения должно быть строкой'
        )
        assert isinstance(first_movie['location'], str), (
            'Местоположение фильма должно быть строкой'
        )
        assert isinstance(first_movie['published'], bool), (
            'Поле "published" должно быть булевым'
        )
        assert isinstance(first_movie['genreId'], int), (
            'ID жанра должно быть целым числом'
        )
        assert isinstance(first_movie['genre'], dict), (
            'Информация о жанре должна быть словарем'
        )
        assert isinstance(first_movie['createdAt'], str), (
            'Дата создания должна быть строкой'
        )
        assert isinstance(first_movie['rating'], int), (
            'Рейтинг должен быть целым числом'
        )

        assert first_movie['price'] > 0, 'Цена должна быть положительной'
        assert 1 <= first_movie['rating'] <= 5, 'Рейтинг должен быть от 1 до 5'

    @pytest.mark.parametrize('param, value, expected_status', [
        ('genreId', 1, 200),
        ('genreId', 5, 200),
        ('locations', 'SPB', 200),
        ('locations', 'MSK', 200),
        ('page', 5, 200),
        ('pageSize', 5, 200),
        ('minPrice', 500, 200),
        ('maxPrice', 500, 200),
        # ('published', 'true', 200),
        # ('published', 'false', 200),

    ],
        ids=[
        'genreId=1', 'genreId=5', 'location=SPB', 'location=MSK', 'page=5',
        'pageSize=5', 'minPrice=1500', 'maxPrice=500',
        # 'published=True', 'published=False'
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
        )
        response_data = response.json()
        assert 'count' in response_data, (
            'Количество фильмов отсутствует в ответе'
        )
        assert response_data['count'] >= 0, (
            'Количество фильмов c учетом фильтра должно быть больше или равно 0'
        )
        if param == 'page' or param == 'pageSize':
            assert response_data[param] == params[param], (
                f'Неверный {param} для фильма '
            )
        for i in range(len(response_data['movies'])):
            if param == 'genreId' or param == 'published':
                assert response_data['movies'][i][param] == params[param], (
                    f'Неверный {param} для фильма '
                )
            if param == 'locations':
                assert response_data['movies'][i]['location'] == params[param], (
                    f'Неверный {param} для фильма '
                )
            if param == 'minPrice':
                assert response_data['movies'][i]['price'] >= params[param], (
                    f'Неверный {param} для фильма '
                )
            if param == 'maxPrice':
                assert response_data['movies'][i]['price'] <= params[param], (
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
        )
        response_data = response.json()

        if pageSize is not None:
            assert response_data['pageSize'] == pageSize
        if page is not None:
            assert response_data['page'] == page

        for movie in response_data['movies']:
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
                    movie['createdAt'] for movie in response_data['movies']
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
        response = super_admin.api.movie_api.add_movie(test_movie)
        response_data = response.json()
        movie_id = response_data['id']

        assert movie_id is not None, 'Идентификатор фильма не найден в ответе'
        assert 'createdAt' in response_data, 'Поле "createdAt" отсутствует'
        assert response_data['name'] == test_movie['name'], (
            'Заданное имя не совпадает'
        )
        assert response_data['price'] == test_movie['price'], (
            'Заданная цена не совпадает'
        )
        assert response_data['published'], (
            'Фильм должен быть опубликован после создания'
        )

        response = super_admin.api.movie_api.get_movies_info(movie_id)
        response_data = response.json()
        assert response_data['location'] == test_movie['location'], (
            'Заданное местоположение не совпадает'
        )
        assert response_data['description'] == test_movie['description'], (
            'Заданное описание не совпадает'
        )

    def test_add_movie_with_min_values(
        self, super_admin, test_movie_min_values
    ):
        """
        Тест на создание фильма с минимальным набором обязательных полей.
        """
        response = super_admin.api.movie_api.add_movie(test_movie_min_values)
        response_data = response.json()
        movie_id = response_data['id']

        assert movie_id is not None, 'Идентификатор фильма не найден в ответе'
        assert 'createdAt' in response_data, 'Поле "createdAt" отсутствует'
        assert response_data['imageUrl'] is None, (
            'Заданная ссылка фотографии не совпадает'
        )
        assert response_data['name'] == test_movie_min_values['name'], (
            'Заданное имя не совпадает'
        )
        assert response_data['price'] == test_movie_min_values['price'], (
            'Заданная цена не совпадает'
        )
        assert response_data['published'], (
            'Фильм должен быть опубликован после создания'
        )

        response = super_admin.api.movie_api.get_movies_info(movie_id)
        response_data = response.json()
        assert response_data['imageUrl'] is None, (
            'Заданная ссылка фотографии не совпадает'
        )
        assert response_data[
            'location'
        ] == test_movie_min_values['location'], (
            'Заданное местоположение не совпадает'
        )
        assert response_data[
            'description'
        ] == test_movie_min_values['description'], (
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
