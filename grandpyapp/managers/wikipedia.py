from .utils import return_urllib_request

API_URL = 'https://fr.wikipedia.org/w/api.php'


def search(query, results=10, suggestion=False):
    """
    Do a Wikipedia search for `query`.

    Keyword arguments:

    * results - the maxmimum number of results returned
    * suggestion - if True, return results and suggestion (if any) in a tuple
    """

    search_params = {
        'list': 'search',
        'srprop': '',
        'srlimit': results,
        'limit': results,
        'srsearch': query
    }
    if suggestion:
        search_params['srinfo'] = 'suggestion'

    raw_results = _wiki_request(search_params)

    if 'error' in raw_results:
        if raw_results['error']['info'] in ('HTTP request timed out.',
                                            'Pool queue is full'):
            raise Exception(
                "Searching for \"{0}\" resulted in a timeout."
                " Try again in a few"
                " seconds, and make sure you have"
                " rate limiting set to True.".format(query))
        else:
            raise Exception("An unknown error occured: \"{0}\"."
                            " Please report it on GitHub!"
                            .format(raw_results['error']['info']))

    search_results = (d['title'] for d in raw_results['query']['search'])

    if suggestion:
        if raw_results['query'].get('searchinfo'):
            return list(search_results), raw_results['query']['searchinfo'][
                'suggestion']
        else:
            return list(search_results), None

    return list(search_results)


def geosearch(latitude, longitude, title=None, results=10, radius=1000):
    """
    Do a wikipedia geo search for `latitude` and `longitude`
    using HTTP API described in http://www.mediawiki.org/wiki/Extension:GeoData

    Arguments:

    * latitude (float or decimal.Decimal)
    * longitude (float or decimal.Decimal)

    Keyword arguments:

    * title - The title of an article to search for
    * results - the maximum number of results returned
    * radius - Search radius in meters. The value must be between 10 and 10000
    """

    search_params = {
        'list': 'geosearch',
        'gsradius': radius,
        'gscoord': '{0}|{1}'.format(latitude, longitude),
        'gslimit': results
    }
    if title:
        search_params['titles'] = title

    raw_results = _wiki_request(search_params)

    if 'error' in raw_results:
        if raw_results['error']['info'] in ('HTTP request timed out.',
                                            'Pool queue is full'):
            raise Exception("Searching for \"{0}\" resulted in a timeout."
                            " Try again in a few"
                            " seconds, and make sure you have"
                            " rate limiting set to True."
                            .format('{0}|{1}'.format(latitude, longitude)))
        else:
            raise Exception("An unknown error occured: \"{0}\"."
                            " Please report it on GitHub!"
                            .format(raw_results['error']['info']))

    search_pages = raw_results['query'].get('pages', None)
    if search_pages:
        search_results = (v['title'] for k, v in search_pages.items() if
                          k != '-1')
    else:
        search_results = (d['title'] for d in raw_results['query']['geosearch'])

    return list(search_results)


def page(title=None, pageid=None, auto_suggest=True, redirect=True):
    """
    Get a WikipediaPage object for the page with title `title` or the pageid
    `pageid` (mutually exclusive).

    Keyword arguments:

    * title - the title of the page to load
    * pageid - the numeric pageid of the page to load
    * auto_suggest - let Wikipedia find a valid page title for the query
    * redirect - allow redirection without raising RedirectError
    * preload - load content, summary, images, references, and
    links during initialization
    """

    if title is not None:
        if auto_suggest:
            results, suggestion = search(title, results=1, suggestion=True)
            try:
                title = suggestion or results[0]
            except IndexError:
                # if there is no suggestion or search results,
                # the page doesn't exist
                raise Exception("\"{0}\" does not match any pages."
                                " Try another query!".format(title))
        return WikipediaPage(title, redirect=redirect)
    elif pageid is not None:
        return WikipediaPage(pageid=pageid)
    else:
        raise ValueError("Either a title or a pageid must be specified")


class WikipediaPage(object):
    """
    Contains data from a Wikipedia page.
    """

    def __init__(self, title=None, pageid=None, redirect=True):
        if title is not None:
            self.title = title
        elif pageid is not None:
            self.pageid = pageid
        else:
            raise ValueError("Either a title or a pageid must be specified")

        self.__load(redirect=redirect)

    def __repr__(self):
        return '<WikipediaPage \'{}\'>'.format(self.title)

    def __eq__(self, other):
        return (
                self.pageid == other.pageid
                and self.title == other.title
                and self.url == other.url
        )

    def __load(self, redirect=True):
        """
        Load basic information from Wikipedia.
        Confirm that page exists and is not a disambiguation/redirect.
        """
        query_params = {
            'prop': 'info|pageprops',
            'inprop': 'url',
            'ppprop': 'disambiguation',
            'redirects': '',
        }
        if not getattr(self, 'pageid', None):
            query_params['titles'] = self.title
        else:
            query_params['pageids'] = self.pageid

        request = _wiki_request(query_params)

        query = request['query']
        pageid = list(query['pages'].keys())[0]
        _page = query['pages'][pageid]

        # missing is present if the page is missing
        if 'missing' in _page:
            if hasattr(self, 'title'):
                raise Exception("\"{0}\" does not match any pages."
                                " Try another query!".format(self.title))
            else:
                raise Exception("Page id \"{0}\" does not "
                                "match any pages. Try another id!"
                                .format(self.pageid))

        # same thing for redirect, except
        # it shows up in query instead of page for
        # whatever silly reason
        elif 'redirects' in query:
            if redirect:
                redirects = query['redirects'][0]

                if 'normalized' in query:
                    normalized = query['normalized'][0]
                    assert normalized['from'] == self.title

                    from_title = normalized['to']

                else:
                    from_title = self.title

                assert redirects['from'] == from_title

                # change the title and reload the whole object
                self.__init__(redirects['to'], redirect=redirect)

            else:
                raise Exception(
                    "\"{0}\" resulted in a redirect. Set the redirect property"
                    " to True to allow automatic redirects."
                    .format(getattr(self, 'title', _page['title'])))

        # since we only asked for disambiguation in ppprop,
        # if a pageprop is returned,
        # then the page must be a disambiguation page
        elif 'pageprops' in _page:
            if hasattr(self, 'title'):
                raise Exception("\"{0}\" does not match any pages."
                                " Try another query!"
                                .format(self.title + " disambiguation"))
            else:
                raise Exception("Page id \"{0}\" does not "
                                "match any pages. Try another id!"
                                .format(self.pageid))
        else:
            self.pageid = pageid
            self.title = _page['title']
            self.url = _page['fullurl']

    def summary(self, sentences=0):
        """
        Plain text summary of the page.
        """

        query_params = {
            'prop': 'extracts',
            'explaintext': '',
            'exintro': '',
        }

        if not getattr(self, 'title', None) is None:
            query_params['titles'] = self.title
        else:
            query_params['pageids'] = self.pageid

        if sentences:
            query_params['exsentences'] = sentences

        request = _wiki_request(query_params)

        return request['query']['pages'][self.pageid]['extract']


def _wiki_request(params):
    """
    Make a request to the Wikipedia API using the given search parameters.
    Returns a parsed dict of the JSON response.
    """

    params['format'] = 'json'
    if 'action' not in params:
        params['action'] = 'query'

    return return_urllib_request(API_URL, params)
