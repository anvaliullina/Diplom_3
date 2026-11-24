# Задание 3 — UI Stellar Burgers

Page Object: pages/base_page.py, constructor_page.py, login_page.py,
modal_page.py, feed_page.py. Все локаторы в locators/locators.py.
Тесты не содержат XPath/CSS и не обращаются напрямую к элементам.
Восемь требуемых сценариев × Chrome/Firefox = 16 запусков.

| Требование | Тест |
|---|---|
| Переход «Конструктор» | test_constructor_navigation |
| Переход «Лента заказов» | test_feed_navigation |
| Открытие деталей ингредиента | test_ingredient_details_open |
| Закрытие деталей крестиком | test_ingredient_details_close |
| Рост счётчика ингредиента | test_ingredient_counter |
| Рост «Выполнено за всё время» | test_completed_counter_increases[all_time] |
| Рост «Выполнено за сегодня» | test_completed_counter_increases[today] |
| Свой номер в «В работе» | test_new_order_in_progress |

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest --browser all --clean-alluredir
allure generate allure-results --clean -o allure-report
allure open allure-report
```

Только Chrome: `python -m pytest --browser chrome`.
Только Firefox: `python -m pytest --browser firefox`.
Без видимого окна: добавить `--headless`.
Если между отдельными прогонами Chrome и Firefox НЕ указывать --clean-alluredir,
результаты обоих окажутся в общем отчёте. Для полного свежего запуска используй --browser all.

Тестовые пользователи создаются через API и удаляются в teardown.
Сам вход, добавление ингредиентов и оформление заказа выполняются через UI.
Каждый тест получает отдельный браузер, данные и пользователя (где он нужен).
Используются явные ожидания, без time.sleep. Паузы в ActionChains — часть жеста drag-and-drop.
Скриншот при ошибке автоматически попадает в Allure.

## Лента и кратковременный статус «В работе»

До нажатия «Оформить заказ» открывается вторая вкладка с лентой.
MutationObserver записывает номера, реально появившиеся в DOM ленты, пока заказ оформляется
в первой вкладке. Это позволяет не потерять кратковременный статус при переключении вкладок.
Не используются внутреннее состояние React или API вместо проверки UI.
Тест «В работе» проверяет номер именно в списке справа от соответствующего заголовка,
а не просто наличие номера где-либо на странице.

Публичные счётчики общие: другие студенты тоже создают заказы. Поэтому проверяем рост `>`,
а не строго `+1`, и отдельно дожидаемся собственного номера в ленте.
Это не доказывает, что никакой другой заказ не повлиял на счётчик; полностью изолировать
причину роста можно только на отдельном стенде. Полночь/сброс дневного счётчика — повод
повторить сценарий в стабильное время, не менять assert.

## Проверенность и ограничения

Python-файлы компилируются; pytest собирает все 16 тестов.
Локаторы сверены с загруженным кодом текущего фронтенда.
В среде подготовки browser session не стартовала из-за ограничений контейнера
(`socket() failed: Operation not permitted`); Firefox здесь отсутствует.
**Прогона сценариев в реальных Chrome/Firefox пока нет.**
Первый реальный запуск нужно выполнить на Windows. При изменении интерфейса корректируем
локаторы, при особенностях drag-and-drop — только метод ConstructorPage.add_ingredient.
Падающие тесты не пропускаются автоматически.

Selenium Manager скачивает подходящие драйверы. Если сеть блокирует загрузку, можно указать:
`$env:CHROMEDRIVER = "C:\drivers\chromedriver.exe"`
или `$env:GECKODRIVER = "C:\drivers\geckodriver.exe"`.
Для нестандартной установки доступны CHROME_BINARY/FIREFOX_BINARY.
Обычным пользователям Windows CHROME_NO_SANDBOX не нужен.

Ветка для сдачи: develop3, отдельный репозиторий и PR.
