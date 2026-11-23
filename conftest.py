import os
import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from helpers.api import TestDataApi
from pages.constructor_page import ConstructorPage
from pages.login_page import LoginPage
from pages.feed_page import FeedPage


def pytest_addoption(parser):
    parser.addoption('--browser', choices=['chrome', 'firefox', 'all'], default='all')
    parser.addoption('--headless', action='store_true', default=False)


def pytest_generate_tests(metafunc):
    if 'browser_name' in metafunc.fixturenames:
        choice = metafunc.config.getoption('--browser')
        browsers = ['chrome', 'firefox'] if choice == 'all' else [choice]
        metafunc.parametrize('browser_name', browsers)


@pytest.fixture
def driver(request, browser_name):
    if browser_name == 'chrome':
        options = webdriver.ChromeOptions()
        if request.config.getoption('--headless'):
            options.add_argument('--headless=new')
        if os.getenv('CHROME_BINARY'):
            options.binary_location = os.environ['CHROME_BINARY']
        # Только для контейнера Linux; на Windows не нужно.
        if os.getenv('CHROME_NO_SANDBOX') == '1':
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
        service = ChromeService(executable_path=os.environ['CHROMEDRIVER']) if os.getenv('CHROMEDRIVER') else ChromeService()
        browser = webdriver.Chrome(options=options, service=service)
    else:
        options = webdriver.FirefoxOptions()
        if request.config.getoption('--headless'):
            options.add_argument('-headless')
        if os.getenv('FIREFOX_BINARY'):
            options.binary_location = os.environ['FIREFOX_BINARY']
        service = FirefoxService(executable_path=os.environ['GECKODRIVER']) if os.getenv('GECKODRIVER') else FirefoxService()
        browser = webdriver.Firefox(options=options, service=service)
    browser.set_window_size(1920, 1080)
    browser.set_page_load_timeout(60)
    allure.dynamic.label('browser', browser_name)
    allure.dynamic.parameter('browser_version', browser.capabilities.get('browserVersion'))
    try:
        yield browser
    finally:
        browser.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.failed and 'driver' in item.funcargs:
        browser = item.funcargs['driver']
        try:
            allure.attach(browser.get_screenshot_as_png(), 'Экран при ошибке', allure.attachment_type.PNG)
            allure.attach(browser.current_url, 'URL при ошибке', allure.attachment_type.TEXT)
        except Exception:
            # Ошибка создания скриншота не должна скрывать исходное падение.
            pass


@pytest.fixture
def data_api():
    api = TestDataApi()
    yield api
    api.session.close()


@pytest.fixture
def ingredients(data_api):
    items = data_api.ingredients()
    return {
        'bun': next(item for item in items if item['type'] == 'bun'),
        'main': next(item for item in items if item['type'] == 'main'),
    }


@pytest.fixture
def user(data_api):
    data = data_api.new_user()
    try:
        data_api.register(data)
        yield data
    finally:
        data_api.cleanup(data)


@pytest.fixture
def constructor(driver):
    return ConstructorPage(driver).open().wait_loaded()


@pytest.fixture
def authorized_constructor(driver, user):
    LoginPage(driver).login(user['email'], user['password'])
    return ConstructorPage(driver).wait_loaded()


@pytest.fixture
def prepared_order(authorized_constructor, ingredients):
    authorized_constructor.add_ingredient(ingredients['bun']['_id'], expected_increase=2)
    authorized_constructor.add_ingredient(ingredients['main']['_id'])
    return authorized_constructor


@pytest.fixture
def observed_feed(driver, prepared_order):
    constructor_tab = driver.current_window_handle
    driver.switch_to.new_window('tab')
    feed_tab = driver.current_window_handle
    feed = FeedPage(driver).open('/feed').wait_loaded()
    feed.observe_orders()
    baseline = {'total': feed.counter('total'), 'today': feed.counter('today')}
    driver.switch_to.window(constructor_tab)
    yield feed, feed_tab, baseline
    # Все вкладки закроются в driver.quit().
