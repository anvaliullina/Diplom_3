import allure
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from config import BASE_URL, WAIT_TIMEOUT, ORDER_TIMEOUT
from locators.locators import HeaderLocators


class BasePage:
    """Единое место для прямой работы с WebDriver и явными ожиданиями."""

    @allure.step('Инициализировать базовую страницу')
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, WAIT_TIMEOUT)

    @allure.step('Открыть страницу')
    def open(self, path='/'):
        self.driver.get(BASE_URL + path)
        return self

    @allure.step('Дождаться видимости элемента')
    def visible(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    @allure.step('Нажать на элемент')
    def click(self, locator):
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    @allure.step('Дождаться скрытия элемента')
    def wait_invisible(self, locator):
        return self.wait.until(EC.invisibility_of_element_located(locator))

    @allure.step('Дождаться адреса страницы')
    def wait_url(self, url):
        return self.wait.until(EC.url_to_be(url))

    @allure.step('Получить текущий адрес страницы')
    def current_url(self):
        return self.driver.current_url

    @allure.step('Найти элементы страницы')
    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    @allure.step('Проверить наличие видимых элементов')
    def has_visible_elements(self, locator):
        try:
            return any(element.is_displayed() for element in self.find_elements(locator))
        except StaleElementReferenceException:
            return False

    @allure.step('Получить числовое значение элемента')
    def optional_integer(self, locator):
        elements = self.find_elements(locator)
        return int(elements[0].text) if elements and elements[0].text else 0

    @allure.step('Прокрутить страницу до элемента')
    def scroll_to(self, locator):
        element = self.visible(locator)
        self.driver.execute_script('arguments[0].scrollIntoView({block:"center"});', element)
        return element

    @allure.step('Дождаться выполнения условия')
    def wait_condition(self, predicate, timeout=WAIT_TIMEOUT, message='Условие не выполнено'):
        return WebDriverWait(self.driver, timeout).until(lambda _: predicate(), message)

    @allure.step('Перетащить элемент')
    def drag_to(self, source_locator, target_locator):
        source = self.scroll_to(source_locator)
        target = self.visible(target_locator)
        if self.driver.capabilities.get('browserName', '').lower() == 'firefox':
            self.driver.execute_script(r"""
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
            """, source, target)
        else:
            (ActionChains(self.driver).move_to_element(source).click_and_hold()
             .pause(0.3).move_to_element(target).pause(0.3).release().perform())

    @allure.step('Дождаться реального номера заказа')
    def wait_real_order_number(self, locator):
        """Пропускает временную заглушку 9999 до появления реального номера."""
        def real_number(driver):
            for element in driver.find_elements(*locator):
                try:
                    if not element.is_displayed():
                        continue
                    text = element.text.strip().replace(' ', '').replace('#', '')
                    if text.isdigit():
                        number = int(text)
                        if number > 0 and number != 9999:
                            return number
                except StaleElementReferenceException:
                    continue
            return False

        return WebDriverWait(self.driver, ORDER_TIMEOUT, poll_frequency=0.5).until(
            real_number, 'Не появился настоящий номер заказа: 9999 либо пустое значение',
        )

    @allure.step('Начать наблюдение за номерами заказов в ленте')
    def start_feed_observer(self, in_progress_selector, all_orders_selector):
        """Сохраняет кратковременные номера заказов из DOM ленты."""
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
        """, in_progress_selector, all_orders_selector)

    @allure.step('Проверить появление номера заказа в ленте')
    def has_feed_order(self, section, number):
        return self.driver.execute_script(
            'return (window.qaFeedSeen && window.qaFeedSeen[arguments[0]] || []).includes(arguments[1]);',
            section, number,
        )

    @allure.step('Получить замеченные в ленте номера заказов')
    def observed_feed_orders(self):
        return self.driver.execute_script('return window.qaFeedSeen || {progress: [], all: []};')

    @allure.step('Перейти по ссылке «Конструктор»')
    def go_to_constructor(self):
        self.click(HeaderLocators.CONSTRUCTOR)

    @allure.step('Перейти по ссылке «Лента заказов»')
    def go_to_feed(self):
        self.click(HeaderLocators.FEED)
