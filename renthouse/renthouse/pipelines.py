"Module to use classes"
from itemadapter import ItemAdapter

class RenthousePipeline:
    """pipeline class to clean the data"""
    def process_item(self, item, spider):
        """pipeline method to use an item adapter"""
        adapter = ItemAdapter(item)

        country = adapter.get("country")
        adapter["country"] = country.capitalize()

        address_item = adapter.get("address")
        address = ''.join(address_item).strip()
        adapter["address"] = address

        postal_code = adapter.get("postal_code")
        if postal_code is not None:
            adapter["postal_code"] = postal_code.strip()

        surface_item = adapter.get("surface")
        if surface_item is not None:
            surface = ''.join(surface_item).strip()
            numerical_value = int(surface.split()[0])
            square_meters_int = numerical_value
            adapter["surface"] = f"{square_meters_int} m\u00B2"

        bedrooms_item = adapter.get("bedrooms")
        if bedrooms_item is not None:
            bedrooms = ''.join(bedrooms_item).strip()
            adapter["bedrooms"] = int(bedrooms)

        bath_item = adapter.get("bath")
        if bath_item is not None:
            bathrooms = ''.join(bath_item).strip()
            adapter["bath"] = int(bathrooms)

        pets_item = adapter.get("pet_friendly")
        if pets_item is not None:
            pet_friendly = ''.join(pets_item).strip()
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

        income_item = adapter.get("income_requirement")
        if income_item is not None:
            income_requirement = ''.join(income_item).strip()
            adapter["income_requirement"] = float(income_requirement)

        return item
