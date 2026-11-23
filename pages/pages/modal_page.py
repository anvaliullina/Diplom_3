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
        return not any(element.is_displayed() for element in self.driver.find_elements(*L.INGREDIENT_TITLE))

class OrderModal(BasePage):
    @allure.step('Дождаться номера созданного заказа')
    def number(self):
        def real_number(driver):
            # 9999 — начальное значение в модальном окне до получения
            # реального номера от сервера. Проверка одной лишь анимации
            # ненадёжна: иногда она уже скрыта, а 9999 ещё отображается.
            if any(element.is_displayed() for element in driver.find_elements(*L.LOADING)):
                return False
            elements = driver.find_elements(*L.ORDER_NUMBER)
            for element in elements:
                text = element.text.strip()
                if element.is_displayed() and text.isdigit():
                    number = int(text)
                    if number > 0 and number != 9999:
                        return number
            return False
        return WebDriverWait(
            self.driver, ORDER_TIMEOUT,
            ignored_exceptions=(StaleElementReferenceException,),
        ).until(
            real_number,
            "В модальном окне не появился реальный номер заказа: отображается 9999 (заглушка) либо номер отсутствует",
        )

    def close(self):
        self.click(L.CLOSE)
        self.wait.until(EC.invisibility_of_element_located(L.ORDER_NUMBER))
