import json
import allure
from selenium.webdriver.support.ui import WebDriverWait
from config import ORDER_TIMEOUT
from locators.locators import FeedLocators as L
from pages.base_page import BasePage

class FeedPage(BasePage):
    def wait_loaded(self):
        self.visible(L.TITLE)
        self.visible(L.TOTAL)
        return self

    def counter(self, kind):
        locator = L.TOTAL if kind == 'total' else L.TODAY
        return int(self.visible(locator).text.replace(' ', ''))

    @allure.step('Начать наблюдение за номерами на странице ленты')
    def observe_orders(self):
        # Только DOM страницы: сохраняем кратковременные появления номеров.
        # Вторую вкладку открываем ДО заказа, чтобы не пропустить «В работе».
        self.driver.execute_script(r"""
            if (window.qaFeedObserver) window.qaFeedObserver.disconnect();
            window.qaFeedSeen = {progress: [], all: []};
            const collect = () => {
                for (const [key, selector] of [['progress', arguments[0]], ['all', arguments[1]]]) {
                    document.querySelectorAll(selector).forEach(node => {
                        const text = node.textContent.trim().replace(/^#/, '');
                        if (/^\d+$/.test(text)) {
                            const number = Number(text);
                            if (!window.qaFeedSeen[key].includes(number)) window.qaFeedSeen[key].push(number);
                        }
                    });
                }
            };
            window.qaFeedObserver = new MutationObserver(collect);
            window.qaFeedObserver.observe(document.body, {childList:true, subtree:true, characterData:true});
            collect();
        """, L.IN_PROGRESS, L.ORDER_NUMBERS)

    @allure.step('Дождаться своего заказа в ленте: {number}')
    def wait_order_seen(self, number, section='all'):
        def seen(_):
            return self.driver.execute_script(
                'return (window.qaFeedSeen && window.qaFeedSeen[arguments[0]] || []).includes(arguments[1]);',
                section, number,
            )
        try:
            WebDriverWait(self.driver, ORDER_TIMEOUT).until(seen, f'Заказ {number} не появился в разделе {section}')
        finally:
            allure.attach(json.dumps(self.driver.execute_script('return window.qaFeedSeen;')), 'Номера из DOM ленты', allure.attachment_type.JSON)
        return True

    @allure.step('Дождаться увеличения счётчика {kind}')
    def wait_counter_increased(self, kind, previous):
        WebDriverWait(self.driver, ORDER_TIMEOUT).until(lambda _: self.counter(kind) > previous)
        return self.counter(kind)
