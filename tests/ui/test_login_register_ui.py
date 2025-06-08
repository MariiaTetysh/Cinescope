import time

import allure
import pytest
from playwright.sync_api import sync_playwright

from models.page_object_models import CinescopLoginPage, CinescopRegisterPage
from utils.data_generator import DataGenerator


@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Login")
@pytest.mark.ui
class TestloginPage:
    @allure.title("Проведение успешного входа в систему")
    def test_login_by_ui(self, registered_user):
        with sync_playwright() as playwright:
            # Запуск браузера headless=False для визуального отображения
            browser = playwright.chromium.launch(headless=False)
            page = browser.new_page()
            # Создаем объект страницы Login
            login_page = CinescopLoginPage(page)

            login_page.open()
            login_page.login(registered_user.email,
                             registered_user.password)  # Осуществяем вход

            # Проверка редиректа на домашнюю страницу
            login_page.assert_was_redirect_to_home_page()
            login_page.make_screenshot_and_attach_to_allure()  # Прикрепляем скриншот
            # Проверка появления и исчезновения алерта
            login_page.assert_allert_was_pop_up()

            # Пауза для визуальной проверки (нужно удалить в реальном тестировании)
            time.sleep(5)
            browser.close()


@allure.epic("Тестирование UI")
@allure.feature("Тестирование Страницы Register")
@pytest.mark.ui
class TestRegisterPage:
    @allure.title("Проведение успешной регистрации")
    def test_register_by_ui(self):
        with sync_playwright() as playwright:
            # Подготовка данных для регистрации
            random_email = DataGenerator.generate_random_email()
            random_name = DataGenerator.generate_random_name()
            random_password = DataGenerator.generate_random_password()

            # Запуск браузера headless=False для визуального отображения
            browser = playwright.chromium.launch(headless=False)
            page = browser.new_page()

            # Создаем объект страницы регистрации cinescope
            register_page = CinescopRegisterPage(page)
            register_page.open()
            # Выполняем регистрацию
            register_page.register(
                f"PlaywrightTest {random_name}", random_email, random_password, random_password)

            # Проверка редиректа на страницу /login
            register_page.assert_was_redirect_to_login_page()
            register_page.make_screenshot_and_attach_to_allure()  # Прикрепляем скриншот
            # Проверка появления и исчезновения алерта
            register_page.assert_allert_was_pop_up()

            # Пауза для визуальной проверки (нужно удалить в реальном тестировании)
            time.sleep(5)
            browser.close()
