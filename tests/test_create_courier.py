"""Тесты создания курьера"""

import allure
import pytest
from api_client import ApiClient
from urls import Urls
from data import INCOMPLETE_COURIER_DATA
from helpers import register_new_courier_and_return_login_password, delete_courier, get_courier_id, generate_random_string


@allure.feature('Курьер')
@allure.story('Создание курьера')
class TestCreateCourier:

    @allure.title('Создание курьера - успех')
    def test_create_courier_success(self):
        courier_data = register_new_courier_and_return_login_password()
        assert len(courier_data) == 3

    @allure.title('Создание двух одинаковых курьеров - ошибка')
    def test_create_duplicate_courier_fails(self):
        # Используем УНИКАЛЬНЫЙ логин через генератор
        unique_login = generate_random_string(10)
        password = "test_pass_123"
        first_name = "Тест"

        payload = {"login": unique_login, "password": password, "firstName": first_name}

        response1 = ApiClient.post(Urls.CREATE_COURIER, data=payload)
        assert response1.status_code == 201, f"Ошибка при создании: {response1.status_code}"

        response2 = ApiClient.post(Urls.CREATE_COURIER, data=payload)
        assert response2.status_code == 409, f"Ожидался 409, получен {response2.status_code}"

        # Очистка
        courier_id = get_courier_id(unique_login, password)
        if courier_id:
            delete_courier(courier_id)

    @allure.title('Создание курьера - ответ содержит ok:true')
    def test_create_courier_response_has_ok_true(self):
        login = generate_random_string(8)
        password = "test_pass_456"
        first_name = "ОкТест"

        payload = {"login": login, "password": password, "firstName": first_name}
        response = ApiClient.post(Urls.CREATE_COURIER, data=payload)

        assert response.status_code == 201
        assert response.json() == {"ok": True}

        # Очистка
        courier_id = get_courier_id(login, password)
        if courier_id:
            delete_courier(courier_id)

    @allure.title('Создание курьера без обязательных полей - ошибка')
    @pytest.mark.parametrize("payload, missing_field", INCOMPLETE_COURIER_DATA)
    def test_create_courier_missing_field_fails(self, payload, missing_field):
        response = ApiClient.post(Urls.CREATE_COURIER, data=payload)
        assert response.status_code != 201

    @allure.title('Создание курьера с существующим логином - ошибка')
    def test_create_courier_existing_login_fails(self):
        # Создаём первого курьера с уникальным логином
        login = generate_random_string(8)
        password = "first_pass_123"

        payload1 = {"login": login, "password": password, "firstName": "Первый"}
        response1 = ApiClient.post(Urls.CREATE_COURIER, data=payload1)
        assert response1.status_code == 201

        # Пытаемся создать второго с таким же логином
        payload2 = {"login": login, "password": "second_pass_456", "firstName": "Второй"}
        response2 = ApiClient.post(Urls.CREATE_COURIER, data=payload2)

        assert response2.status_code == 409

        # Очистка
        courier_id = get_courier_id(login, password)
        if courier_id:
            delete_courier(courier_id)