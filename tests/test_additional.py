"""Дополнительные тесты: удаление курьера, принятие заказа, получение заказа по номеру"""

import pytest
import allure
import time
from api_client import ApiClient
from urls import Urls
from data import OrderTestData


@allure.feature('Курьер')
@allure.story('Удаление курьера')
class TestDeleteCourier:

    @allure.title('Удаление курьера - успех')
    def test_delete_courier_success(self, create_test_courier):
        courier_data = create_test_courier
        if courier_data is None:
            pytest.skip("Не удалось создать курьера")

        response = ApiClient.delete(Urls.delete_courier(courier_data['id']))
        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title('Удаление несуществующего курьера - ошибка')
    def test_delete_nonexistent_courier_fails(self):
        response = ApiClient.delete(Urls.delete_courier(999999999))
        assert response.status_code == 404
        assert response.json().get('message') == 'Курьера с таким id нет'

    @allure.title('Удаление курьера с отрицательным ID - ошибка')
    def test_delete_courier_negative_id_fails(self):
        response = ApiClient.delete(Urls.delete_courier(-1))
        assert response.status_code in [400, 404]

    @allure.title('Удаление курьера с текстовым ID - ошибка')
    def test_delete_courier_text_id_fails(self):
        response = ApiClient.delete(Urls.delete_courier("abc"))
        assert response.status_code in [400, 404, 500]


@allure.feature('Заказы')
@allure.story('Принятие заказа')
class TestAcceptOrder:

    @allure.title('Принятие заказа - успех')
    def test_accept_order_success(self, create_test_courier):
        courier_data = create_test_courier
        if courier_data is None:
            pytest.skip("Не удалось создать курьера")

        # Создаём заказ
        response = ApiClient.post(Urls.CREATE_ORDER, json=OrderTestData.ORDER_BLACK)
        assert response.status_code == 201
        track = response.json().get('track')

        time.sleep(1)

        # Получаем ID заказа
        order_response = ApiClient.get(Urls.GET_ORDER_BY_TRACK, params={'t': track})
        assert order_response.status_code == 200
        order_id = order_response.json()['order']['id']

        # Принимаем заказ
        accept_response = ApiClient.put(Urls.accept_order(order_id), params={'courierId': courier_data['id']})
        assert accept_response.status_code == 200
        assert accept_response.json() == {"ok": True}

        # Отменяем заказ для очистки
        ApiClient.put(Urls.CANCEL_ORDER, params={'track': track})

    @allure.title('Принятие заказа без ID курьера - ошибка')
    def test_accept_order_without_courier_id_fails(self):
        response = ApiClient.post(Urls.CREATE_ORDER, json=OrderTestData.ORDER_BLACK)
        assert response.status_code == 201
        track = response.json().get('track')

        time.sleep(1)

        order_response = ApiClient.get(Urls.GET_ORDER_BY_TRACK, params={'t': track})
        assert order_response.status_code == 200
        order_id = order_response.json()['order']['id']

        accept_response = ApiClient.put(Urls.accept_order(order_id))
        assert accept_response.status_code == 400
        assert accept_response.json().get('message') == 'Недостаточно данных для поиска'

        ApiClient.put(Urls.CANCEL_ORDER, params={'track': track})

    @allure.title('Принятие заказа с неверным ID курьера - ошибка')
    def test_accept_order_wrong_courier_id_fails(self):
        response = ApiClient.post(Urls.CREATE_ORDER, json=OrderTestData.ORDER_BLACK)
        assert response.status_code == 201
        track = response.json().get('track')

        time.sleep(1)

        order_response = ApiClient.get(Urls.GET_ORDER_BY_TRACK, params={'t': track})
        assert order_response.status_code == 200
        order_id = order_response.json()['order']['id']

        accept_response = ApiClient.put(Urls.accept_order(order_id), params={'courierId': 999999999})
        assert accept_response.status_code == 404
        assert accept_response.json().get('message') == 'Курьера с таким id нет'

        ApiClient.put(Urls.CANCEL_ORDER, params={'track': track})

    @allure.title('Принятие заказа с неверным ID заказа - ошибка')
    def test_accept_order_wrong_order_id_fails(self, create_test_courier):
        courier_data = create_test_courier
        if courier_data is None:
            pytest.skip("Не удалось создать курьера")

        response = ApiClient.put(Urls.accept_order(999999999), params={'courierId': courier_data['id']})
        assert response.status_code == 404
        assert response.json().get('message') == 'Заказа с таким id нет'


@allure.feature('Заказы')
@allure.story('Получение заказа по номеру')
class TestGetOrderByTrack:

    @allure.title('Получение заказа по трек-номеру - успех')
    def test_get_order_by_track_success(self):
        response = ApiClient.post(Urls.CREATE_ORDER, json=OrderTestData.ORDER_BLACK)
        assert response.status_code == 201
        track = response.json().get('track')

        time.sleep(2)

        order_response = ApiClient.get(Urls.GET_ORDER_BY_TRACK, params={'t': track})

        if order_response.status_code == 404:
            time.sleep(2)
            order_response = ApiClient.get(Urls.GET_ORDER_BY_TRACK, params={'t': track})

        assert order_response.status_code == 200
        assert 'order' in order_response.json()
        assert order_response.json()['order']['track'] == track

        ApiClient.put(Urls.CANCEL_ORDER, params={'track': track})

    @allure.title('Получение заказа без трек-номера - ошибка')
    def test_get_order_without_track_fails(self):
        response = ApiClient.get(Urls.GET_ORDER_BY_TRACK)
        assert response.status_code == 400
        assert response.json().get('message') == 'Недостаточно данных для поиска'

    @allure.title('Получение заказа с пустым трек-номером - ошибка')
    def test_get_order_empty_track_fails(self):
        response = ApiClient.get(Urls.GET_ORDER_BY_TRACK, params={'t': ''})
        assert response.status_code == 400

    @allure.title('Получение несуществующего заказа - ошибка')
    def test_get_nonexistent_order_fails(self):
        response = ApiClient.get(Urls.GET_ORDER_BY_TRACK, params={'t': 999999999})
        assert response.status_code == 404
        assert response.json().get('message') == 'Заказ не найден'