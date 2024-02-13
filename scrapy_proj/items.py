# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import re
import scrapy
from itemloaders.processors import MapCompose, TakeFirst, Compose


def cleaner_price(value):
    if value:
        numbers = re.findall(r'\d+', value[0].replace(' ', ''))
        return int(numbers[0])
    return None


def cleaner_text(value):
    if value:
        res = ' '.join(value)
        return res
    return None


def clean_param_size(value):
    if value:
        el_dict = {}
        clean_value = [val for val in value if val != '?']
        print(1)
        for x in range(0, len(clean_value), 2):
            name = clean_value[x].strip()
            value = clean_value[x + 1].strip()
            if name == '' or value == '':
                continue
            elif name.split(',')[0] == 'Уровень шума':
                el_dict['level_dBa'] = value
            elif name.split(',')[0] == 'Габариты (ВхШхГ)':
                el_dict['size'] = f'{value} {name.split(",")[1]}'
            elif name.split(',')[0] == 'Вес':
                el_dict['mass'] = value

        return el_dict


def cleaner_params(value):
    if value:
        res = []
        clean_value = [val for val in value if val != '?']
        for x in range(0, len(clean_value), 2):
            if clean_value[x].strip() == '' or clean_value[x + 1].strip() == '':
                continue
            el = {
                'name': clean_value[x].strip(),
                'params': clean_value[x + 1].strip()
            }
            res.append(el)
        return res



class ScrapyProjItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field(output_processor=TakeFirst())
    category = scrapy.Field(output_processor=TakeFirst())
    content = scrapy.Field(input_processor=Compose(cleaner_text))
    description = scrapy.Field(input_processor=Compose(cleaner_text))
    params = scrapy.Field(input_processor=Compose(cleaner_params))
    params_size_in = scrapy.Field(input_processor=Compose(clean_param_size))
    params_size_out = scrapy.Field(input_processor=Compose(clean_param_size))
    price = scrapy.Field(output_processor=TakeFirst(), input_processor=Compose(cleaner_price))
    photos = scrapy.Field(input_processor=Compose())
    photos_path = scrapy.Field()
    photos_link = scrapy.Field()
    _id = scrapy.Field()
