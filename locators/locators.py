from selenium.webdriver.common.by import By

class HeaderLocators:
    CONSTRUCTOR = (By.XPATH, "//header//a[.//p[normalize-space()='Конструктор']]")
    FEED = (By.CSS_SELECTOR, 'header a[href="/feed"]')

class ConstructorLocators:
    TITLE = (By.XPATH, "//h1[normalize-space()='Соберите бургер']")
    CARDS = (By.CSS_SELECTOR, 'a[href^="/ingredient/"]')
    BASKET = (By.CSS_SELECTOR, 'section[class*="BurgerConstructor_basket__"]')
    ORDER_BUTTON = (By.XPATH, "//button[normalize-space()='Оформить заказ']")

    @staticmethod
    def card(ingredient_id):
        return By.CSS_SELECTOR, f'a[href="/ingredient/{ingredient_id}"]'

    @staticmethod
    def counter(ingredient_id):
        return By.CSS_SELECTOR, f'a[href="/ingredient/{ingredient_id}"] p[class*="counter_counter__num"]'

class ModalLocators:
    LOADING = (By.CSS_SELECTOR, 'div[class*="Modal_modal_opened"] img[alt="loading animation"]')
    OPEN = (By.CSS_SELECTOR, 'section[class*="Modal_modal_opened"]')
    INGREDIENT_TITLE = (By.XPATH, "//section[contains(@class,'Modal_modal_opened')]//h2[normalize-space()='Детали ингредиента']")
    INGREDIENT_NAME = (By.CSS_SELECTOR, 'section[class*="Modal_modal_opened"] p.text_type_main-medium')
    CLOSE = (By.CSS_SELECTOR, 'section[class*="Modal_modal_opened"] button[class*="Modal_modal__close"]')
    ORDER_NUMBER = (By.CSS_SELECTOR, 'section[class*="Modal_modal_opened"] h2[class*="text_type_digits-large"]')

class LoginLocators:
    EMAIL = (By.XPATH, "//input[@type='text']")
    PASSWORD = (By.XPATH, "//input[@type='password']")
    SUBMIT = (By.XPATH, "//button[normalize-space()='Войти']")

class FeedLocators:
    TITLE = (By.XPATH, "//h1[normalize-space()='Лента заказов']")
    TOTAL = (By.XPATH, "//p[normalize-space()='Выполнено за все время:']/following-sibling::p")
    TODAY = (By.XPATH, "//p[normalize-space()='Выполнено за сегодня:']/following-sibling::p")
    IN_PROGRESS = 'ul[class*="OrderFeed_orderListReady"] li'
    ORDER_NUMBERS = 'a[href^="/feed/"] p.text_type_digits-default'
