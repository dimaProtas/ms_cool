# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
from pathlib import Path


class ScrapyProjPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.mirClima

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        # print(item["title"], '\n', item["price"], '\n', item['content'], '\n', item['description'], '\n', item['params'])
        item['photos_path'] = [f"{Path().resolve()}/images/{i['path']}" for i in item['photos']]
        item['photos_link'] = [i['url'] for i in item['photos']]
        collection.insert_one(item)
        return item

class MirClimaPhotosPipline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            n = 1
            for img in item['photos']:
                try:
                    yield scrapy.Request(img, meta={'name': item['title'].replace(' ', '_'), 'file': f'file_{str(n)}'})
                    n += 1
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        item['photos'] = [itm for ok, itm in results if ok]
        return item

    def file_path(self, request, response=None, info=None, *, item=None):
        return f'{request.meta["name"]}/{request.meta["file"]}.jpg'