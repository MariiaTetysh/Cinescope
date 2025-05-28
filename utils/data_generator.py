import random
import string
import time

from faker import Faker

faker = Faker()


class DataGenerator:

    @staticmethod
    def generate_random_email():
        """
        Генерация случайного email.
        """
        random_string = ''.join(
            random.choices(string.ascii_lowercase + string.digits, k=8)
        )
        return f'kek{random_string}@gmail.com'

    @staticmethod
    def generate_random_name():
        """
        Генерация случайного имени и фамилии.
        """
        return f'{faker.first_name()} {faker.last_name()}'

    @staticmethod
    def generate_random_film_name():
        """
        Генерация случайного названия фильма.
        """
        themes = [
            f"Return to {faker.city()}",
            f"The last {faker.job().split()[0]}",
            f"{faker.first_name()} and {faker.first_name()}",
            f"Back to {faker.country()}",
            f"{faker.color_name()} {faker.word(part_of_speech='noun')}"
        ]
        timestamp = int(time.time() * 1000)
        return f'{random.choice(themes)} {timestamp}'

    @staticmethod
    def generate_random_price():
        """
        Генерация случайной цены фильма.
        """
        return faker.random_int(min=100, max=1000)

    @staticmethod
    def generate_random_password():
        """
        Генерация пароля, соответствующего требованиям:
        - Минимум 1 буква.
        - Минимум 1 цифра.
        - Допустимые символы.
        - Длина от 8 до 20 символов.
        """
        # Гарантируем наличие хотя бы одной буквы и одной цифры
        letters = random.choice(string.ascii_letters)  # Одна буква
        digits = random.choice(string.digits)  # Одна цифра

        # Дополняем пароль случайными символами из допустимого набора
        special_chars = "?@#$%^&*|:"
        all_chars = string.ascii_letters + string.digits + special_chars
        remaining_length = random.randint(6, 18)  # Остальная длина пароля
        remainig_chars = ''.join(random.choices(all_chars, k=remaining_length))

        # Перемешиваем пароль для рандомизации
        password = list(letters + digits + remainig_chars)
        random.shuffle(password)

        return ''.join(password)
