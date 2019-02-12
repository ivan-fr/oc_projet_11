from .utils import return_urllib_request
from config import GOOGLE_API_KEY

GEOLOCATE_URL = "https://maps.googleapis.com/maps/api/geocode/json"


def get_geolocate_response(address, from_country=None):
    """Communicate with the google map API for get
    data from a given adress."""

    params = {
        "address": address,
        "key": GOOGLE_API_KEY,
        "language": "fr",
    }

    if from_country:
        params["components"] = "country:" + from_country

    _dict = return_urllib_request(GEOLOCATE_URL, params)

    assert 'status' in _dict.keys() and _dict['status'] == "OK"

    return _dict


def parse_geolocate_response(address, from_country=None):
    """Get Parsed google maps request"""

    _dict = get_geolocate_response(address, from_country)

    result = _dict['results'][0]
    return {
        "asked_address": address,
        "formatted_address": result['formatted_address'],
        "location": result['geometry']['location'],
        "bounds": result['geometry']['viewport'],
        "place_id": result['place_id']
    }
