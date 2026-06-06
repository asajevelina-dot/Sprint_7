"""Дополнительные тесты: удаление курьера, принятие заказа, получение заказа по номеру"""

import allure
import time
from api_client import ApiClient
from urls import Urls
from helpers import create_test_order, cancel_order, get_order_id_by_track
from data import OrderTestData


@allure.feature('Курьер')
@allure.story('Удаление курьера')
class TestDeleteCourier:

    @allure.title('Удаление курьера - успех')
    def test_delete_courier_success(self, create_test_courier):
        courier_id = create_test_courier['id']
        response = ApiClient.delete(Urls.delete_courier(courier_id))
        assert response.status_code == 200
        assert response.json() == {"ok": True}

    @allure.title('Удаление несуществующего курьера - ошибка')
    def test_delete_nonexistent_courier_fails(self):
        response = ApiClient.delete(Urls.delete_courier(999999999))
        assert response.status_code == 404

    @allure.title('Удаление курьера с отрицательным ID - ошибка')
    def test_delete_courier_negative_id_fails(self):
        response = ApiClient.delete(Urls.delete_courier(-1))
        assert response.status_code in [400, 404, 500]

    @allure.title('Удаление курьера с текстовым ID - ошибка')
    def test_delete_courier_text_id_fails(self):
        response = ApiClient.delete(Urls.delete_courier("abc"))
        assert response.status_code in [400, 404, 500]


@allure.feature('Заказы')
@allure.story('Принятие заказа')
class TestAcceptOrder:

    @allure.title('Принятие заказа - успех')
    def test_accept_order_success(self, create_test_courier):
        courier_id = create_test_courier['id']
        track = create_test_order(OrderTestData.ORDER_BLACK)
        assert track is not None

        time.sleep(1)
        order_id = get_order_id_by_track(track)

        response = ApiClient.put(Urls.accept_order(order_id), params={'courierId': courier_id})
        assert response.status_code == 200
        assert response.json() == {"ok": True}

        cancel_order(track)

    @allure.title('Принятие заказа без ID курьера - ошибка')
    def test_accept_order_without_courier_id_fails(self):
        track = create_test_order(OrderTestData.ORDER_BLACK)
        assert track is not None

        time.sleep(1)
        order_id = get_order_id_by_track(track)

        response = ApiClient.put(Urls.accept_order(order_id))
        assert response.status_code in [400, 404]

        cancel_order(track)

    @allure.title('Принятие заказа с неверным ID курьера - ошибка')
    def test_accept_order_wrong_courier_id_fails(self):
        track = create_test_order(OrderTestData.ORDER_BLACK)
        assert track is not None

        time.sleep(1)
        order_id = get_order_id_by_track(track)

        response = ApiClient.put(Urls.accept_order(order_id), params={'courierId': 999999999})
        assert response.status_code == 404

        cancel_order(track)

    @allure.title('Принятие заказа с неверным ID заказа - ошибка')
    def test_accept_order_wrong_order_id_fails(self, create_test_courier):
        courier_id = create_test_courier['id']
        response = ApiClient.put(Urls.accept_order(999999999), params={'courierId': courier_id})
        assert response.status_code == 404


@allure.feature('Заказы')
@allure.story('Получение заказа по номеру')
class TestGetOrderByTrack:

    @allure.title('Получение заказа по трек-номеру - успех')
    def test_get_order_by_track_success(self):
        track = create_test_order(OrderTestData.ORDER_BLACK)
        assert track is not None

        time.sleep(2)
        response = ApiClient.get(Urls.GET_ORDER_BY_TRACK, params={'t': track})

        if response.status_code == 404:
            time.sleep(2)
            response = ApiClient.get(Urls.GET_ORDER_BY_TRACK, params={'t': track})

        assert response.status_code == 200
        assert 'order' in response.json()
        assert response.json()['order']['track'] == track

        cancel_order(track)

    @allure.title('Получение заказа без трек-номера - ошибка')
    def test_get_order_without_track_fails(self):
        response = ApiClient.get(Urls.GET_ORDER_BY_TRACK)
        assert response.status_code == 400

    @allure.title('Получение заказа с пустым трек-номером - ошибка')
    def test_get_order_empty_track_fails(self):
        response = ApiClient.get(Urls.GET_ORDER_BY_TRACK, params={'t': ''})
        assert response.status_code in [400, 404]

    @allure.title('Получение несуществующего заказа - ошибка')
    def test_get_nonexistent_order_fails(self):
        response = ApiClient.get(Urls.GET_ORDER_BY_TRACK, params={'t': 999999999})
        assert response.status_code == 404