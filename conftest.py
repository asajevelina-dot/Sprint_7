import pytest
import allure
from helpers import register_new_courier_and_return_login_password, delete_courier, get_courier_id

@pytest.fixture
def create_courier_and_delete():
    with allure.step("Создание курьера"):
        courier_data = register_new_courier_and_return_login_password()
    if not courier_data:
        yield None, None, None
        return
    login, password, first_name = courier_data
    courier_id = get_courier_id(login, password)
    yield login, password, first_name
    if courier_id:
        delete_courier(courier_id)

@pytest.fixture
def create_test_courier():
    courier_data = register_new_courier_and_return_login_password()
    if not courier_data:
        return None
    login, password, first_name = courier_data
    courier_id = get_courier_id(login, password)
    return {"login": login, "password": password, "first_name": first_name, "id": courier_id}