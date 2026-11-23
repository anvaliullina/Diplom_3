import allure
from selenium.webdriver.support import expected_conditions as EC
from config import BASE_URL
from locators.locators import LoginLocators as L
from pages.base_page import BasePage

class LoginPage(BasePage):
    def login(self, email, password):
        # Пароль не передаётся в параметры декоратора Allure.
        self.open('/login')
        self.visible(L.EMAIL).send_keys(email)
        self.visible(L.PASSWORD).send_keys(password)
        self.click(L.SUBMIT)
        self.wait.until(EC.url_to_be(BASE_URL + '/'))
