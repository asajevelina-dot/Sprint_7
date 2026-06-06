"""Вспомогательные функции для тестов"""

import random
import string
import time
import allure
from api_client import ApiClient
from urls import Urls


def generate_random_string(length):
    """Генерирует случайную строку для логина/пароля курьера"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


@allure.step("Регистрация нового курьера")
def register_new_courier_and_return_login_password():
    """Регистрирует нового курьера, возвращает [login, password, first_name]"""
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = "ТестовыйКурьер"

    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    response = ApiClient.post(Urls.CREATE_COURIER, data=payload)

    if response.status_code == 201:
        return [login, password, first_name]
    return []


@allure.step("Удаление курьера по ID")
def delete_courier(courier_id):
    """Удаляет курьера по ID"""
    if courier_id:
        return ApiClient.delete(Urls.delete_courier(courier_id))
    return None


@allure.step("Получение ID курьера")
def get_courier_id(login, password):
    """Получает ID курьера по логину и паролю"""
    payload = {"login": login, "password": password}
    response = ApiClient.post(Urls.LOGIN_COURIER, data=payload)
    if response.status_code == 200:
        return response.json().get('id')
    return None


@allure.step("Создание тестового заказа")
def create_test_order(order_data=None):
    """Создаёт заказ, возвращает track номер"""
    if order_data is None:
        from data import OrderTestData
        order_data = OrderTestData.ORDER_BLACK

    response = ApiClient.post(Urls.CREATE_ORDER, json=order_data)
    if response.status_code == 201:
        time.sleep(1)
        return response.json().get('track')
    return None


@allure.step("Отмена заказа")
def cancel_order(track):
    """Отменяет заказ по трек-номеру"""
    if track:
        return ApiClient.put(Urls.CANCEL_ORDER, params={'track': track})
    return None


@allure.step("Получение ID заказа по трек-номеру")
def get_order_id_by_track(track):
    """Получает ID заказа по трек-номеру"""
    for attempt in range(3):
        response = ApiClient.get(Urls.GET_ORDER_BY_TRACK, params={'t': track})
        if response.status_code == 200:
            return response.json()['order']['id']
        time.sleep(1)
    return None