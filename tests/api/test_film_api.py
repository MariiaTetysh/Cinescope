from constants import VALID_MOVIE_ID


class TestMoviesAPI:

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

    def test_get_movie_posters_info_with_filter(self, common_user):
        """
        Тест на получение информации об афишах фильмов с фильтром "genreId".
        """
        params = {'genreId': 1}
        response = common_user.api.movie_api.get_movie_posters_info(
            params=params
        )
        response_data = response.json()
        assert 'count' in response_data, (
            'Количество фильмов отсутствует в ответе'
        )
        assert response_data['count'] >= 0, (
            'Количество фильмов с genreId = 1 должно быть больше или равно 0'
        )
        for i in range(len(response_data['movies'])):    
            assert response_data['movies'][i]['genreId'] == params['genreId'], (
                'Неверный genreId для фильма '
            )

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

    def test_delete_movies_info(
        self, super_admin, test_movie
    ):
        """
        Тест на удаление фильма с валидным ID.
        """
        response = super_admin.api.movie_api.add_movie(test_movie)
        movie_id = response.json()['id']
        response = super_admin.api.movie_api.delete_movies_info(movie_id)
        response_data = response.json()

        response = super_admin.api.movie_api.get_movies_info(
            movie_id, expected_status=404
        )
        response_data = response.json()
        assert 'message' in response_data, (
            'Сообщения об ошибке нет в ответе'
        )
        assert response_data['message'] == 'Фильм не найден', (
            'Нет подтверждения удаления фильма'
        )
        assert response_data['error'] == 'Not Found', (
            'Нет подтверждения удаления фильма'
        )

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
