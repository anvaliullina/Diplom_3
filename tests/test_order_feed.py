import allure
import pytest
from pages.modal_page import OrderModal

@allure.feature('Лента заказов')
class TestOrderFeed:
    @pytest.mark.parametrize('counter', ['total', 'today'], ids=['all_time', 'today'])
    @allure.title('После оформления заказа увеличивается счётчик ленты: {counter}')
    def test_completed_counter_increases(self, driver, prepared_order, observed_feed, counter):
        feed, feed_tab, baseline = observed_feed
        prepared_order.place_order()
        number = OrderModal(driver).number()
        allure.dynamic.parameter('created_order_number', number)
        driver.switch_to.window(feed_tab)
        # Проверяем и появление собственного заказа, и рост счётчика.
        assert feed.wait_order_seen(number)
        assert feed.wait_counter_increased(counter, baseline[counter]) > baseline[counter]

    @allure.title('Номер оформленного заказа появляется в разделе «В работе»')
    def test_new_order_in_progress(self, driver, prepared_order, observed_feed):
        feed, feed_tab, _ = observed_feed
        prepared_order.place_order()
        number = OrderModal(driver).number()
        allure.dynamic.parameter('created_order_number', number)
        driver.switch_to.window(feed_tab)
        assert feed.wait_order_seen(number, section='progress')
