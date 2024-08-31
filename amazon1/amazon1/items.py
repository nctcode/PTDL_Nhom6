# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Amazon1Item(scrapy.Item):
    productName = scrapy.Field()
    brand = scrapy.Field()
    productDescription = scrapy.Field()
    countryOfOrigin =scrapy.Field()
    price = scrapy.Field()
    typicalPrice = scrapy.Field()
    boughtInPastMonth = scrapy.Field()
    comment = scrapy.Field()
    rate = scrapy.Field()
    star = scrapy.Field()
    productUrl = scrapy.Field()