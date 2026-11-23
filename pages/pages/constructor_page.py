import allure
from selenium.webdriver import ActionChains
from config import BASE_URL
from locators.locators import ConstructorLocators as L
from pages.base_page import BasePage

class ConstructorPage(BasePage):
    def wait_loaded(self):
        self.visible(L.TITLE)
        self.visible(L.CARDS)
        return self

    @allure.step('Открыть детали ингредиента')
    def open_ingredient(self, ingredient_id):
        card = self.visible(L.card(ingredient_id))
        self.driver.execute_script('arguments[0].scrollIntoView({block:"center"});', card)
        self.click(L.card(ingredient_id))

    def ingredient_count(self, ingredient_id):
        elements = self.driver.find_elements(*L.counter(ingredient_id))
        return int(elements[0].text) if elements and elements[0].text else 0

    @allure.step('Перетащить ингредиент в конструктор')
    def add_ingredient(self, ingredient_id, expected_increase=1):
        before = self.ingredient_count(ingredient_id)
        card = self.visible(L.card(ingredient_id))
        self.driver.execute_script('arguments[0].scrollIntoView({block:"center"});', card)
        basket = self.visible(L.BASKET)
        if self.driver.capabilities.get('browserName', '').lower() == 'firefox':
            self.driver.execute_script("""
                const source = arguments[0], target = arguments[1];
                const dataTransfer = new DataTransfer();
                const sourceRect = source.getBoundingClientRect();
                const targetRect = target.getBoundingClientRect();
                function fire(element, type, rect) {
                    element.dispatchEvent(new DragEvent(type, {
                        bubbles: true, cancelable: true, view: window,
                        dataTransfer: dataTransfer,
                        clientX: rect.left + rect.width / 2,
                        clientY: rect.top + rect.height / 2
                    }));
                }
                fire(source, 'dragstart', sourceRect);
                fire(target, 'dragenter', targetRect);
                fire(target, 'dragover', targetRect);
                fire(target, 'drop', targetRect);
                fire(source, 'dragend', targetRect);
            """, card, basket)
        else:
            (ActionChains(self.driver).move_to_element(card).click_and_hold()
             .pause(0.3).move_to_element(basket).pause(0.3).release().perform())
        self.wait.until(lambda _: self.ingredient_count(ingredient_id) == before + expected_increase)
        return self

    @allure.step('Оформить заказ через интерфейс')
    def place_order(self):
        self.click(L.ORDER_BUTTON)

    def is_open(self):
        self.wait_loaded()
        return self.driver.current_url.rstrip('/') == BASE_URL.rstrip('/')

