"Module to use classes"
from itemadapter import ItemAdapter

class RenthousePipeline:
    """pipeline class to clean the data"""
    def process_item(self, item, spider):
        """pipeline method to use an item adapter"""
        adapter = ItemAdapter(item)

        country = adapter.get("country")
        adapter["country"] = country.capitalize()

        address = adapter.get("address")
        adapter["address"] = address.strip()

        postal_code = adapter.get("postal_code")
        if postal_code is not None:
            adapter["postal_code"] = postal_code.strip()

        surface = adapter.get("surface")
        if surface is not None:
            numerical_value = int(surface.split()[0])
            square_meters_int = numerical_value
            adapter["surface"] = f"{square_meters_int} m\u00B2"

        bedrooms = adapter.get("bedrooms")
        if bedrooms is not None:
            adapter["bedrooms"] = int(bedrooms)

        pet_friendly = adapter.get("pet_friendly")
        if pet_friendly == "Not allowed":
            adapter["pet_friendly"] = "No"
        elif pet_friendly == "Allowed":
            adapter["pet_friendly"] = "Yes"

        photo = adapter.get("photo")
        adapter["photo"] = photo.split(" ")[0]

        price = adapter.get("price")
        price_value = price.replace("€", "")
        adapter["price"] = float(price_value)

        description = adapter["description"]
        adapter["description"] = ' '.join(space.strip() for space in description if space.strip())

        income_requirement = adapter.get("income_requirement")
        if income_requirement is not None:
            adapter["income_requirement"] = float(income_requirement)

        return item
