from constants import BASE_URL_MOVIES_API, LOGIN_ENDPOINT, REGISTER_ENDPOINT
from custom_requester.custom_requester import CustomRequester

class MoviesAPI(CustomRequester):
    def __init__(self, session, BASE_URL_MOVIES_API):
        super().__init__(session, base_url=BASE_URL_MOVIES_API)