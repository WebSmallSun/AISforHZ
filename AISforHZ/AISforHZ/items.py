# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class AddressItem(scrapy.Item):
    # fields for address
    address_id      = scrapy.Field()
    address_name    = scrapy.Field()
    area            = scrapy.Field()
    distinct        = scrapy.Field()
    city            = scrapy.Field()
    province        = scrapy.Field()
    country         = scrapy.Field()
    
class CommunityItem(scrapy.Item):
    # fields for community
    comm_id         = scrapy.Field()
    comm_name       = scrapy.Field()
    address_id      = scrapy.Field()
    property_type   = scrapy.Field()
    property_name   = scrapy.Field()
    property_mange_fee = scrapy.Field()
    building_type   = scrapy.Field()
    comm_area       = scrapy.Field()
    households      = scrapy.Field()
    households_comment = scrapy.Field()
    built_date      = scrapy.Field()
    parking_no      = scrapy.Field()
    parking_rate    = scrapy.Field()
    capacity_rate   = scrapy.Field()
    greening_rate   = scrapy.Field()
    developer       = scrapy.Field()
    school          = scrapy.Field()

class AisforhzItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
    
    