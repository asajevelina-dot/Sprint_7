"""Базовый класс для выполнения API запросов"""

import allure
import requests
from urls import Urls


class ApiClient:
    """Базовый класс для всех API запросов"""

    @staticmethod
    @allure.step("POST {endpoint}")
    def post(endpoint, data=None, json=None, params=None):
        url = f'{Urls.BASE_URL}{endpoint}'
        response = requests.post(url, data=data, json=json, params=params)
        allure.attach(str(response.status_code), name="Status Code", attachment_type=allure.attachment_type.TEXT)
        allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.TEXT)
        return response

    @staticmethod
    @allure.step("GET {endpoint}")
    def get(endpoint, params=None):
        url = f'{Urls.BASE_URL}{endpoint}'
        response = requests.get(url, params=params)
        allure.attach(str(response.status_code), name="Status Code", attachment_type=allure.attachment_type.TEXT)
        allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.TEXT)
        return response

    @staticmethod
    @allure.step("PUT {endpoint}")
    def put(endpoint, params=None, json=None):
        url = f'{Urls.BASE_URL}{endpoint}'
        response = requests.put(url, params=params, json=json)
        allure.attach(str(response.status_code), name="Status Code", attachment_type=allure.attachment_type.TEXT)
        allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.TEXT)
        return response

    @staticmethod
    @allure.step("DELETE {endpoint}")
    def delete(endpoint):
        url = f'{Urls.BASE_URL}{endpoint}'
        response = requests.delete(url)
        allure.attach(str(response.status_code), name="Status Code", attachment_type=allure.attachment_type.TEXT)
        allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.TEXT)
        return response

    # Вспомогательные методы для работы с URL
    @staticmethod
    def delete_courier(courier_id):
        return ApiClient.delete(Urls.DELETE_COURIER_TEMPLATE.format(courier_id=courier_id))

    @staticmethod
    def accept_order(order_id, courier_id):
        return ApiClient.put(Urls.ACCEPT_ORDER.format(order_id=order_id), params={'courierId': courier_id})