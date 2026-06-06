# Sprint_7 - API тестирование сервиса "Яндекс.Самокат"

## 📝 Описание проекта
Автотесты для API сервиса заказа самокатов. Проверяют основные ручки:
- Создание курьера
- Авторизация курьера
- Создание заказа
- Получение списка заказов
- Дополнительные ручки (удаление курьера, принятие заказа, получение заказа по треку)

## 🛠 Технологии
- Python 3.14
- Pytest 7.4.3
- Requests 2.31.0
- Allure-pytest 2.13.2

## 📁 Структура проекта
Sprint_7/
├── tests/
│ ├── test_create_courier.py # Тесты создания курьера
│ ├── test_login_courier.py # Тесты авторизации
│ ├── test_create_order.py # Тесты создания заказа
│ ├── test_orders_list.py # Тесты списка заказов
│ └── test_additional.py # Дополнительные тесты
├── api_client.py # Базовый класс для API запросов
├── urls.py # URL endpoints
├── data.py # Тестовые данные
├── helpers.py # Вспомогательные функции
├── conftest.py # Фикстуры
└── requirements.txt # Зависимости

## 🚀 Запуск тестов

### Установка зависимостей
```bash
pip install -r requirements.txt
```
Запуск всех тестов
```bash
pytest tests/ -v
```
Запуск с генерацией Allure-отчёта
```bash
pytest tests/ --alluredir=allure_results -v
allure generate allure_results -o allure-report --clean
allure open allure-report```