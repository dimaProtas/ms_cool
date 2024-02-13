from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from parser_exel import list_parse_exel, search_paint


def parser_ms_cool(path: str, sheet_name: str, skiprows: int = 0, nrows: int = None):

    driver = webdriver.Firefox()
    driver.get(f'https://ms-cool.ru/wp-admin/')

    time.sleep(1)

    user_login = driver.find_element(By.ID, "user_login")
    password = driver.find_element(By.ID, "user_pass")
    button_login = driver.find_element(By.XPATH, "//input[@id='wp-submit']")

    user_login.send_keys('admin')
    password.send_keys('b56qEVIBEp@hzL0sulEnIulB')
    button_login.click()

    items = driver.find_element(By.XPATH, "//div[@class='wp-menu-image dashicons-before dashicons-archive']")
    items.click()

    time.sleep(0.5)

    items = list_parse_exel(path, sheet_name, skiprows, nrows)

    none_items = []

    count_succes = 0

    count_pass = 0

    for item in items:
        search_item = driver.find_element(By.XPATH, "//input[@id='post-search-input']")
        search_item.clear()
        search_item.send_keys(item['name'])

        search_submit = driver.find_element(By.XPATH, "//input[@id='search-submit']")
        search_submit.click()

        time.sleep(0.5)

        try:
            edit = driver.find_element(By.XPATH,
                                       "//tbody[@id='the-list']//a[@class='row-title']")  # //span[@class='edit']/a"
        except NoSuchElementException:
            none_items.append(item)
            search_paint(item['name'], path, sheet_name, 'red')
            continue

        price_previus = (driver.find_element(By.XPATH, "//span[@class='woocommerce-Price-amount amount']").text[:-1]).replace(' ', '')
        if int(price_previus) == item['price']:
            search_paint(item['name'], path, sheet_name, 'yellow')
            count_pass += 1
            continue

        # Создадим объект ActionChains для выполнения действий с клавишами
        action_chains = ActionChains(driver)

        # Откроем ссылку в новой вкладке (может потребоваться регулировка)
        action_chains.key_down(Keys.CONTROL).click(edit).key_up(Keys.CONTROL).perform()
        time.sleep(1)

        # Переключимся на новую вкладку
        driver.switch_to.window(driver.window_handles[1])

        price = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@id='_regular_price']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", price)
        price.clear()
        time.sleep(0.5)
        price.send_keys(item['price'])

        save_button = driver.find_element(By.ID, "publish")
        # driver.execute_script("arguments[0].click();", save_button)
        driver.execute_script("arguments[0].scrollIntoView(false);", save_button)
        save_button.click()

        search_paint(item['name'], path, sheet_name, 'green')

        driver.close()

        count_succes += 1

        # Переключимся обратно на предыдущую вкладку
        driver.switch_to.window(driver.window_handles[0])

    print(f'Изменено цен: {count_succes}\n'
          f'Цена соответсвует: {count_pass}\n'
          f'Не найдено: {len(none_items)}\n'
          f'{none_items}')

    driver.close()


parser_ms_cool('exel/energolux.xlsx', 'Sheet6')
