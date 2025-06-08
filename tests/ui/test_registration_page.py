import time

from playwright.sync_api import Page, expect

from utils.data_generator import DataGenerator


def test_registration(page: Page):
    page.goto('https://dev-cinescope.coconutqa.ru/register')

    username_locator = '[data-qa-id="register_full_name_input"]'
    email_locator = '[data-qa-id="register_email_input"]'
    password_locator = '[data-qa-id="register_password_input"]'
    repeat_password_locator = '[data-qa-id="register_password_repeat_input"]'

    random_username = DataGenerator.generate_random_name()
    random_email = DataGenerator.generate_random_email()
    random_password = DataGenerator.generate_random_password()

    page.fill(username_locator, random_username)
    page.fill(email_locator, random_email)
    page.fill(password_locator, random_password)
    page.fill(repeat_password_locator, random_password)

    page.click('[data-qa-id="register_submit_button"]')

    page.wait_for_url('https://dev-cinescope.coconutqa.ru/login')
    expect(page.get_by_text("Подтвердите свою почту")).to_be_visible(
        visible=True
    )


def test_registration_with_codegen(page: Page):
    page.goto("https://dev-cinescope.coconutqa.ru/register")
    page.get_by_role("textbox", name="Имя Фамилия Отчество").fill(
        "Иван Иванов")
    page.get_by_role("textbox", name="Email").fill("iv1iv@mail.ru")
    page.get_by_role("textbox", name="Пароль", exact=True).fill("ivanoviv1997")
    page.get_by_role("textbox", name="Повторите пароль").fill("ivanoviv1997")

    time.sleep(10)
    page.get_by_role("button", name="Зарегистрироваться").click()

    page.wait_for_url('https://dev-cinescope.coconutqa.ru/login')
    expect(page.get_by_text("Подтвердите свою почту")).to_be_visible(
        visible=True
    )
