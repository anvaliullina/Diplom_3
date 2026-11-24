from uuid import uuid4

import allure
import requests
from config import BASE_URL


class TestDataApi:
    def __init__(self):
        self.session = requests.Session()

    @allure.step('Получить ингредиенты через API')
    def ingredients(self):
        response = self.session.get(BASE_URL + '/api/ingredients', timeout=30)
        response.raise_for_status()
        return response.json()['data']

    @allure.step('Создать тестового пользователя через API')
    def register(self, data):
        response = self.session.post(BASE_URL + '/api/auth/register', json=data, timeout=30)
        response.raise_for_status()
        if not response.json().get('success'):
            raise RuntimeError('API не подтвердил регистрацию тестового пользователя')
        return response.json()

    @allure.step('Удалить тестового пользователя через API')
    def cleanup(self, data):
        response = self.session.post(
            BASE_URL + '/api/auth/login',
            json={'email': data['email'], 'password': data['password']},
            timeout=30,
        )
        if response.status_code == 401:
            return
        response.raise_for_status()
        deleted = self.session.delete(
            BASE_URL + '/api/auth/user',
            headers={'Authorization': response.json()['accessToken']},
            timeout=30,
        )
        if deleted.status_code != 202:
            raise RuntimeError(f'Ошибка удаления пользователя: {deleted.status_code}')

    @staticmethod
    def new_user():
        return {
            'email': f'anna.ui.{uuid4().hex}@example.com',
            'password': 'QaTest!123456',
            'name': 'Anna UI',
        }
