# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import re
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


def decode_unicode(value):
    if value is not None:
        value = value.encode('ascii', 'ignore')
        value = value.decode()
    return value

def list_str(value):
    if isinstance(value, list):
        vals = ""
        for i in value:
            vals += f" {i}"
        return vals.strip()

    return value

def date(value):
    if isinstance(value, datetime.date):
        # value = datetime.isoformat(value)
        value = value.strftime("%Y-%m-%d")
    return value

def strip_spaces(value):
    return value.strip()

def website(value):
    match_obj = re.search("www\..*\.[a-z]{3}", value)
    if match_obj:
        return match_obj.group(0)

class JobsItem(scrapy.Item):
    id = scrapy.Field(input_processor=MapCompose(remove_tags, replace_escape_chars), output_processor=TakeFirst())
 #url for the job advert itself
    url = scrapy.Field(output_processor=TakeFirst())
 #the job title
    title = scrapy.Field(
        input_processor=MapCompose(remove_tags, replace_entities, replace_escape_chars, strip_spaces, decode_unicode),
        output_processor=TakeFirst(),
    )
#the link on the organisation's website which takes the user to the application process. Eg often an 'apply here' button 
    application_url = scrapy.Field(output_processor=TakeFirst())
    date_created = scrapy.Field(
        input_processor=MapCompose(replace_escape_chars), output_processor=TakeFirst()
    )
    
  #the date when the job ad closes
    date_closing = scrapy.Field(
        input_processor=MapCompose(date, replace_escape_chars, remove_tags), 
        output_processor=TakeFirst()
    )
 #the bulk description of the role - ie what it consists of, skills required, details of the position. Scrape in html format
    description = scrapy.Field(
        input_processor=MapCompose(replace_escape_chars, decode_unicode),
        output_processor=TakeFirst(),
    )
  #specific to categories on intdevjob.com. Often will not be possible to scrape
    category = scrapy.Field(
        input_processor=MapCompose(remove_tags, replace_escape_chars, decode_unicode), output_processor=TakeFirst()
    )
    location = scrapy.Field(
        input_processor=MapCompose(list_str, remove_tags, replace_escape_chars),
        output_processor=TakeFirst()
    )
    #full time, part time, etc. See https://app.jboard.io/api/documentation
    contract_type = scrapy.Field(
        input_processor=MapCompose(remove_tags, replace_escape_chars, decode_unicode), output_processor=TakeFirst()
    )
    contract_type_jboard = scrapy.Field(output_processor=TakeFirst())
    salary = scrapy.Field(
        input_processor=MapCompose(decode_unicode), output_processor=TakeFirst()
    )
    #name of the organisation
    organisation = scrapy.Field(input_processor=MapCompose(remove_tags, replace_escape_chars, decode_unicode), output_processor=TakeFirst())
    #organisation's website
    website = scrapy.Field(input_processor=MapCompose(remove_tags, replace_escape_chars, decode_unicode, website), output_processor=TakeFirst())
    # wp_logo = scrapy.Field(output_processor=TakeFirst())
    #jboard allocated no.
    employer_id_jboard = scrapy.Field(output_processor=TakeFirst())
