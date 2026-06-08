"""Тесты создания курьера"""

import allure
import pytest
from api_client import ApiClient
from urls import Urls
from data import INCOMPLETE_COURIER_DATA
from helpers import generate_random_string


@allure.feature('Курьер')
@allure.story('Создание курьера')
class TestCreateCourier:

    @allure.title('Создание курьера - успех (позитивный сценарий)')
    def test_create_courier_success(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = "Тест"

        payload = {"login": login, "password": password, "firstName": first_name}
        response = ApiClient.post(Urls.CREATE_COURIER, data=payload)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.title('Создание курьера с повторяющимся логином - ошибка 409')
    def test_create_courier_duplicate_login_fails(self):
        login = generate_random_string(10)
        password = "test_pass_123"
        first_name = "Тест"

        payload = {"login": login, "password": password, "firstName": first_name}

        # Первое создание - успех
        response1 = ApiClient.post(Urls.CREATE_COURIER, data=payload)
        assert response1.status_code == 201

        # Второе создание с тем же логином - ошибка
        response2 = ApiClient.post(Urls.CREATE_COURIER, data=payload)
        assert response2.status_code == 409
        assert response2.json().get('message') == 'Этот логин уже используется'

    @allure.title('Создание курьера без обязательных полей - ошибка 400')
    @pytest.mark.parametrize("payload, expected_message", INCOMPLETE_COURIER_DATA)
    def test_create_courier_missing_field_fails(self, payload, expected_message):
        response = ApiClient.post(Urls.CREATE_COURIER, data=payload)

        assert response.status_code == 400
        assert response.json().get('message') == expected_message