"Module to use scrapy and its classes"
import scrapy
from renthouse.items import HouseItem

class RentSpider(scrapy.Spider):
    """spider class to scrape the web url"""
    name = "rent"
    allowed_domains = ["www.iamexpat.nl"]
    start_urls = ["https://www.iamexpat.nl/housing/rentals"]

    def parse(self, response):
        """parse method to scrape from response of website"""
        property_link = response.css("li.property")
        for link in property_link:
            property_uri = link.css("a.article__link::attr(href)").get()
            items = {
                'website_url': response.url,
                'furnished': link.css("span.label--interior~ span::text").get()
            }
            if property_uri:
                property_page = "https://www.iamexpat.nl" + property_uri

                yield response.follow(property_page, callback=self.property_parser,
                                      cb_kwargs={'items': items})

        next_page = response.css('ul.pager li.pager-current~li a::attr(href)').get()
        if next_page is not None:
            next_page_uri = "https://www.iamexpat.nl" + next_page

            yield response.follow(next_page_uri, callback=self.parse)

    def extract_fields(self, response, field_key):
        """method to merge the same fields functionality"""
        if field_key in ('bedrooms', 'surface'):
            field_value = response.xpath(f"//span[contains(@class,'label--{field_key}')]"
                                         "/../text()")
        else:
            field_value = response.xpath(f"//div[@class='field']/div[contains(text(),'{field_key}'"
                                         ")]/../text()")

        return field_value.getall() if len(field_value) > 1 else None

    def property_parser(self, response, items):
        """parsing the response from property url"""

        # making a dic for items having similar selectors
        field_items = {
            'Address:': 'address',
            'Deposit:': 'deposit',
            'Pets:': 'pets_allowed',
            'Bathrooms:': 'bathrooms',
            'bedrooms': 'bedrooms',
            'surface': 'surface'
        }
        extracted_items = {}
        for field_key, field_value in field_items.items():
            extracted_items[field_value] = self.extract_fields(response, field_key)

        #extracting postal code
        postal_code_avail = ''.join(extracted_items.get('address')).split(",")
        has_postal_code = postal_code_avail[1] if len(postal_code_avail) > 1 else None

        #extracting description
        desc = response.css("div.property__body-section h2")
        desc_p_elements = desc.xpath("//div[contains(text(), 'Description:')]/../../p/text()")

        if desc_p_elements:
            description = desc_p_elements.getall()
        else:
            description = desc.xpath("//div[contains(text(), 'Description:')]"
                                     "/../../text()").getall()

        # making an instance of class
        house_item = HouseItem()

        house_item["url"] = response.url
        house_item["country"] = response.css("li.main__country a::text").get()
        house_item["city"] = response.css(".breadcrumb li.last a::text").get()
        house_item["address"] = extracted_items.get('address')
        house_item["postal_code"] = has_postal_code
        house_item["surface"] = extracted_items.get('surface')
        house_item["bedrooms"] = extracted_items.get('bedrooms')
        house_item["furnished"] = items['furnished']
        house_item["bath"] = extracted_items.get('bathrooms')
        house_item["pet_friendly"] = extracted_items.get('pets_allowed')
        house_item["photo"] = response.css(".gallery img::attr(srcset)").get()
        house_item["price"] = response.css("p.price-wrapper .property__price::text").get()
        house_item["description"] = description
        house_item["income_requirement"] = extracted_items.get('deposit')
        house_item["realtor"] = response.css(".property__main-info a::text").get()
        house_item["realtor_link"] = response.css(".property__main-info a::attr(href)").get()
        house_item["website"] = items['website_url']

        yield house_item
