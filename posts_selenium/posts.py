import random
from selenium import webdriver
from selenium.common import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
from mongo_client import searcj_all
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from parser_exel import list_parse_exel, search_paint


def post_ms_cool():

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

    items = searcj_all()

    for item in items:
        add_item_bt = driver.find_element(By.XPATH, "//a[@class='page-title-action'][1]")

        # Создадим объект ActionChains для выполнения действий с клавишами
        action_chains = ActionChains(driver)

        # Откроем ссылку в новой вкладке (может потребоваться регулировка)
        action_chains.key_down(Keys.CONTROL).click(add_item_bt).key_up(Keys.CONTROL).perform()
        time.sleep(1)

        # Переключимся на новую вкладку
        driver.switch_to.window(driver.window_handles[1])

        title = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='title']"))
        )
        title.send_keys(item['title'])

        if 'content' in item and item['content']:
            try:
                content = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//iframe[@id='content_ifr']"))
                )
                driver.switch_to.frame(content)

                content = driver.find_element(By.XPATH, "//body[@id='tinymce']")
                content.clear()
                content.send_keys(item['content'][0])
                driver.switch_to.default_content()
            except ElementNotInteractableException:
                content_frame = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//iframe[@id='content_ifr']"))
                )
                driver.execute_script("arguments[0].scrollIntoView(true);", content_frame)
                driver.switch_to.frame(content_frame)

                content = driver.find_element(By.XPATH, "//body[@id='tinymce']")
                content.clear()
                content.send_keys(item['content'][0])

                # Вернуться на основную страницу из iframe
                driver.switch_to.default_content()

        if 'description' in item and item['description']:
            description = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//iframe[@id='excerpt_ifr']"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", description)
            description.send_keys(item['description'][0])

        price = driver.find_element(By.XPATH, "//input[@id='_regular_price']")
        driver.execute_script("arguments[0].scrollIntoView(true);", price)
        price.send_keys(item['price'])

        atr_btn = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//ul[@class='product_data_tabs wc-tabs']//li[contains(@class,  'attribute_options')]"))
        )
        # atr_btn = driver.find_element(By.XPATH, "//li[@class='linked_product_options linked_product_tab']//a")
        # driver.execute_script("arguments[0].scrollIntoView(true);", atr_btn)
        atr_btn.click()

        time.sleep(2)

        # add_atr_btn = driver.find_element(By.XPATH, "//button[@class='button add_custom_attribute']")
        add_atr_btn = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, f"//button[@class='button add_custom_attribute']"))
        )


        for indx, atr in enumerate(item['params']):

            name_atr = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, f"//input[@name='attribute_names[{indx}]']"))
            )
            value_atr = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, f"//textarea[@name='attribute_values[{indx}]']"))
            )

            driver.execute_script("arguments[0].scrollIntoView(true);", value_atr)

            name_atr.send_keys(atr['name'])
            value_atr.send_keys(atr['params'])


            # closing = driver.find_elements(By.XPATH, "//div[@class='handlediv']")[-1]
            closing = WebDriverWait(driver, 10).until(
                EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='handlediv']"))
            )

            try:
                closing[-1].click()
            except ElementClickInterceptedException:
                time.sleep(1)
                closing = WebDriverWait(driver, 10).until(
                    EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='handlediv']")))
                driver.execute_script("arguments[0].click();", closing[-1])

            try:
                add_atr_btn.click()
            except ElementClickInterceptedException:
                time.sleep(2)
                driver.execute_script("arguments[0].scrollIntoView(false);", add_atr_btn)
                add_atr_btn.click()

        if 'params_size_out' not in item or not item['params_size_out'] \
                and 'params_size_in' not in item or not item['params_size_in']:
            pass
        else:
            out_checkbox = driver.find_element(By.XPATH, "//input[@id='_vneshnii_checked']")
            driver.execute_script("arguments[0].scrollIntoView(false);", out_checkbox)
            try:
                driver.execute_script("arguments[0].checked = true;", out_checkbox)
            except:
                time.sleep(1)
                out_checkbox.click()

            in_checkbox = driver.find_element(By.XPATH, "//input[@id='_vnutrenii_checked']")
            driver.execute_script("arguments[0].scrollIntoView();", in_checkbox)
            try:
                driver.execute_script("arguments[0].checked = true;", in_checkbox)
            except:
                time.sleep(1)
                in_checkbox.click()
            # driver.execute_script("arguments[0].click();", in_checkbox)

        if 'params_size_out' in item and item['params_size_out']:
            size = driver.find_element(By.XPATH, "//input[@id='_vneshnii_field_1']")
            driver.execute_script("arguments[0].scrollIntoView();", size)
            size.send_keys(item['params_size_out'][0]['size'])

            level_dBa = driver.find_element(By.XPATH, "//input[@id='_vneshnii_field_2']")
            driver.execute_script("arguments[0].scrollIntoView();", level_dBa)
            if 'level_dBa' in item['params_size_out'][0] and item['params_size_out'][0]['level_dBa']:
                level_dBa.send_keys(item['params_size_out'][0]['level_dBa'])

            mass = driver.find_element(By.XPATH, "//input[@id='_vneshnii_field_3']")
            driver.execute_script("arguments[0].scrollIntoView();", mass)
            mass.send_keys(item['params_size_out'][0]['mass'])

        if 'params_size_in' in item and item['params_size_in']:
            size = driver.find_element(By.XPATH, "//input[@id='_vnutrenii_field_1']")
            driver.execute_script("arguments[0].scrollIntoView();", size)
            size.send_keys(item['params_size_in'][0]['size'])

            level_dBa = driver.find_element(By.XPATH, "//input[@id='_vnutrenii_field_2']")
            driver.execute_script("arguments[0].scrollIntoView();", level_dBa)
            if 'level_dBa' in item['params_size_in'][0] and item['params_size_in'][0]['level_dBa']:
                level_dBa.send_keys(item['params_size_in'][0]['level_dBa'])

            mass = driver.find_element(By.XPATH, "//input[@id='_vnutrenii_field_3']")
            driver.execute_script("arguments[0].scrollIntoView();", mass)
            mass.send_keys(item['params_size_in'][0]['mass'])

        # Запасы
        time.sleep(1)
        # stocks = driver.find_element(By.XPATH, "//li[@class='inventory_options inventory_tab show_if_simple show_if_variable show_if_grouped show_if_external']/a")
        stocks = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//ul[@class='product_data_tabs wc-tabs']//li[contains(@class,  'inventory_options')]"))
        )
        driver.execute_script("arguments[0].scrollIntoView(false);", stocks)
        stocks.click()

        vendor_code = driver.find_element(By.XPATH, "//input[@id='_sku']")
        random_number = random.randint(1000000, 9999999)
        vendor_code.send_keys(random_number)

        add_title_photo = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@id='postimagediv']//a"))
        )
        driver.execute_script("arguments[0].scrollIntoView(false);", add_title_photo)
        try:
            add_title_photo.click()
        except ElementClickInterceptedException:
            time.sleep(1)
            driver.execute_script("arguments[0].scrollIntoView(true);", add_title_photo)
            add_title_photo.click()

        chenge_file = driver.find_element(By.XPATH, "//input[@type='file']")

        chenge_file.send_keys(item['photos_path'][0])

        save_btn = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//button[@class='button media-button button-primary button-large media-button-select']"))
        )
        # save_btn = driver.find_element(By.XPATH, "//button[@class='button media-button button-primary button-large media-button-select']")
        time.sleep(4)
        save_btn.click()

        time.sleep(2)

        if item["category"] == "Настенные кондиционеры":
            select_category = driver.find_element(By.XPATH, "//li[@id='product_cat-113']/label")
            # Вызовите JavaScript, чтобы прокрутить страницу к вашему элементу
            driver.execute_script(
                "window.scrollTo(0, arguments[0].getBoundingClientRect().top - window.innerHeight / 2);", select_category)
            try:
                select_category.click()
            except ElementClickInterceptedException:
                print('Категория не выбрана, выберите категорию')
        elif item["category"] == "Мульти сплит системы":
            select_category = driver.find_element(By.XPATH, "//li[@id='product_cat-625']/label")
            # Вызовите JavaScript, чтобы прокрутить страницу к вашему элементу
            driver.execute_script(
                "window.scrollTo(0, arguments[0].getBoundingClientRect().top - window.innerHeight / 2);",
                select_category)
            try:
                select_category.click()
            except ElementClickInterceptedException:
                print('Категория не выбрана, выберите категорию "внутрений блок"')
        elif item["category"] == "Кассетные кондиционеры":
            select_category = driver.find_element(By.XPATH, "//li[@id='product_cat-65']/label")
            # Вызовите JavaScript, чтобы прокрутить страницу к вашему элементу
            driver.execute_script(
                "window.scrollTo(0, arguments[0].getBoundingClientRect().top - window.innerHeight / 2);",
                select_category)
            select_category.click()
        elif item["category"] == "Канальные кондиционеры":
            select_category = driver.find_element(By.XPATH, "//li[@id='product_cat-19']/label")
            # Вызовите JavaScript, чтобы прокрутить страницу к вашему элементу
            driver.execute_script(
                "window.scrollTo(0, arguments[0].getBoundingClientRect().top - window.innerHeight / 2);",
                select_category)
            try:
                WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//li[@id='product_cat-19']/label")))
                select_category.click()
            except:
                print("Не удалось кликнуть на категорию")


        published = driver.find_element(By.XPATH, "//input[@id='publish']")
        published.click()

        if len(item['photos_path']) > 1:
            published = driver.find_element(By.XPATH, "//input[@id='publish']")
            driver.execute_script("arguments[0].scrollIntoView(false);", published)
            published.click()

            time.sleep(2)


            add_photos = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//div[@id='woocommerce-product-images']//a"))
            )
            driver.execute_script("arguments[0].scrollIntoView(false);", add_photos)
            time.sleep(1)
            add_photos.click()
            # driver.execute_script("arguments[0].click();", add_photos)

            try:
                add_files = driver.find_element(By.XPATH, "//input[@type='file']")
            except NoSuchElementException:
                time.sleep(2)
                add_files = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//input[@type='file']"))
                )
                # add_files = driver.find_element(By.XPATH, "//input[@type='file']")

            for img in item['photos_path'][1:4]:
                add_files.send_keys(img)

            time.sleep(6)
            # driver.execute_script("arguments[0].click();", add_btn)
            add_btn = driver.find_element(By.XPATH, "//button[@class='button media-button button-primary button-large media-button-select']")
            try:
                add_btn.click()
            except ElementNotInteractableException:
                add_btn.click()


            published = driver.find_element(By.XPATH, "//input[@id='publish']")
            driver.execute_script("arguments[0].scrollIntoView(false);", published)
            published.click()

        driver.close()

        # Переключимся обратно на предыдущую вкладку
        driver.switch_to.window(driver.window_handles[0])


if __name__ == '__main__':
    post_ms_cool()