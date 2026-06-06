"""Тесты создания заказа"""

import allure
import pytest
from api_client import ApiClient
from urls import Urls
from data import OrderTestData


@allure.feature('Заказы')
@allure.story('Создание заказа')
class TestCreateOrder:

    @allure.title('Создание заказа с цветом BLACK')
    def test_create_order_black_color_success(self):
        response = ApiClient.post(Urls.CREATE_ORDER, json=OrderTestData.ORDER_BLACK)
        assert response.status_code == 201
        assert 'track' in response.json()

    @allure.title('Создание заказа с цветом GREY')
    def test_create_order_grey_color_success(self):
        response = ApiClient.post(Urls.CREATE_ORDER, json=OrderTestData.ORDER_GREY)
        assert response.status_code == 201
        assert 'track' in response.json()

    @allure.title('Создание заказа с двумя цветами')
    def test_create_order_both_colors_success(self):
        response = ApiClient.post(Urls.CREATE_ORDER, json=OrderTestData.ORDER_BOTH_COLORS)
        assert response.status_code == 201
        assert 'track' in response.json()

    @allure.title('Создание заказа без цвета')
    def test_create_order_no_color_success(self):
        response = ApiClient.post(Urls.CREATE_ORDER, json=OrderTestData.ORDER_NO_COLOR)
        assert response.status_code == 201
        assert 'track' in response.json()

    @allure.title('Создание заказа - параметризация по цветам')
    @pytest.mark.parametrize("order_payload", OrderTestData.ALL_ORDERS)
    def test_create_order_different_colors_success(self, order_payload):
        response = ApiClient.post(Urls.CREATE_ORDER, json=order_payload)
        assert response.status_code == 201
        assert 'track' in response.json()