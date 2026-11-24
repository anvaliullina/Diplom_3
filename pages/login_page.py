import allure
from config import BASE_URL
from locators.locators import LoginLocators as L
from pages.base_page import BasePage


class LoginPage(BasePage):
    @allure.step('Войти под тестовым пользователем')
    def login(self, email, password):
        # Не записываем пароль в аргументы шага Allure.
        with allure.step('Войти в приложение под тестовым пользователем'):
            self.open('/login')
            self.visible(L.EMAIL).send_keys(email)
            self.visible(L.PASSWORD).send_keys(password)
            self.click(L.SUBMIT)
            self.wait_url(BASE_URL + '/')
