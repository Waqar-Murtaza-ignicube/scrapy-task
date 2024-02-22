"Module to use scrapy and its classes"
import scrapy
from renthouse.items import HouseItem

class RentSpider(scrapy.Spider):
    """spider class to scrape the web url"""
    name = "rent"
    allowed_domains = ["www.iamexpat.nl"]
    start_urls = ["https://www.iamexpat.nl/housing/rentals"]

    def parse(self, response):

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

    def property_parser(self, response, items):
        """parsing the response from property url"""
        postal_code = response.xpath("//div[@class='field']/div[contains(text(),'Address:')]"
                                     "/../text()")
        postal_code_avail = postal_code[1].get().split(",")
        has_postal_code = postal_code_avail[1] if len(postal_code_avail) > 1 else None

        deposit = response.xpath("//div[@class='field']/div[contains(text(),'Deposit:')]/../text()")
        has_deposit = deposit[1].get().strip() if len(deposit) > 1 else None

        pets_allowed = response.xpath("//div[@class='field']/div[contains(text(),'Pets:')]"
                                      "/../text()")
        has_pets = pets_allowed[1].get().strip() if len(pets_allowed) > 1 else None

        bathrooms = response.xpath("//div[contains(text(),'Bathrooms:')]/../text()")
        has_baths = bathrooms[1].get().strip() if len(bathrooms) > 1 else None

        bedrooms = response.css(".field:has(span.label--bedrooms)::text")
        has_bedrooms = bedrooms[1].get().strip() if len(bedrooms) > 1 else None

        surface = response.css(".field:has(span.label--surface)::text")
        has_surface = surface[1].get().strip() if len(surface) > 1 else None


        desc = response.css("div.property__body-section h2")
        desc_p_elements = desc.xpath("//div[contains(text(), 'Description:')]/../../p/text()")

        if desc_p_elements:
            description = desc_p_elements
        else:
            description = desc.xpath("//div[contains(text(), 'Description:')]"
                                     "/../../text()").getall()

        # making an instance of class
        house_item = HouseItem()

        house_item["url"] = response.url
        house_item["country"] = response.css("li.main__country a::text").get()
        house_item["city"] = response.css(".breadcrumb li.last a::text").get()
        house_item["address"] = response.xpath("//div[contains(text(),'Address:')]"
                                               "/../text()")[1].get()
        house_item["postal_code"] = has_postal_code
        house_item["surface"] = has_surface
        house_item["bedrooms"] = has_bedrooms
        house_item["furnished"] = items['furnished']
        house_item["bath"] = has_baths
        house_item["pet_friendly"] = has_pets
        house_item["photo"] = response.css(".gallery img::attr(srcset)").get()
        house_item["price"] = response.css("p.price-wrapper .property__price::text").get()
        house_item["description"] = description
        house_item["income_requirement"] = has_deposit
        house_item["realtor"] = response.css(".property__main-info a::text").get()
        house_item["realtor_link"] = response.css(".property__main-info a::attr(href)").get()
        house_item["website"] = items['website_url']

        yield house_item
