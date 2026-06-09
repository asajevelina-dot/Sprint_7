"""Тесты получения списка заказов"""

import allure
from api_client import ApiClient
from urls import Urls


@allure.feature('Заказы')
@allure.story('Список заказов')
class TestOrdersList:

    @allure.title('Получение списка заказов - возвращает список')
    def test_get_orders_list_returns_list(self):
        response = ApiClient.get(Urls.GET_ORDERS_LIST)

        assert response.status_code == 200
        assert 'orders' in response.json()
        assert isinstance(response.json()['orders'], list)

    @allure.title('Получение списка заказов с лимитом')
    def test_get_orders_list_with_limit(self):
        response = ApiClient.get(Urls.GET_ORDERS_LIST, params={'limit': 5})

        assert response.status_code == 200
        assert len(response.json()['orders']) <= 5

    @allure.title('Получение списка заказов - проверка структуры заказа')
    def test_get_orders_list_structure(self):
        response = ApiClient.get(Urls.GET_ORDERS_LIST, params={'limit': 1})

        assert response.status_code == 200
        orders = response.json()['orders']
        if len(orders) > 0:
            order = orders[0]
            expected_fields = ['id', 'firstName', 'lastName', 'address', 'track', 'status']
            for field in expected_fields:
                assert field in order

    @allure.title('Получение списка заказов с пагинацией')
    def test_get_orders_list_pagination(self):
        response = ApiClient.get(Urls.GET_ORDERS_LIST, params={'page': 0, 'limit': 5})
        assert response.status_code == 200
        assert 'pageInfo' in response.json()