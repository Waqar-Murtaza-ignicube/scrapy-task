"Module to use scrapy and its classes"
import scrapy


class HouseItem(scrapy.Item):
    """class to use scrapy item fields"""
    url = scrapy.Field()
    address = scrapy.Field()
    country = scrapy.Field()
    city = scrapy.Field()
    postal_code = scrapy.Field()
    price = scrapy.Field()
    bedrooms = scrapy.Field()
    surface = scrapy.Field()
    photo = scrapy.Field()
    website = scrapy.Field()
    description = scrapy.Field()
    bath = scrapy.Field()
    furnished = scrapy.Field()
    pet_friendly = scrapy.Field()
    income_requirement = scrapy.Field()
    realtor = scrapy.Field()
    realtor_link = scrapy.Field()
