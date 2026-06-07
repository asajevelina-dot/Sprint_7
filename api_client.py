"""Базовый класс для выполнения API запросов"""

import allure
import requests
from urls import Urls


class ApiClient:
    """Базовый класс для всех API запросов"""

    @staticmethod
    @allure.step("POST {endpoint}")
    def post(endpoint, data=None, json=None, params=None):
        """Выполняет POST запрос"""
        url = f'{Urls.BASE_URL}{endpoint}'
        response = requests.post(url, data=data, json=json, params=params)
        allure.attach(str(response.status_code), name="Status Code", attachment_type=allure.attachment_type.TEXT)
        allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.TEXT)
        return response

    @staticmethod
    @allure.step("GET {endpoint}")
    def get(endpoint, params=None):
        """Выполняет GET запрос"""
        url = f'{Urls.BASE_URL}{endpoint}'
        response = requests.get(url, params=params)
        allure.attach(str(response.status_code), name="Status Code", attachment_type=allure.attachment_type.TEXT)
        allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.TEXT)
        return response

    @staticmethod
    @allure.step("PUT {endpoint}")
    def put(endpoint, params=None, json=None):
        """Выполняет PUT запрос"""
        url = f'{Urls.BASE_URL}{endpoint}'
        response = requests.put(url, params=params, json=json)
        allure.attach(str(response.status_code), name="Status Code", attachment_type=allure.attachment_type.TEXT)
        allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.TEXT)
        return response

    @staticmethod
    @allure.step("DELETE {endpoint}")
    def delete(endpoint):
        """Выполняет DELETE запрос"""
        url = f'{Urls.BASE_URL}{endpoint}'
        response = requests.delete(url)
        allure.attach(str(response.status_code), name="Status Code", attachment_type=allure.attachment_type.TEXT)
        allure.attach(response.text, name="Response Body", attachment_type=allure.attachment_type.TEXT)
        return response