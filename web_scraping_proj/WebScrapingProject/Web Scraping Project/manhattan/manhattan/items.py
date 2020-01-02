# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ManhattanItem(scrapy.Item):
    # define the fields for your item here like:
    Property = scrapy.Field()
    Bed = scrapy.Field()
    Bath = scrapy.Field()
    Sqft = scrapy.Field()
    Price = scrapy.Field()
