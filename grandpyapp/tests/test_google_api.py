import pytest
import json
import urllib.request
from io import BytesIO
from grandpyapp.managers.googlemaps import get_geolocate_response, \
    parse_geolocate_response


class TestGoogleMapsApi:
    def test_ok_status_google_place(self, monkeypatch):
        """Test if the function returns a dict with
         the needed values."""
        geometry = {"lat": 20, "lng": 30}
        candidates = [{"frmtted_address": "champ de Mars",
                       "geometry": geometry,
                       "name": "Tour Eiffel"}]
        response = {"candidates": candidates, "status": "OK"}

        def mockreturn(request):
            return BytesIO(json.dumps(response).encode())

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        _response = get_geolocate_response("tour eiffel")

        assert response == _response

    def test_not_status_google_place(self, monkeypatch):
        """Test if the function raise asserationError
         when the request have no Ok status."""
        response = {
            "results": [],
            "status": "ZERO_RESULTS"
        }

        def mockreturn(request):
            return BytesIO(json.dumps(response).encode())

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        with pytest.raises(AssertionError):
            get_geolocate_response('ireozprjfze')

    def test_parse_geolocate_response(self, monkeypatch):
        """Test if the function return a dict with the expected keys"""
        response = {
            "results": [
                {
                    "formatted_address": "7 Cité Paradis, 75010 Paris, France",
                    "geometry": {
                        "location": {
                            "lat": 48.8747265,
                            "lng": 2.3505517
                        },
                        "viewport": {
                            "northeast": {
                                "lat": 48.9021449,
                                "lng": 2.4699208
                            },
                            "southwest": {
                                "lat": 48.815573,
                                "lng": 2.224199
                            }
                        }
                    },
                    "types": ["establishment", "point_of_interest"]
                }
            ],
            "status": "OK"
        }

        def mockreturn(request):
            return BytesIO(json.dumps(response).encode())

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        _response = parse_geolocate_response("openclassrooms")

        assert list(_response.keys()) == [
            "asked_address",
            "formatted_address",
            "location",
            "bounds"
        ]
