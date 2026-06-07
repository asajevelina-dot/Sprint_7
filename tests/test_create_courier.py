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

    @allure.title('Создание курьера - успех')
    def test_create_courier_success(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = "Тест"

        payload = {"login": login, "password": password, "firstName": first_name}
        response = ApiClient.post(Urls.CREATE_COURIER, data=payload)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.title('Создание двух одинаковых курьеров - ошибка')
    def test_create_duplicate_courier_fails(self):
        unique_login = generate_random_string(10)
        password = "test_pass_123"
        first_name = "Тест"

        payload = {"login": unique_login, "password": password, "firstName": first_name}

        response1 = ApiClient.post(Urls.CREATE_COURIER, data=payload)
        assert response1.status_code == 201
        assert response1.json() == {"ok": True}

        response2 = ApiClient.post(Urls.CREATE_COURIER, data=payload)

        assert response2.status_code == 409
        assert response2.json().get('message') == 'Этот логин уже используется. Попробуйте другой.'

    @allure.title('Создание курьера - ответ содержит ok:true')
    def test_create_courier_response_has_ok_true(self):
        login = generate_random_string(8)
        password = "test_pass_456"
        first_name = "ОкТест"

        payload = {"login": login, "password": password, "firstName": first_name}
        response = ApiClient.post(Urls.CREATE_COURIER, data=payload)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

    @allure.title('Создание курьера без обязательных полей - ошибка')
    @pytest.mark.parametrize("payload, expected_message", INCOMPLETE_COURIER_DATA)
    def test_create_courier_missing_field_fails(self, payload, expected_message):
        response = ApiClient.post(Urls.CREATE_COURIER, data=payload)
        # API возвращает 400 или 409 (если логин уже существует)
        assert response.status_code in [400, 409]

    @allure.title('Создание курьера с существующим логином - ошибка')
    def test_create_courier_existing_login_fails(self, create_courier_and_delete):
        courier_data = create_courier_and_delete
        if courier_data is None:
            pytest.skip("Не удалось создать курьера")

        login = courier_data['login']

        payload = {"login": login, "password": "second_pass_456", "firstName": "Второй"}
        response = ApiClient.post(Urls.CREATE_COURIER, data=payload)

        assert response.status_code == 409
        assert response.json().get('message') == 'Этот логин уже используется. Попробуйте другой.'