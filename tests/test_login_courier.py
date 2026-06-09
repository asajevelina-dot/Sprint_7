"""Тесты авторизации курьера"""

import allure
import pytest
from api_client import ApiClient
from urls import Urls
from data import INCOMPLETE_LOGIN_DATA
from helpers import generate_random_string


@allure.feature('Курьер')
@allure.story('Авторизация курьера')
class TestLoginCourier:

    @allure.title('Авторизация курьера - успех (200, id)')
    def test_login_courier_success(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = "Тест"

        create_payload = {"login": login, "password": password, "firstName": first_name}
        create_response = ApiClient.post(Urls.CREATE_COURIER, data=create_payload)
        assert create_response.status_code == 201

        login_payload = {"login": login, "password": password}
        response = ApiClient.post(Urls.LOGIN_COURIER, data=login_payload)

        assert response.status_code == 200
        assert 'id' in response.json()
        assert response.json()['id'] > 0

    @allure.title('Авторизация без обязательных полей - ошибка 400')
    @pytest.mark.parametrize("payload, expected_message", INCOMPLETE_LOGIN_DATA)
    def test_login_missing_fields_fails(self, payload, expected_message):
        response = ApiClient.post(Urls.LOGIN_COURIER, data=payload)

        assert response.status_code == 400
        assert response.json().get('message') == expected_message

    @allure.title('Авторизация с несуществующими данными - ошибка 404')
    def test_login_nonexistent_user_fails(self):
        payload = {"login": "ghost_user_999", "password": "ghost_pass_888"}
        response = ApiClient.post(Urls.LOGIN_COURIER, data=payload)

        assert response.status_code == 404
        assert response.json().get('message') == 'Учетная запись не найдена'

    @allure.title('Авторизация с неверным паролем - ошибка 404')
    def test_login_wrong_password_fails(self):
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = "Тест"

        create_payload = {"login": login, "password": password, "firstName": first_name}
        create_response = ApiClient.post(Urls.CREATE_COURIER, data=create_payload)
        assert create_response.status_code == 201

        wrong_password = "wrong_password_123"
        login_payload = {"login": login, "password": wrong_password}
        response = ApiClient.post(Urls.LOGIN_COURIER, data=login_payload)

        assert response.status_code == 404
        assert response.json().get('message') == 'Учетная запись не найдена'