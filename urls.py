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
    ACCEPT_ORDER_TEMPLATE = '/api/v1/orders/accept/{order_id}'
    CANCEL_ORDER = '/api/v1/orders/cancel'

    @staticmethod
    def delete_courier(courier_id):
        """Возвращает URL для удаления курьера по ID"""
        return Urls.DELETE_COURIER_TEMPLATE.format(courier_id=courier_id)

    @staticmethod
    def accept_order(order_id):
        """Возвращает URL для принятия заказа по ID"""
        return Urls.ACCEPT_ORDER_TEMPLATE.format(order_id=order_id)