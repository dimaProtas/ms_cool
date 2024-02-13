from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess

from scrapy_proj import settings
from scrapy_proj.spiders.mircli import MircliSpider


if __name__ == '__main__':
    mir_clima_settings = Settings()
    mir_clima_settings.setmodule(settings)

    process = CrawlerProcess(settings=mir_clima_settings)
    # process.crawl(LabirintSpider)
    process.crawl(MircliSpider)

    process.start()