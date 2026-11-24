import allure
from config import BASE_URL
from locators.locators import ConstructorLocators as L
from pages.base_page import BasePage


class ConstructorPage(BasePage):
    @allure.step('Дождаться загрузки конструктора')
    def wait_loaded(self):
        self.visible(L.TITLE)
        self.visible(L.CARDS)
        return self

    @allure.step('Открыть детали ингредиента')
    def open_ingredient(self, ingredient_id):
        self.scroll_to(L.card(ingredient_id))
        self.click(L.card(ingredient_id))

    @allure.step('Получить счётчик выбранного ингредиента')
    def ingredient_count(self, ingredient_id):
        return self.optional_integer(L.counter(ingredient_id))

    @allure.step('Перетащить ингредиент в конструктор')
    def add_ingredient(self, ingredient_id, expected_increase=1):
        before = self.ingredient_count(ingredient_id)
        self.drag_to(L.card(ingredient_id), L.BASKET)
        self.wait_condition(
            lambda: self.ingredient_count(ingredient_id) == before + expected_increase,
            message='Счётчик ингредиента не увеличился',
        )
        return self

    @allure.step('Оформить заказ через интерфейс')
    def place_order(self):
        self.click(L.ORDER_BUTTON)

    @allure.step('Проверить открытие конструктора')
    def is_open(self):
        self.wait_loaded()
        return self.current_url().rstrip('/') == BASE_URL.rstrip('/')
