import urllib.request
import urllib.parse
import json


def return_urllib_request(base_url, params):
    query_string = urllib.parse.urlencode(params)

    url = base_url + '?' + query_string

    _dict = {}

    with urllib.request.urlopen(url) as response:
        _dict = json.loads(response.read().decode('utf8'))

    return _dict
