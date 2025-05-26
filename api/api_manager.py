from api.auth_api import AuthAPI
from api.movies_api import MoviesAPI
from api.user_api import UserAPI


class ApiManager:
    """
    Класс для управления API-классами с единой HTTP-сессией.
    """

    def __init__(self, session, base_url):
        """
        Инициализация ApiManager.
        :param session: HTTP-сессия, используемая всеми API-классами.
        :param base_url: URL, используемый всеми API-классами.
        """
        self.session = session
        self.auth_api = AuthAPI(session)
        self.user_api = UserAPI(session, base_url)
        self.movie_api = MoviesAPI(session, base_url)
