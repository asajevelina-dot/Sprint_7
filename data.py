"""Тестовые данные для API тестов"""


class OrderTestData:
    """Тестовые данные для создания заказов - все цвета"""

    ALL_ORDERS = [
        {  # BLACK
            "firstName": "Александр",
            "lastName": "Пушкин",
            "address": "Москва, ул. Тверская, 15",
            "metroStation": 7,
            "phone": "+7 916 123 45 67",
            "rentTime": 3,
            "deliveryDate": "2024-12-25",
            "comment": "Тестовый заказ BLACK",
            "color": ["BLACK"]
        },
        {  # GREY
            "firstName": "Лев",
            "lastName": "Толстой",
            "address": "Москва, ул. Пятницкая, 25",
            "metroStation": 9,
            "phone": "+7 925 987 65 43",
            "rentTime": 5,
            "deliveryDate": "2024-12-29",
            "comment": "Тестовый заказ GREY",
            "color": ["GREY"]
        },
        {  # BOTH
            "firstName": "Фёдор",
            "lastName": "Достоевский",
            "address": "Москва, ул. Воздвиженка, 15",
            "metroStation": 2,
            "phone": "+7 903 111 22 33",
            "rentTime": 4,
            "deliveryDate": "2024-12-27",
            "comment": "Тестовый заказ BLACK + GREY",
            "color": ["BLACK", "GREY"]
        },
        {  # NO COLOR
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
    ]


# Данные для параметризованных тестов создания курьера (негативные)
INCOMPLETE_COURIER_DATA = [
    ({"login": "test_login", "password": "test_pass"}, "Недостаточно данных для создания учетной записи"),
    ({"login": "test_login", "firstName": "Тест"}, "Недостаточно данных для создания учетной записи"),
    ({"password": "test_pass", "firstName": "Тест"}, "Недостаточно данных для создания учетной записи"),
]

# Данные для параметризованных тестов авторизации (негативные)
INCOMPLETE_LOGIN_DATA = [
    ({"login": "test_user"}, "Недостаточно данных для входа"),
    ({"password": "test_pass"}, "Недостаточно данных для входа"),
    ({}, "Недостаточно данных для входа"),
]