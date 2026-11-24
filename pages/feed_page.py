import json
import allure

from config import ORDER_TIMEOUT
from locators.locators import FeedLocators as L
from pages.base_page import BasePage


class FeedPage(BasePage):
    @allure.step('Дождаться загрузки ленты заказов')
    def wait_loaded(self):
        self.visible(L.TITLE)
        self.visible(L.TOTAL)
        return self

    @allure.step('Получить значение счётчика заказов')
    def counter(self, kind):
        locator = L.TOTAL if kind == 'total' else L.TODAY
        return int(self.visible(locator).text.replace(' ', ''))

    @allure.step('Начать наблюдение за номерами на странице ленты')
    def observe_orders(self):
        self.start_feed_observer(L.IN_PROGRESS, L.ORDER_NUMBERS)

    @allure.step('Дождаться своего заказа в ленте: {number}')
    def wait_order_seen(self, number, section='all'):
        try:
            self.wait_condition(
                lambda: self.has_feed_order(section, number),
                timeout=ORDER_TIMEOUT,
                message=f'Заказ {number} не появился в разделе {section}',
            )
        finally:
            allure.attach(
                json.dumps(self.observed_feed_orders()),
                'Номера из DOM ленты',
                allure.attachment_type.JSON,
            )
        return True

    @allure.step('Дождаться увеличения счётчика {kind}')
    def wait_counter_increased(self, kind, previous):
        self.wait_condition(
            lambda: self.counter(kind) > previous,
            timeout=ORDER_TIMEOUT,
            message=f'Счётчик {kind} не увеличился',
        )
        return self.counter(kind)
