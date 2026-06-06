"""Фикстуры для тестов"""

import pytest
import allure
from helpers import (
    register_new_courier_and_return_login_password,
    delete_courier,
    get_courier_id
)


@pytest.fixture
def create_courier_and_delete():
    """Создаёт курьера и удаляет после теста"""
    with allure.step("Создание курьера"):
        courier_data = register_new_courier_and_return_login_password()

    if not courier_data:
        yield None, None, None
        return

    login, password, first_name = courier_data

    with allure.step(f"Получение ID курьера {login}"):
        courier_id = get_courier_id(login, password)

    yield login, password, first_name

    with allure.step(f"Удаление курьера {courier_id}"):
        if courier_id:
            delete_courier(courier_id)


@pytest.fixture
def create_test_courier():
    """Создаёт курьера, возвращает словарь с данными"""
    with allure.step("Создание курьера"):
        courier_data = register_new_courier_and_return_login_password()

    if not courier_data:
        return None

    login, password, first_name = courier_data
    courier_id = get_courier_id(login, password)

    return {
        "login": login,
        "password": password,
        "first_name": first_name,
        "id": courier_id
    }