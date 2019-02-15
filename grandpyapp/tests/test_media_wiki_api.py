import urllib.request
from io import BytesIO
from decimal import Decimal
from grandpyapp.managers import wikipedia
import pytest
from .mock_data_wiki import mock_data_wiki


def mockreturn(request):
    return BytesIO(mock_data_wiki['requests'][request].encode())


class TestSearchLoc:
    """Test the functionality of wikipedia.geosearch."""

    @classmethod
    def setup_class(cls):
        cls.mock_data = {
            "data": {
                "geo_search": ['Great Wall of China'],
                "geo_search_with_radius":
                    ['Great Wall of China', 'Jinshanling', 'Gubeikou'],
                "geo_search_with_existing_article_name":
                    ['Great Wall of China'],
                "geo_search_with_non_existing_article_name":
                    [],
            },
        }

    def test_geosearch(self, monkeypatch):
        """Test parsing a Wikipedia location request result."""

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        assert wikipedia.geosearch(Decimal('40.67693'), Decimal('117.23193')) \
               == self.mock_data['data']["geo_search"]

    def test_geosearch_with_radius(self, monkeypatch):
        """Test parsing a Wikipedia location request result."""

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        assert wikipedia.geosearch(
            Decimal('40.67693'), Decimal('117.23193'), radius=10000) == \
               self.mock_data['data']["geo_search_with_radius"]

    def test_geosearch_with_existing_title(self, monkeypatch):
        """Test parsing a Wikipedia location request result."""

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        assert wikipedia.geosearch(
            Decimal('40.67693'), Decimal('117.23193'),
            title='Great Wall of China') == \
               self.mock_data['data']["geo_search_with_existing_article_name"]

    def test_geosearch_with_non_existing_title(self, monkeypatch):
        """Test parsing a Wikipedia location request result."""

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        assert wikipedia.geosearch(
            Decimal('40.67693'), Decimal('117.23193'), title='fdosfjdspdj') == \
               self.mock_data['data']["geo_search_with_non_"
                                      "existing_article_name"]


class TestSearch:
    """Test the functionality of wikipedia.search."""

    @classmethod
    def setup_class(cls):
        cls.mock_data = {
            "data": {
                "barack.search": ['Barack Obama',
                                  'Family of Barack Obama',
                                  'Barack Obama Sr.',
                                  'Presidency of Barack Obama',
                                  "Barack Obama citizenship"
                                  " conspiracy theories",
                                  'Speeches of Barack Obama',
                                  "First inauguration "
                                  "of Barack Obama",
                                  "Barack Obama religion"
                                  " conspiracy theories",
                                  "Barack Obama"
                                  " Presidential Center",
                                  "Early life and career"
                                  " of Barack Obama"]
            }
        }

    def test_search(self, monkeypatch):
        """Test parsing a Wikipedia request result."""

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        assert wikipedia.search("Barack Obama") == \
               self.mock_data['data']["barack.search"]

    def test_limit(self, monkeypatch):
        """Test limiting a request results."""

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        assert len(wikipedia.search("Porsche", results=3)) <= 3

    def test_suggestion(self, monkeypatch):
        """Test getting a suggestion as well as search results."""

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        search, suggestion = wikipedia.search("hallelulejah", suggestion=True)
        assert search == []
        assert suggestion == "hallelujah"

    def test_suggestion_none(self, monkeypatch):
        """Test getting a suggestion when there is no suggestion."""

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        search, suggestion = wikipedia.search("qmxjsudek", suggestion=True)
        assert search == []
        assert suggestion is None


class TestPageSetUp:
    """Test the functionality of
    wikipedia.page's __init__ and load functions."""

    def test_missing(self, monkeypatch):
        """Test that page raises a PageError for a nonexistant page."""

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        with pytest.raises(Exception):
            wikipedia.page("sdfjpodsjdf", auto_suggest=False)

    def test_redirect_true(self, monkeypatch):
        """Test that a page successfully redirects a query."""

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        # no error should be raised if redirect is true
        mp = wikipedia.page("Menlo Park, New Jersey", auto_suggest=False)

        assert mp.title == "Edison, New Jersey"
        assert mp.url == "https://en.wikipedia.org/wiki/Edison,_New_Jersey"

    def test_redirect_false(self, monkeypatch):
        """Test that page raises an error
         on a redirect when redirect == False."""

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        with pytest.raises(Exception):
            wikipedia.page("Menlo Park, New Jersey",
                           auto_suggest=False, redirect=False)

    def test_redirect_with_normalization(self, monkeypatch):
        """Test that a page redirect with a normalized query loads correctly"""

        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        the_party = wikipedia.page("communist Party", auto_suggest=False)
        assert isinstance(the_party, wikipedia.WikipediaPage)
        assert the_party.title == "Communist party"


class TestPage:
    """Test the functionality of the rest of wikipedia.page."""

    @classmethod
    def setup_class(cls):
        cls.mock_data = {
            "data": {
                "celtuce.summary": 'Celtuce (Lactuca sativa var. asparagina,'
                                   ' augustana, or angustata), also called stem'
                                   ' lettuce, celery lettuce,'
                                   ' asparagus lettuce,'
                                   ' or Chinese lettuce, IPA (UK,US)'
                                   ' /\u02c8s\u025blt.\u0259s/, is a '
                                   'cultivar of lettuce grown primarily '
                                   'for its thick stem, used '
                                   'as a vegetable. It '
                                   'is especially popular '
                                   'in China, and is called'
                                   ' wosun (Chinese: \u83b4\u7b0b; pinyin:'
                                   ' w\u014ds\u016dn) or woju (Chinese:'
                                   ' \u83b4\u82e3; pinyin:) (although '
                                   'the latter name may also'
                                   ' be used to mean lettuce'
                                   ' in general).\n\nThe stem'
                                   ' is usually harvested '
                                   'at a length of around 15\u201320 cm and a '
                                   'diameter of around'
                                   ' 3\u20134 cm. It is crisp, '
                                   'moist, and mildly flavored, and typically '
                                   'prepared by slicing and then stir frying '
                                   'with more strongly flavored ingredients.',
                "cyclone.summary": 'Tropical Depression '
                                   'Ten was the tenth tropical'
                                   ' cyclone of the record-breaking'
                                   ' 2005 Atlantic '
                                   'hurricane season. It '
                                   'formed on August 13 from '
                                   'a tropical wave that emerged from the west '
                                   'coast of Africa on '
                                   'August 8. As a result of '
                                   'strong wind shear, the'
                                   ' depression remained weak'
                                   ' and did not strengthen beyond tropical '
                                   'depression status. The cyclone degenerated '
                                   'on August 14, although'
                                   ' its remnants partially '
                                   'contributed to the formation of Tropical '
                                   'Depression Twelve, which'
                                   ' eventually intensified'
                                   ' into Hurricane Katrina. The cyclone had no'
                                   ' effect on land, and did not directly '
                                   'result in any fatalities or damage.',
            },
        }

    @pytest.fixture(autouse=True)
    def setup_method(self, monkeypatch):
        """ setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """

        # shortest wikipedia articles with images and sections
        monkeypatch.setattr(urllib.request, 'urlopen', mockreturn)

        self.celtuce = wikipedia.page("Celtuce", auto_suggest=False)
        self.cyclone = wikipedia.page("Tropical Depression Ten (2005)",
                                      auto_suggest=False)
        self.great_wall_of_china = wikipedia.page("Great Wall of China",
                                                  auto_suggest=False)

    def test_from_page_id(self, monkeypatch):
        """Test loading from a page id"""
        assert self.celtuce == wikipedia.page(pageid=1868108)

    def test_title(self):
        """Test the title."""
        assert self.celtuce.title == "Celtuce"
        assert self.cyclone.title == "Tropical Depression Ten (2005)"

    def test_url(self):
        """Test the url."""
        assert self.celtuce.url == "https://en.wikipedia.org/wiki/Celtuce"
        assert self.cyclone.url == "https://en.wikipedia.org/wiki/" \
                                   "Tropical_Depression_Ten_(2005)"

    def test_summary(self, monkeypatch):
        """Test the summary."""
        assert self.celtuce.summary() == self.mock_data['data'][
            "celtuce.summary"]
        assert self.cyclone.summary() == self.mock_data['data'][
            "cyclone.summary"]
