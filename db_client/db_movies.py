import psycopg2

from resources.db_creds import DBCreds


def connect_to_postgres():
    """Функция для подключения к PostgreSQL базе данных"""
    connection = None
    cursor = None

    try:
        # Подключение к базе данных
        connection = psycopg2.connect(
            dbname=DBCreds.DB_NAME,
            user=DBCreds.DB_USER,
            password=DBCreds.DB_PASSWORD,
            host=DBCreds.DB_HOST,
            port=DBCreds.DB_PORT
        )

        print("Подключение успешно установлено")

        # Создание курсора
        cursor = connection.cursor()

        # Вывод информации о PostgreSQL сервере
        print("Информация о сервере PostgreSQL:")
        print(connection.get_dsn_parameters(), "\n")

        # Выполнение SQL-запроса
        cursor.execute("SELECT version();")

        # Получение результата
        record = cursor.fetchone()
        print("Вы подключены к - ", record, "\n")

    except Exception as error:
        print("Ошибка при работе с PostgreSQL:", error)

    finally:
        # Закрытие соединения с базой данных
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("Соединение с PostgreSQL закрыто")


if __name__ == "__main__":
    connect_to_postgres()
