from constants import BASE_URL_AUTH, LOGIN_ENDPOINT, REGISTER_ENDPOINT
from custom_requester.custom_requester import CustomRequester


class AuthAPI(CustomRequester):
    def __init__(self, session):
        super().__init__(session=session, base_url=BASE_URL_AUTH)

    def register_user(self, user_data, expected_status=201):
        """
        Регистрация нового пользователя.
        :param user_data: Данные пользователя.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=REGISTER_ENDPOINT,
            data=user_data,
            expected_status=expected_status
        )

    def login_user(self, login_data, expected_status=201):
        """
        Авторизация пользователя.
        :param login_data: Данные для логина.
        :param expected_status: Ожидаемый статус-код.
        """
        return self.send_request(
            method="POST",
            endpoint=LOGIN_ENDPOINT,
            data=login_data,
            expected_status=expected_status
        )

    # def authenticate(self, user_creds):  #для использования до ролевой модели
    #     login_data = {
    #         "email": user_creds['email'],
    #         "password": user_creds['password']
    #     }

    #     response = self.login_user(login_data).json()
    #     if "accessToken" not in response:
    #         raise KeyError("token is missing")

    #     token = response["accessToken"]
    #     self._update_session_headers(Authorization=f"Bearer {token}")
    #     return response

    def authenticate(self, user_creds):
        # для использования ролевой модели и параметризации
        login_data = {
            "email": user_creds[0],
            "password": user_creds[1]
        }

        response = self.login_user(login_data).json()
        if "accessToken" not in response:
            raise KeyError("token is missing")

        token = response["accessToken"]
        self._update_session_headers(Authorization=f"Bearer {token}")
        return response
