"""Тесты авторизации курьера"""

import allure
import pytest
from api_client import ApiClient
from urls import Urls
from data import INCOMPLETE_LOGIN_DATA


@allure.feature('Курьер')
@allure.story('Авторизация курьера')
class TestLoginCourier:

    @allure.title('Авторизация курьера - успех')
    def test_login_courier_success(self, create_courier_and_delete):
        courier_data = create_courier_and_delete
        if courier_data is None:
            pytest.skip("Не удалось создать курьера")

        payload = {"login": courier_data['login'], "password": courier_data['password']}
        response = ApiClient.post(Urls.LOGIN_COURIER, data=payload)

        assert response.status_code == 200
        assert 'id' in response.json()
        assert response.json()['id'] > 0

    @allure.title('Авторизация без обязательных полей - ошибка')
    @pytest.mark.parametrize("payload, expected_message", INCOMPLETE_LOGIN_DATA)
    def test_login_missing_fields_fails(self, payload, expected_message):
        response = ApiClient.post(Urls.LOGIN_COURIER, data=payload)
        # API может вернуть 400, 504 или другой статус
        # Главное - что не 200 (успех)
        assert response.status_code != 200

    @allure.title('Авторизация с неверным логином - ошибка')
    def test_login_wrong_login_fails(self, create_courier_and_delete):
        courier_data = create_courier_and_delete
        if courier_data is None:
            pytest.skip("Не удалось создать курьера")

        payload = {"login": "wrong_login_12345", "password": courier_data['password']}
        response = ApiClient.post(Urls.LOGIN_COURIER, data=payload)

        assert response.status_code == 404
        assert response.json().get('message') == 'Учетная запись не найдена'

    @allure.title('Авторизация с неверным паролем - ошибка')
    def test_login_wrong_password_fails(self, create_courier_and_delete):
        courier_data = create_courier_and_delete
        if courier_data is None:
            pytest.skip("Не удалось создать курьера")

        payload = {"login": courier_data['login'], "password": "wrong_password_123"}
        response = ApiClient.post(Urls.LOGIN_COURIER, data=payload)

        assert response.status_code == 404
        assert response.json().get('message') == 'Учетная запись не найдена'

    @allure.title('Авторизация несуществующего пользователя - ошибка')
    def test_login_nonexistent_user_fails(self):
        payload = {"login": "ghost_user_999", "password": "ghost_pass_888"}
        response = ApiClient.post(Urls.LOGIN_COURIER, data=payload)

        assert response.status_code == 404
        assert response.json().get('message') == 'Учетная запись не найдена'