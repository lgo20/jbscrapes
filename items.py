# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import (
    remove_tags,
    replace_escape_chars,
    remove_entities,
    replace_entities,
)
import datetime


def clear(value):
    if isinstance(value, str):
        value = value.replace("\xa0", " ")
        value = value.strip()
    return value


def date(value):
    if isinstance(value, datetime.date):
        # value = datetime.isoformat(value)
        value = value.strftime("%Y-%m-%d")
    return value


class JobsItem(scrapy.Item):
    id = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(
        input_processor=MapCompose(remove_tags, replace_entities, clear),
        output_processor=TakeFirst(),
    )
    application_url = scrapy.Field(output_processor=TakeFirst())
    date_created = scrapy.Field(
        input_processor=MapCompose(date), output_processor=TakeFirst()
    )
    date_closing = scrapy.Field(
        input_processor=MapCompose(date), output_processor=TakeFirst()
    )
    description = scrapy.Field(
        input_processor=MapCompose(remove_tags, replace_entities, clear),
        output_processor=TakeFirst(),
    )
    category = scrapy.Field(
        input_processor=MapCompose(remove_tags, clear), output_processor=TakeFirst()
    )
    location = scrapy.Field(
        input_processor=MapCompose(clear), output_processor=TakeFirst()
    )
    contract_type = scrapy.Field(
        input_processor=MapCompose(remove_tags, clear), output_processor=TakeFirst()
    )
    contract_type_jboard = scrapy.Field(output_processor=TakeFirst())
    salary = scrapy.Field(
        input_processor=MapCompose(clear), output_processor=TakeFirst()
    )
    organisation = scrapy.Field(output_processor=TakeFirst())
    website = scrapy.Field(output_processor=TakeFirst())
    # wp_logo = scrapy.Field(output_processor=TakeFirst())
    employer_id_jboard = scrapy.Field(output_processor=TakeFirst())
