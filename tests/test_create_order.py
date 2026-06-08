"""Тесты создания заказа"""

import allure
import pytest
from api_client import ApiClient
from urls import Urls
from data import OrderTestData


@allure.feature('Заказы')
@allure.story('Создание заказа')
class TestCreateOrder:

    @allure.title('Создание заказа с разными вариантами цвета (параметризованный тест)')
    @pytest.mark.parametrize("order_payload", OrderTestData.ALL_ORDERS)
    def test_create_order_different_colors_success(self, order_payload):
        response = ApiClient.post(Urls.CREATE_ORDER, json=order_payload)

        assert response.status_code == 201
        assert 'track' in response.json()
        assert isinstance(response.json()['track'], int)