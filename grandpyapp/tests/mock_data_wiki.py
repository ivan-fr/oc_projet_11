import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, 'geosearch_1.json')) as f:
    views_1 = f.read()

with open(os.path.join(BASE_DIR, 'geosearch.json')) as f:
    views_2 = f.read()

with open(os.path.join(BASE_DIR, 'geosearch_3.json')) as f:
    views_3 = f.read()

with open(os.path.join(BASE_DIR, 'search.json')) as f:
    views_4 = f.read()

with open(os.path.join(BASE_DIR, 'search_2.json')) as f:
    views_5 = f.read()

with open(os.path.join(BASE_DIR, 'search_3.json')) as f:
    views_6 = f.read()

with open(os.path.join(BASE_DIR, 'search_4.json')) as f:
    views_7 = f.read()

with open(os.path.join(BASE_DIR, 'page.json')) as f:
    views_8 = f.read()

with open(os.path.join(BASE_DIR, 'page_2.json')) as f:
    views_9 = f.read()

with open(os.path.join(BASE_DIR, 'page_3.json')) as f:
    views_10 = f.read()

with open(os.path.join(BASE_DIR, 'page_4.json')) as f:
    views_11 = f.read()

with open(os.path.join(BASE_DIR, 'page_5.json')) as f:
    views_12 = f.read()

with open(os.path.join(BASE_DIR, 'page_object.json')) as f:
    views_13 = f.read()

with open(os.path.join(BASE_DIR, 'page_object_2.json')) as f:
    views_14 = f.read()

with open(os.path.join(BASE_DIR, 'page_object_3.json')) as f:
    views_15 = f.read()

with open(os.path.join(BASE_DIR, 'page_object_4.json')) as f:
    views_16 = f.read()

with open(os.path.join(BASE_DIR, 'page_object_5.json')) as f:
    views_17 = f.read()

# create mock data

mock_data_wiki = {
    'requests': {
        'https://fr.wikipedia.org/w/api.php?list=geosearch&gsradius=1000'
        '&gscoord=40.67693%7C117.23193&gslimit=10'
        '&format=json&action=query': views_1,
        'https://fr.wikipedia.org/w/api.php?list=geosearch&gsradius=1000&'
        'gscoord=40.67693%7C117.23193&gslimit=10&titles=Great+Wall+of+China'
        '&format=json&action=query': views_1,
        'https://fr.wikipedia.org/w/api.php?list=geosearch&gsradius=10000&'
        'gscoord=40.67693%7C117.23193&gslimit=10&'
        'format=json&action=query': views_2,
        'https://fr.wikipedia.org/w/api.php?list=geosearch&gsradius=1000&'
        'gscoord=40.67693%7C117.23193&gslimit=10&'
        'titles=fdosfjdspdj&format=json&action=query': views_3,
        'https://fr.wikipedia.org/w/api.php?list=search&srprop=&srlimit=10&'
        'limit=10&srsearch=Barack+Obama&format=json&action=query': views_4,
        'https://fr.wikipedia.org/w/api.php?list=search&srprop=&srlimit=3&'
        'limit=3&srsearch=Porsche&format=json&action=query': views_5,
        'https://fr.wikipedia.org/w/api.php?list=search&srprop=&srlimit=10'
        '&limit=10&srsearch=hallelulejah&srinfo=suggestion'
        '&format=json&action=query': views_6,
        'https://fr.wikipedia.org/w/api.php?list=search&srprop='
        '&srlimit=10&limit=10&srsearch=qmxjsudek&srinfo=suggestion&'
        'format=json&action=query': views_7,
        'https://fr.wikipedia.org/w/api.php?prop=info%7Cpageprops&inprop=url'
        '&ppprop=disambiguation&redirects=&titles=sdfjpodsjdf'
        '&format=json&action=query': views_8,
        'https://fr.wikipedia.org/w/api.php?prop=info%7Cpageprops&inprop=url'
        '&ppprop=disambiguation&redirects=&titles=Menlo+Park%2C+New+Jersey&'
        'format=json&action=query': views_9,
        'https://fr.wikipedia.org/w/api.php?prop=info%7Cpageprops&inprop=url'
        '&ppprop=disambiguation&redirects=&titles=Edison%2C+New+Jersey&'
        'format=json&action=query': views_10,
        'https://fr.wikipedia.org/w/api.php?prop=info%7Cpageprops&inprop=url'
        '&ppprop=disambiguation&redirects=&titles=communist+Party&'
        'format=json&action=query': views_11,
        'https://fr.wikipedia.org/w/api.php?prop=info%7Cpageprops&inprop=url'
        '&ppprop=disambiguation&redirects=&titles=Communist+party&'
        'format=json&action=query': views_12,
        'https://fr.wikipedia.org/w/api.php?prop=info%7Cpageprops&inprop=url'
        '&ppprop=disambiguation&redirects=&titles=Celtuce&'
        'format=json&action=query': views_13,
        'https://fr.wikipedia.org/w/api.php?prop=info%7Cpageprops&inprop=url'
        '&ppprop=disambiguation&redirects=&'
        'titles=Tropical+Depression+Ten+%282005%29&format=json'
        '&action=query': views_14,
        'https://fr.wikipedia.org/w/api.php?prop=info%7Cpageprops&'
        'inprop=url&ppprop=disambiguation&'
        'redirects=&titles=Great+Wall+of+China&format=json'
        '&action=query': views_15,
        'https://fr.wikipedia.org/w/api.php?prop=info%7Cpageprops&inprop=url'
        '&ppprop=disambiguation&redirects=&pageids=1868108'
        '&format=json&action=query': views_13,
        'https://fr.wikipedia.org/w/api.php?prop=extracts&explaintext='
        '&exintro=&titles=Celtuce&format=json&action=query': views_16,
        'https://fr.wikipedia.org/w/api.php?prop=extracts&explaintext=&exintro='
        '&titles=Tropical+Depression+Ten+%282005%29'
        '&format=json&action=query': views_17
    }
}
