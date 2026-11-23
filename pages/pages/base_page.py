import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import BASE_URL, WAIT_TIMEOUT
from locators.locators import HeaderLocators

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, WAIT_TIMEOUT)

    def open(self, path='/'):
        self.driver.get(BASE_URL + path)
        return self

    def visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    @allure.step('Перейти по ссылке «Конструктор»')
    def go_to_constructor(self):
        self.click(HeaderLocators.CONSTRUCTOR)

    @allure.step('Перейти по ссылке «Лента заказов»')
    def go_to_feed(self):
        self.click(HeaderLocators.FEED)
