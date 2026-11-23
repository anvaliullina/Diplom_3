
import allure
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import ORDER_TIMEOUT
from locators.locators import ModalLocators as L
from pages.base_page import BasePage


class IngredientModal(BasePage):
    def name(self):
        self.visible(L.INGREDIENT_TITLE)
        return self.visible(L.INGREDIENT_NAME).text

    @allure.step('Закрыть детали ингредиента крестиком')
    def close(self):
        self.click(L.CLOSE)
        self.wait.until(EC.invisibility_of_element_located(L.INGREDIENT_TITLE))

    def is_closed(self):
        return not any(
            element.is_displayed()
            for element in self.driver.find_elements(*L.INGREDIENT_TITLE)
        )


class OrderModal(BasePage):
    @allure.step('Дождаться настоящего номера созданного заказа')
    def number(self):
        def real_number(driver):
            for element in driver.find_elements(*L.ORDER_NUMBER):
                try:
                    if not element.is_displayed():
                        continue

                    text = element.text.strip().replace(' ', '').replace('#', '')
                    if not text.isdigit():
                        continue

                    number = int(text)

                    # 9999 — заглушка, а не настоящий номер заказа.
                    if number > 0 and number != 9999:
                        return number

                except StaleElementReferenceException:
                    continue

            return False

        return WebDriverWait(
            self.driver,
            ORDER_TIMEOUT,
            poll_frequency=0.5,
        ).until(
            real_number,
            'Не появился настоящий номер заказа: на экране всё ещё 9999 или пусто',
        )

    def close(self):
        self.click(L.CLOSE)
        self.wait.until(EC.invisibility_of_element_located(L.ORDER_NUMBER))
