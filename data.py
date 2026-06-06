"""Тестовые данные для API тестов"""


class OrderTestData:
    """Тестовые данные для создания заказов"""

    ORDER_BLACK = {
        "firstName": "Александр",
        "lastName": "Пушкин",
        "address": "Москва, ул. Тверская, 15",
        "metroStation": 7,
        "phone": "+7 916 123 45 67",
        "rentTime": 3,
        "deliveryDate": "2024-12-25",
        "comment": "Тестовый заказ BLACK",
        "color": ["BLACK"]
    }

    ORDER_GREY = {
        "firstName": "Лев",
        "lastName": "Толстой",
        "address": "Москва, ул. Пятницкая, 25",
        "metroStation": 9,
        "phone": "+7 925 987 65 43",
        "rentTime": 5,
        "deliveryDate": "2024-12-29",
        "comment": "Тестовый заказ GREY",
        "color": ["GREY"]
    }

    ORDER_BOTH_COLORS = {
        "firstName": "Фёдор",
        "lastName": "Достоевский",
        "address": "Москва, ул. Воздвиженка, 15",
        "metroStation": 2,
        "phone": "+7 903 111 22 33",
        "rentTime": 4,
        "deliveryDate": "2024-12-27",
        "comment": "Тестовый заказ BLACK + GREY",
        "color": ["BLACK", "GREY"]
    }

    ORDER_NO_COLOR = {
        "firstName": "Николай",
        "lastName": "Гоголь",
        "address": "Москва, Никитский бульвар, 12",
        "metroStation": 1,
        "phone": "+7 909 444 55 66",
        "rentTime": 2,
        "deliveryDate": "2024-12-24",
        "comment": "Тестовый заказ без цвета",
        "color": []
    }

    ALL_ORDERS = [ORDER_BLACK, ORDER_GREY, ORDER_BOTH_COLORS, ORDER_NO_COLOR]


# Данные для проверки валидации
INCOMPLETE_COURIER_DATA = [
    ({"login": "test_login", "password": "test_pass"}, "firstName"),
    ({"login": "test_login", "firstName": "Тест"}, "password"),
    ({"password": "test_pass", "firstName": "Тест"}, "login"),
]