"""Тесты авторизации курьера"""

import allure
from api_client import ApiClient
from urls import Urls
from helpers import register_new_courier_and_return_login_password


@allure.feature('Курьер')
@allure.story('Авторизация курьера')
class TestLoginCourier:

    @allure.title('Авторизация курьера - успех')
    def test_login_courier_success(self, create_courier_and_delete):
        login, password, _ = create_courier_and_delete

        payload = {"login": login, "password": password}
        response = ApiClient.post(Urls.LOGIN_COURIER, data=payload)

        assert response.status_code == 200
        assert 'id' in response.json()
        assert response.json()['id'] > 0

    @allure.title('Авторизация без пароля - ошибка')
    def test_login_without_password_fails(self, create_courier_and_delete):
        login, _, _ = create_courier_and_delete

        payload = {"login": login}
        response = ApiClient.post(Urls.LOGIN_COURIER, data=payload)

        assert response.status_code != 200

    @allure.title('Авторизация без логина - ошибка')
    def test_login_without_login_fails(self, create_courier_and_delete):
        _, password, _ = create_courier_and_delete

        payload = {"password": password}
        response = ApiClient.post(Urls.LOGIN_COURIER, data=payload)

        assert response.status_code != 200

    @allure.title('Авторизация без полей - ошибка')
    def test_login_without_fields_fails(self):
        response = ApiClient.post(Urls.LOGIN_COURIER, data={})
        assert response.status_code != 200

    @allure.title('Авторизация с неверным логином - ошибка')
    def test_login_wrong_login_fails(self, create_courier_and_delete):
        _, password, _ = create_courier_and_delete

        payload = {"login": "wrong_login_12345", "password": password}
        response = ApiClient.post(Urls.LOGIN_COURIER, data=payload)

        assert response.status_code == 404

    @allure.title('Авторизация с неверным паролем - ошибка')
    def test_login_wrong_password_fails(self, create_courier_and_delete):
        login, _, _ = create_courier_and_delete

        payload = {"login": login, "password": "wrong_password_123"}
        response = ApiClient.post(Urls.LOGIN_COURIER, data=payload)

        assert response.status_code == 404

    @allure.title('Авторизация несуществующего пользователя - ошибка')
    def test_login_nonexistent_user_fails(self):
        payload = {"login": "ghost_user_999", "password": "ghost_pass_888"}
        response = ApiClient.post(Urls.LOGIN_COURIER, data=payload)

        assert response.status_code == 404