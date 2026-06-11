"""Хранение всех URL endpoints для API"""


class Urls:
    """Базовые URL для API Самоката"""

    BASE_URL = 'https://qa-scooter.praktikum-services.ru'

    # Курьер
    CREATE_COURIER = '/api/v1/courier'
    LOGIN_COURIER = '/api/v1/courier/login'
    DELETE_COURIER_TEMPLATE = '/api/v1/courier/{courier_id}'

    # Заказы
    CREATE_ORDER = '/api/v1/orders'
    GET_ORDERS_LIST = '/api/v1/orders'
    GET_ORDER_BY_TRACK = '/api/v1/orders/track'
    ACCEPT_ORDER = '/api/v1/orders/accept/{order_id}'
    CANCEL_ORDER = '/api/v1/orders/cancel'