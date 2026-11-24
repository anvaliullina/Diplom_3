import allure
from locators.locators import ModalLocators as L
from pages.base_page import BasePage


class IngredientModal(BasePage):
    @allure.step('Получить имя ингредиента в модальном окне')
    def name(self):
        self.visible(L.INGREDIENT_TITLE)
        return self.visible(L.INGREDIENT_NAME).text

    @allure.step('Закрыть детали ингредиента крестиком')
    def close(self):
        self.click(L.CLOSE)
        self.wait_invisible(L.INGREDIENT_TITLE)

    @allure.step('Проверить закрытие модального окна')
    def is_closed(self):
        return not self.has_visible_elements(L.INGREDIENT_TITLE)


class OrderModal(BasePage):
    @allure.step('Дождаться настоящего номера созданного заказа')
    def number(self):
        return self.wait_real_order_number(L.ORDER_NUMBER)

    @allure.step('Закрыть модальное окно заказа')
    def close(self):
        self.click(L.CLOSE)
        self.wait_invisible(L.ORDER_NUMBER)
