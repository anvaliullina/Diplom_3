import allure
from pages.constructor_page import ConstructorPage
from pages.feed_page import FeedPage
from pages.modal_page import IngredientModal

@allure.feature('Основная функциональность')
class TestMainFunctionality:
    @allure.title('Переход из ленты заказов в конструктор по ссылке «Конструктор»')
    def test_constructor_navigation(self, driver):
        page = FeedPage(driver).open('/feed').wait_loaded()
        page.go_to_constructor()
        assert ConstructorPage(driver).is_open()

    @allure.title('Переход из конструктора в раздел «Лента заказов»')
    def test_feed_navigation(self, driver, constructor):
        constructor.go_to_feed()
        FeedPage(driver).wait_loaded()
        assert driver.current_url.endswith('/feed')

    @allure.title('Нажатие на ингредиент открывает окно с его деталями')
    def test_ingredient_details_open(self, driver, constructor, ingredients):
        ingredient = ingredients['bun']
        constructor.open_ingredient(ingredient['_id'])
        assert IngredientModal(driver).name() == ingredient['name']

    @allure.title('Крестик закрывает окно деталей ингредиента')
    def test_ingredient_details_close(self, driver, constructor, ingredients):
        constructor.open_ingredient(ingredients['bun']['_id'])
        modal = IngredientModal(driver)
        assert modal.name() == ingredients['bun']['name']
        modal.close()
        assert modal.is_closed()
        constructor.wait_loaded()

    @allure.title('Добавление начинки в конструктор увеличивает её счётчик на один')
    def test_ingredient_counter(self, constructor, ingredients):
        ingredient_id = ingredients['main']['_id']
        before = constructor.ingredient_count(ingredient_id)
        constructor.add_ingredient(ingredient_id)
        assert constructor.ingredient_count(ingredient_id) == before + 1
