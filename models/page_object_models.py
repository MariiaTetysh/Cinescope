# Modul_4\Cinescope\models\page_object_models.py
import allure
from playwright.sync_api import Page

# class CinescopRegisterPage:
#     def __init__(self, page: Page):
#         self.page = page
#         self.url = "https://dev-cinescope.coconutqa.ru/register"

#         # Локаторы элементов
#         self.home_button = "a[href='/' and text()='Cinescope']"
#         self.all_movies_button = "a[href='/movies' and text()='Все фильмы']"

#         self.full_name_input = "input[name='fullName']"
#         self.email_input = "input[name='email']"
#         self.password_input = "input[name='password']"
#         self.repeat_password_input = "input[name='passwordRepeat']"

#         self.register_button = "button[data-qa-id='register_submit_button']"
#         self.sign_button = "a[href='/login' and text()='Войти']"

#     # Шапка страницы
#     def go_to_home_page(self):
#         """Переход на главную страницу."""
#         self.page.click(self.home_button)
#         # Ожидание загрузки главной страницы
#         self.page.wait_for_url("https://dev-cinescope.coconutqa.ru/")

#     def go_to_all_movies(self):
#         """Переход на страницу 'Все фильмы'."""
#         self.page.click(self.all_movies_button)
#         # Ожидание загрузки страницы
#         self.page.wait_for_url("https://dev-cinescope.coconutqa.ru/movies")

#     # Тело страницы
#     def open(self):
#         """Переход на страницу регистрации."""
#         self.page.goto(self.url)

#     def enter_full_name(self, full_name: str):
#         """Ввод full_name"""
#         self.page.fill(self.full_name_input, full_name)

#     def enter_email(self, email: str):
#         """Ввод email"""
#         self.page.fill(self.email_input, email)

#     def enter_password(self, password: str):
#         """Ввод пароля"""
#         self.page.fill(self.password_input, password)

#     def enter_repeat_password(self, password: str):
#         """Ввод подтверждения пароля"""
#         self.page.fill(self.repeat_password_input, password)

#     def click_register_button(self):
#         """Клик по кнопке регистрации"""
#         self.page.click(self.register_button)

#     # Вспомогательные action методы
#     def register(self, full_name: str, email: str, password: str, confirm_password: str):
#         """Полный процесс регистрации."""
#         self.enter_full_name(full_name)
#         self.enter_email(email)
#         self.enter_password(password)
#         self.enter_repeat_password(confirm_password)
#         self.click_register_button()

#     def wait_redirect_to_login_page(self):
#         """Переход на страницу login."""
#         self.page.wait_for_url(
#             "https://dev-cinescope.coconutqa.ru/login")  # Ожидание загрузки страницы login
#         assert self.page.url == "https://dev-cinescope.coconutqa.ru/login", "Редирект на домашнюю старницу не произошел"

#     def check_allert(self):
#         """Проверка всплывающего сообщения после редиректа"""
#         # Проверка появления алерта с текстом "Подтвердите свою почту"
#         notification_locator = self.page.get_by_text("Подтвердите свою почту")
#         notification_locator.wait_for(
#             state="visible")  # Ждем появления элемента

#         assert notification_locator.is_visible(), "Уведомление не появилось"
#         # Ожидание исчезновения алерта
#         # Ждем, пока алерт исчезнет
#         notification_locator.wait_for(state="hidden")
#         assert notification_locator.is_visible() == False, "Уведомление исчезло"


# class CinescopLoginPage:
#     def __init__(self, page: Page):
#         self.page = page
#         self.url = "https://dev-cinescope.coconutqa.ru/login"

#         # Локаторы элементов
#         self.home_button = "a[href='/' and text()='Cinescope']"
#         self.all_movies_button = "a[href='/movies' and text()='Все фильмы']"

#         self.email_input = "input[name='email']"
#         self.password_input = "input[name='password']"

#         self.login_button = "button[data-qa-id='login_submit_button']"
#         self.register_button = "a[href='/register' and text()='Зарегистрироваться']"

#      # Обработчики локаторов на шапке страницы
#     def go_to_home_page(self):
#         """Переход на главную страницу"""
#         self.page.click(self.home_button)
#         # Ожидание загрузки главной страницы
#         self.page.wait_for_url("https://dev-cinescope.coconutqa.ru/")

#     def go_to_all_movies(self):
#         """Переход на страницу 'Все фильмы'"""
#         self.page.click(self.all_movies_button)
#         # Ожидание загрузки страницы
#         self.page.wait_for_url("https://dev-cinescope.coconutqa.ru/movies")

#     # Обработчики локаторов на теле страницы
#     def open(self):
#         """Переход на страницу входа"""
#         self.page.goto(self.url)

#     def enter_email(self, email: str):
#         """Ввод email"""
#         self.page.fill(self.email_input, email)

#     def enter_password(self, password: str):
#         """Ввод пароля"""
#         self.page.fill(self.password_input, password)

#     def click_login_button(self):
#         """Клик по кнопке входа"""
#         self.page.click(self.login_button)

#     # Вспомогательные action методы
#     def login(self, email: str, password: str):
#         """Полный процесс входа"""
#         self.enter_email(email)
#         self.enter_password(password)
#         self.click_login_button()

#     def wait_redirect_to_home_page(self):
#         """Ожидание перехода на домашнюю страницу"""
#         self.page.wait_for_url(
#             "https://dev-cinescope.coconutqa.ru/")  # Ожидание загрузки домашней страницы
#         assert self.page.url == "https://dev-cinescope.coconutqa.ru/", "Редирект на домашнюю старницу не произошел"

#     def check_allert(self):
#         """Проверка всплывающего сообщения после редиректа"""
#         # Проверка появления алерта с текстом "Вы вошли в аккаунт"
#         notification_locator = self.page.get_by_text("Вы вошли в аккаунт")
#         notification_locator.wait_for(
#             state="visible")  # Ждем появления элемента
#         assert notification_locator.is_visible(), "Уведомление не появилось"

#         # Ожидание исчезновения алерта
#         # Ждем, пока алерт исчезнет
#         notification_locator.wait_for(state="hidden")
#         assert notification_locator.is_visible() == False, "Уведомление исчезло"


class PageAction:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Переход на страницу: {url}")
    def open_url(self, url: str):
        self.page.goto(url)

    @allure.step("Ввод текста '{text}' в поле '{locator}'")
    def enter_text_to_element(self, locator: str, text: str):
        self.page.fill(locator, text)

    @allure.step("Клик по элементу '{locator}'")
    def click_element(self, locator: str):
        self.page.click(locator)

    @allure.step("Ожидание загрузки страницы: {url}")
    def wait_redirect_for_url(self, url: str):
        self.page.wait_for_url(url)
        assert self.page.url == url, "Редирект на домашнюю старницу не произошел"

    @allure.step("Получение текста элемента: {locator}")
    def get_element_text(self, locator: str) -> str:
        return self.page.locator(locator).text_content()

    @allure.step("Ожидание появления или исчезновения элемента: {locator}, state = {state}")
    def wait_for_element(self, locator: str, state: str = "visible"):
        self.page.locator(locator).wait_for(state=state)

    @allure.step("Скриншот текущей страиницы")
    def make_screenshot_and_attach_to_allure(self):
        screenshot_path = "screenshot.png"
        # full_page=True для скриншота всей страницы
        self.page.screenshot(path=screenshot_path, full_page=True)

        # Прикрепление скриншота к Allure-отчёту
        with open(screenshot_path, "rb") as file:
            allure.attach(file.read(), name="Screenshot after redirect",
                          attachment_type=allure.attachment_type.PNG)

    @allure.step("Проверка всплывающего сообщения c текстом: {text}")
    def check_pop_up_element_with_text(self, text: str) -> bool:
        with allure.step("Проверка появления алерта с текстом: '{text}'"):
            notification_locator = self.page.get_by_text(text)
            # Ждем появления элемента
            notification_locator.wait_for(state="visible")
            assert notification_locator.is_visible(), "Уведомление не появилось"

        with allure.step("Проверка исчезновения алерта с текстом: '{text}'"):
            # Ждем, пока алерт исчезнет
            notification_locator.wait_for(state="hidden")
            assert notification_locator.is_visible() == False, "Уведомление не исчезло"


class BasePage(PageAction):  # Базовая логика доспустимая для всех страниц на сайте
    def __init__(self, page: Page):
        super().__init__(page)
        self.home_url = "https://dev-cinescope.coconutqa.ru/"

        # Общие локаторы для всех страниц на сайте
        self.home_button = "a[href='/' and text()='Cinescope']"
        self.all_movies_button = "a[href='/movies' and text()='Все фильмы']"

    @allure.step("Переход на главную страницу, из шапки сайта")
    def go_to_home_page(self):
        self.click_element(self.home_button)
        self.wait_redirect_for_url(self.home_url)

    @allure.step("Переход на страницу 'Все фильмы, из шапки сайта'")
    def go_to_all_movies(self):
        self.click_element(self.all_movies_button)
        self.wait_redirect_for_url(f"{self.home_url}movies")


class CinescopRegisterPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}register"

        # Локаторы элементов
        self.full_name_input = "input[name='fullName']"
        self.email_input = "input[name='email']"
        self.password_input = "input[name='password']"
        self.repeat_password_input = "input[name='passwordRepeat']"

        self.register_button = "button[data-qa-id='register_submit_button']"
        self.sign_button = "a[href='/login' and text()='Войти']"

    # Локальные action методы
    def open(self):
        self.open_url(self.url)

    def register(self, full_name: str, email: str, password: str, confirm_password: str):
        self.enter_text_to_element(self.full_name_input, full_name)
        self.enter_text_to_element(self.email_input, email)
        self.enter_text_to_element(self.password_input, password)
        self.enter_text_to_element(
            self.repeat_password_input, confirm_password)

        self.click_element(self.register_button)

    def assert_was_redirect_to_login_page(self):
        self.wait_redirect_for_url(f"{self.home_url}login")

    def assert_allert_was_pop_up(self):
        self.check_pop_up_element_with_text("Подтвердите свою почту")


class CinescopLoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.url = f"{self.home_url}login"

        # Локаторы элементов
        self.email_input = "input[name='email']"
        self.password_input = "input[name='password']"

        self.login_button = "button[data-qa-id='login_submit_button']"
        self.register_button = "a[href='/register' and text()='Зарегистрироваться']"

    # Локальные action методы
    def open(self):
        self.open_url(self.url)

    def login(self, email: str, password: str):
        self.enter_text_to_element(self.password_input, password)
        self.enter_text_to_element(self.email_input, email)
        self.click_element(self.login_button)

    def assert_was_redirect_to_home_page(self):
        self.wait_redirect_for_url(self.home_url)

    def assert_allert_was_pop_up(self):
        self.check_pop_up_element_with_text("Вы вошли в аккаунт")
