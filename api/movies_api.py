from constants import BASE_URL_MOVIES_API, MOVIES_ENDPOINT
from custom_requester.custom_requester import CustomRequester


class MoviesAPI(CustomRequester):
    def __init__(self, session, base_url):
        super().__init__(session, base_url=BASE_URL_MOVIES_API)

    def get_movie_posters_info(self, expected_status=200, params=None):
        """
        Получение информации об афише фильмов.
        :param expected_status: Ожидаемый статус-код.
        :param params: Фильтр для запроса.
        """
        return self.send_request(
            method="GET",
            endpoint=MOVIES_ENDPOINT,
            expected_status=expected_status,
            params=params
        )

    def add_movie(self, movie_data, expected_status=201, headers=None):
        """
        Создание фильма.
        :param movie_data: Данные фильма.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=MOVIES_ENDPOINT,
            data=movie_data,
            expected_status=expected_status,
            headers=headers
        )

    def get_movies_info(self, movie_id, expected_status=201):
        """
        Получение информации о фильме.
        :param movie_id: ID фильма.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="GET",
            endpoint=f'{MOVIES_ENDPOINT}/{movie_id}',
            expected_status=expected_status
        )

    def delete_movies_info(self, movie_id, expected_status=200, token=None):
        """
        Удаление фильма.
        :param movie_id: ID фильма.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="DELETE",
            endpoint=f'{MOVIES_ENDPOINT}/{movie_id}',
            expected_status=expected_status,
            token=token
        )

    def partial_update_movies_info(
        self, movie_id, movie_update_data, expected_status=200
    ):
        """
        Частичное изменение информации о фильме.
        :param movie_id: ID фильма.
        :param movie_update_data: Данные фильма для изменения информации.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="PATCH",
            endpoint=f'{MOVIES_ENDPOINT}/{movie_id}',
            data=movie_update_data,
            expected_status=expected_status
        )
