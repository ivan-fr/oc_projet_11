import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, 'google_map.json')) as f:
    views_1 = f.read()

with open(os.path.join(BASE_DIR, 'google_map_invalide.json')) as f:
    views_2 = f.read()

# create mock data

mock_data_view = {
    'requests': {
        'https://maps.googleapis.com/maps/api/geocode/json?address=tour+eiffel'
        '%2C+75+paris%2C+FR&key=AIzaSyCIB8gP3P5S-ttaOCZQBj0efd8sSDbPqdQ'
        '&language=fr&components=country%3AFR': views_1,
        'https://maps.googleapis.com/maps/api/geocode/json?address='
        'dfohdfsfdhoidsf&key=AIzaSyCIB8gP3P5S-ttaOCZQBj0efd8sSDbPqdQ'
        '&language=fr': views_1
    }
}
