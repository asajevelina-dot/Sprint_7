"""Вспомогательные функции для тестов"""

import random
import string


def generate_random_string(length):
    """Генерирует случайную строку для логина/пароля курьера"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))