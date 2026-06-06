import allure
import requests
from urls import Urls

class ApiClient:
    @staticmethod
    @allure.step("POST {endpoint}")
    def post(endpoint, data=None, json=None, params=None):
        url = f'{Urls.BASE_URL}{endpoint}'
        return requests.post(url, data=data, json=json, params=params)

    @staticmethod
    @allure.step("GET {endpoint}")
    def get(endpoint, params=None):
        url = f'{Urls.BASE_URL}{endpoint}'
        return requests.get(url, params=params)

    @staticmethod
    @allure.step("PUT {endpoint}")
    def put(endpoint, params=None, json=None):
        url = f'{Urls.BASE_URL}{endpoint}'
        return requests.put(url, params=params, json=json)

    @staticmethod
    @allure.step("DELETE {endpoint}")
    def delete(endpoint):
        url = f'{Urls.BASE_URL}{endpoint}'
        return requests.delete(url)