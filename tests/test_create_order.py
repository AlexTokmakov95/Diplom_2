import pytest
import allure
import requests

from data.urls import Urls
from data.user_data import User
from data.ingredients_data import Ingredients

class TestCreateOrder:
    @allure.description('Успешное создание заказа с авторизованным пользователем')
    @allure.title('Создание заказа с авторизацией')
    def test_create_order_with_authorization(self, create_user):
        token = {'Authorization': create_user[3]}
        with allure.step("Отправляем запрос на создание заказа"):
            r = requests.post(Urls.url_create_order, headers=token, data=Ingredients.correct_ingredients_data)
        assert r.status_code == 200 and r.json().get("success") is True

    @allure.description('Успешное создание заказа с неавторизованным пользователем')
    @allure.title('Создание заказа без авторизации')
    def test_create_order_not_authorization(self):
        with allure.step("Отправляем запрос на создание заказа"):
            r = requests.post(Urls.url_create_order, data=Ingredients.correct_ingredients_data)
        assert r.status_code == 200 and r.json().get("success") is True  

    @allure.description('Ошибка при создании заказа без ингредиентов')
    @allure.title('Создание заказа без ингредиентов')
    def test_create_order_without_ingridients(self):
        with allure.step("Отправляем запрос на создание заказа"):
            r = requests.post(Urls.url_create_order)
        assert r.status_code == 400 and r.json()['message'] == "Ingredient ids must be provided"

    @allure.description('Ошибка при создании заказа с неверным хешем ингредиентов')
    @allure.title('Создание заказа с неверным хешем ингредиентов')
    def test_create_order_invalid_hash_ingridient(self):
        with allure.step("Отправляем запрос на создание заказа"):
            response = requests.post(Urls.url_create_order, headers=Urls.headers, json=Ingredients.incorrect_ingredients_data)
        assert response.status_code == 500 and 'Internal Server Error' in response.text         