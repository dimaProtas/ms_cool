import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from scrapy_proj.items import ScrapyProjItem
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from parser_exel import list_parse_exel


class MircliSpider(scrapy.Spider):
    name = "mircli"
    allowed_domains = ["mircli.ru"]
    start_urls = ["https://mircli.ru/"]

    def parse(self, response):
        items = [{'name': 'SIR-I07PN', 'price': 27590}, {'name': 'SIR-I09PN', 'price': 29790}, {'name': 'SIR-I12PN', 'price': 34190}, {'name': 'SIR-I18PN', 'price': 55090}, {'name': 'ECS-I07PN', 'price': 24990}, {'name': 'ECS-I09PN', 'price': 26890}, {'name': 'ECS-I12PN', 'price': 30990}, {'name': 'ECS-I18PN', 'price': 40590}, {'name': 'ECS-I24PN', 'price': 50890}, {'name': 'SIR-07PN', 'price': 17190}, {'name': 'SIR-09PN', 'price': 19090}, {'name': 'SIR-12PN', 'price': 25490}, {'name': 'ECS-07PN', 'price': 16690}, {'name': 'ECS-09PN', 'price': 18390}, {'name': 'ECS-12PN', 'price': 24390}, {'name': 'ECS-18PN', 'price': 42190}, {'name': 'ECS-24PN', 'price': 52990}]

        for item in items:
            yield response.follow(f'https://mircli.ru/search?keyword={item["name"]}', callback=self.product_parse)


    def product_parse(self, response: HtmlResponse):
        links_product = response.xpath("//div[@class='product_name']/a/@href").extract_first()
        yield response.follow(links_product, callback=self.product)
        # print(1)

    def product(self, response: HtmlResponse):
        loader = ItemLoader(item=ScrapyProjItem(), response=response)
        loader.add_xpath("title", "//span[@class='product-name']//text()")
        loader.add_xpath("category", "//ul[@class='main-menu main-menu-breadcrumbs']/li[2]//text()")
        # loader.add_xpath("content", "//div[@class='show-more-block-new']/p[1]//text() |  //div[@class='show-more-block-new']//div/p//text()")
        loader.add_xpath("content", "//div[contains(@class, 'show-more-block-new')]/p[1]//text() |  //div[contains(@class, 'show-more-block-new')]/p[3]//text()")
        loader.add_xpath("description", "//div[@class='show-more-block-new']//ul//text()")
        loader.add_xpath("params", "//div[@class='col-lg-12 col-md-12 col-sm-24 col-xs-24 without-mobile-3605'][1]//text()")
        loader.add_xpath("params_size_in", "//div[@class='col-lg-12 col-md-12 col-sm-24 col-xs-24 without-mobile-3605'][2]//ul[@class='menu-dot']//text()")
        loader.add_xpath("params_size_out", "//div[@class='col-lg-12 col-md-12 col-sm-24 col-xs-24 without-mobile-3605'][3]//ul[@class='menu-dot']//text()")
        loader.add_xpath("price", "//div[@class='col-lg-7 col-md-7 col-sm-12 col-xs-24']//span[@class='price']//text()")
        # loader.add_xpath('photos', "//div[@class='swiper-container gallery-thumbs swiper-container-horizontal']//div[contains(@class, 'swiper-slide')]//img/@src")

        driver = webdriver.Firefox()
        actions = ActionChains(driver)
        driver.get(response.url)

        thumbs = driver.find_elements(By.XPATH, "//div[@class='swiper-container gallery-thumbs swiper-container-horizontal']//div[contains(@class, 'swiper-slide')]")

        photos = [i.find_element(By.XPATH, ".//img").get_attribute('src') for i in thumbs]

        driver.quit()
        photos.pop()

        loader.add_value('photos', photos)
        print(1)
        yield loader.load_item()
        # print(1)