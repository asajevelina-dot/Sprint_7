"""Дополнительные тесты: удаление курьера, принятие заказа, получение заказа по номеру"""

import allure
import time
from api_client import ApiClient
from urls import Urls
from data import OrderTestData
from helpers import generate_random_string


@allure.feature('Курьер')
@allure.story('Удаление курьера')
class TestDeleteCourier:

    @allure.title('Удаление курьера - успех')
    def test_delete_courier_success(self):
        # Создаём курьера
        login = generate_random_string(10)
        password = generate_random_string(10)
        first_name = "Тест"

        create_payload = {"login": login, "password": password, "firstName": first_name}
        create_response = ApiClient.post(Urls.CREATE_COURIER, data=create_payload)
        assert create_response.status_code == 201

        # Получаем ID курьера
        login_payload = {"login": login, "password": password}
        login_response = ApiClient.post(Urls.LOGIN_COURIER, data=login_payload)
        assert login_response.status_code == 200
        courier_id = login_response.json()['id']

        # Удаляем курьера
        delete_response = ApiClient.delete(Urls.delete_courier(courier_id))
        assert delete_response.status_code == 200
        assert delete_response.json() == {"ok": True}

    @allure.title('Удаление несуществующего курьера - ошибка 400')
    def test_delete_nonexistent_courier_fails(self):
        response = ApiClient.delete(Urls.delete_courier(999999999))
        assert response.status_code == 400
        assert response.json().get('message') == 'Недостаточно данных для удаления курьера'

    @allure.title('Удаление курьера без ID - ошибка 400')
    def test_delete_courier_without_id_fails(self):
        response = ApiClient.delete('/api/v1/courier/')
        assert response.status_code == 400


@allure.feature('Заказы')
@allure.story('Принятие заказа')
class TestAcceptOrder:

    @allure.title('Принятие заказа - успех')
    def test_accept_order_success(self):
        # Создаём курьера
        login = generate_random_string(10)
        password = generate_random_string(10)

        create_courier_payload = {"login": login, "password": password, "firstName": "Тест"}
        create_courier_response = ApiClient.post(Urls.CREATE_COURIER, data=create_courier_payload)
        assert create_courier_response.status_code == 201

        # Получаем ID курьера
        login_payload = {"login": login, "password": password}
        login_response = ApiClient.post(Urls.LOGIN_COURIER, data=login_payload)
        assert login_response.status_code == 200
        courier_id = login_response.json()['id']

        # Создаём заказ
        order_response = ApiClient.post(Urls.CREATE_ORDER, json=OrderTestData.ALL_ORDERS[0])
        assert order_response.status_code == 201
        track = order_response.json().get('track')

        time.sleep(1)

        # Получаем ID заказа
        track_response = ApiClient.get(Urls.GET_ORDER_BY_TRACK, params={'t': track})
        assert track_response.status_code == 200
        order_id = track_response.json()['order']['id']

        # Принимаем заказ
        accept_response = ApiClient.put(Urls.accept_order(order_id), params={'courierId': courier_id})
        assert accept_response.status_code == 200
        assert accept_response.json() == {"ok": True}

        # Отменяем заказ для очистки
        ApiClient.put(Urls.CANCEL_ORDER, params={'track': track})

    @allure.title('Принятие заказа без ID курьера - ошибка 400')
    def test_accept_order_without_courier_id_fails(self):
        # Создаём заказ
        order_response = ApiClient.post(Urls.CREATE_ORDER, json=OrderTestData.ALL_ORDERS[0])
        assert order_response.status_code == 201
        track = order_response.json().get('track')

        time.sleep(1)

        # Получаем ID заказа
        track_response = ApiClient.get(Urls.GET_ORDER_BY_TRACK, params={'t': track})
        assert track_response.status_code == 200
        order_id = track_response.json()['order']['id']

        # Пытаемся принять заказ без ID курьера
        accept_response = ApiClient.put(Urls.accept_order(order_id))
        assert accept_response.status_code == 400
        assert accept_response.json().get('message') == 'Недостаточно данных для поиска'

        # Отменяем заказ для очистки
        ApiClient.put(Urls.CANCEL_ORDER, params={'track': track})

    @allure.title('Принятие заказа с неверным ID курьера - ошибка 400')
    def test_accept_order_wrong_courier_id_fails(self):
        # Создаём заказ
        order_response = ApiClient.post(Urls.CREATE_ORDER, json=OrderTestData.ALL_ORDERS[0])
        assert order_response.status_code == 201
        track = order_response.json().get('track')

        time.sleep(1)

        # Получаем ID заказа
        track_response = ApiClient.get(Urls.GET_ORDER_BY_TRACK, params={'t': track})
        assert track_response.status_code == 200
        order_id = track_response.json()['order']['id']

        # Пытаемся принять заказ с неверным ID курьера
        accept_response = ApiClient.put(Urls.accept_order(order_id), params={'courierId': 999999999})
        assert accept_response.status_code == 400
        assert accept_response.json().get('message') == 'Недостаточно данных для поиска'

        # Отменяем заказ для очистки
        ApiClient.put(Urls.CANCEL_ORDER, params={'track': track})

    @allure.title('Принятие заказа с неверным ID заказа - ошибка 400')
    def test_accept_order_wrong_order_id_fails(self):
        # Создаём курьера
        login = generate_random_string(10)
        password = generate_random_string(10)

        create_courier_payload = {"login": login, "password": password, "firstName": "Тест"}
        create_courier_response = ApiClient.post(Urls.CREATE_COURIER, data=create_courier_payload)
        assert create_courier_response.status_code == 201

        # Получаем ID курьера
        login_payload = {"login": login, "password": password}
        login_response = ApiClient.post(Urls.LOGIN_COURIER, data=login_payload)
        assert login_response.status_code == 200
        courier_id = login_response.json()['id']

        # Пытаемся принять заказ с неверным ID заказа
        accept_response = ApiClient.put(Urls.accept_order(999999999), params={'courierId': courier_id})
        assert accept_response.status_code == 400
        assert accept_response.json().get('message') == 'Недостаточно данных для поиска'


@allure.feature('Заказы')
@allure.story('Получение заказа по номеру')
class TestGetOrderByTrack:

    @allure.title('Получение заказа по трек-номеру - успех')
    def test_get_order_by_track_success(self):
        # Создаём заказ
        order_response = ApiClient.post(Urls.CREATE_ORDER, json=OrderTestData.ALL_ORDERS[0])
        assert order_response.status_code == 201
        track = order_response.json().get('track')

        time.sleep(2)

        # Получаем заказ по треку
        track_response = ApiClient.get(Urls.GET_ORDER_BY_TRACK, params={'t': track})

        if track_response.status_code == 404:
            time.sleep(2)
            track_response = ApiClient.get(Urls.GET_ORDER_BY_TRACK, params={'t': track})

        assert track_response.status_code == 200
        assert 'order' in track_response.json()
        assert track_response.json()['order']['track'] == track

        # Отменяем заказ для очистки
        ApiClient.put(Urls.CANCEL_ORDER, params={'track': track})

    @allure.title('Получение заказа без трек-номера - ошибка 400')
    def test_get_order_without_track_fails(self):
        response = ApiClient.get(Urls.GET_ORDER_BY_TRACK)
        assert response.status_code == 400
        assert response.json().get('message') == 'Недостаточно данных для поиска'

    @allure.title('Получение заказа с пустым трек-номером - ошибка 400')
    def test_get_order_empty_track_fails(self):
        response = ApiClient.get(Urls.GET_ORDER_BY_TRACK, params={'t': ''})
        assert response.status_code == 400

    @allure.title('Получение несуществующего заказа - ошибка 400')
    def test_get_nonexistent_order_fails(self):
        response = ApiClient.get(Urls.GET_ORDER_BY_TRACK, params={'t': 999999999})
        assert response.status_code == 400
        assert response.json().get('message') == 'Недостаточно данных для поиска'