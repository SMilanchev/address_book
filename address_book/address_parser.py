from geopy import Nominatim, location

locator = Nominatim(user_agent="myGeocoder")


def parse_address(address: str) -> location.Location | None:
    locator_object = locator.geocode(address, language='en', exactly_one=True)
    if locator_object:
        if locator_object.latitude and locator_object.longitude:
            return locator_object

