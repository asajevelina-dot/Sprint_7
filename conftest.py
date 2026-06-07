"""Фикстуры для тестов"""

import pytest
import allure
from api_client import ApiClient
from urls import Urls
from helpers import generate_random_string, get_courier_id


@pytest.fixture
def create_courier_and_delete():
    """Создаёт курьера и удаляет после теста"""
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = "ТестовыйКурьер"

    payload = {"login": login, "password": password, "firstName": first_name}
    response = ApiClient.post(Urls.CREATE_COURIER, data=payload)

    if response.status_code == 201:
        courier_id = get_courier_id(login, password)
        yield {"login": login, "password": password, "first_name": first_name, "id": courier_id}

        # Удаление после теста
        if courier_id:
            ApiClient.delete(Urls.delete_courier(courier_id))
    else:
        yield None


@pytest.fixture
def create_test_courier():
    """Создаёт курьера, возвращает словарь с данными"""
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = "ТестовыйКурьер"

    payload = {"login": login, "password": password, "firstName": first_name}
    response = ApiClient.post(Urls.CREATE_COURIER, data=payload)

    if response.status_code == 201:
        courier_id = get_courier_id(login, password)
        return {"login": login, "password": password, "first_name": first_name, "id": courier_id}
    return None