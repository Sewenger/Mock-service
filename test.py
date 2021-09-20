import pytest
import requests
from faker import Faker
import random


@pytest.fixture
def host():
    yield 'http://127.0.0.1:5000'


def test_create_user(host: str):
    """ Проверка создания пользователя"""
    faker = Faker()
    body = {
        'name': faker.first_name(),
        'job': faker.job()
    }
    response = requests.post(f'{host}/api/users', json=body)
    assert response.status_code == 201
    user = response.json()

    assert 'id' in user
    assert 'createdAt' in user
    assert user['name'] == body["name"]
    assert user['job'] == body["job"]


@pytest.mark.parametrize('field', ('job', 'name'))
def test_create_user_field_name_is_empty(host: str, field: str):
    """Проверка валидации обязательных полей"""
    faker = Faker()
    body = {
        'name': faker.first_name(),
        'job': faker.job()
    }
    del body[field]
    response = requests.post(f'{host}/api/users', json=body)
    assert response.status_code == 400
    error = response.json()
    assert error['msg'] == f'{field.title()} field is required'


def test_get_user_by_id(host: str):
    """Получение рандомного пользователья"""
    users = requests.get(f'{host}/api/users').json()
    random_user = random.choice(users["data"])
    user = requests.get(f'{host}/api/users/{random_user["id"]}').json()
    assert user == random_user


def test_get_user_by_invalid_id(host: str):
    """Проверка получения несуществующего пользователя"""
    users = requests.get(f'{host}/api/users').json()
    random_user = max(users["data"], key=lambda x: x["id"])
    response = requests.get(f'{host}/api/users/{random_user["id"] + 1}')
    assert response.status_code == 404
    error = response.json()
    assert error['msg'] == 'User not found'
