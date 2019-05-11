import pytest
from grandpyapp.managers.parser import Parser


@pytest.mark.parametrize("sentence,excpected", [
    ("Malgré la morosité de l'époque actuelle,"
     " je préconise un audit afin d'examiner les relations"
     " des options emblématiques, même si ce n'est pas facile.", 23),
    ("Pour réagir face à la morosité présente,"
     " je vous demande de façonner les principales"
     " solutions envisageables, pour longtemps.", 18),
    ("Dans le but de pallier à la restriction induite,"
     " il serait bon de considérer les principales"
     " modalités envisageables, parce que nous le valons bien.", 24)
])
def test_get_words_from_sentence(sentence, excpected):
    assert len(list(Parser.get_words_from_sentence(sentence))) == excpected


@pytest.mark.parametrize("sentence,excpected", [
    ("Salut papi, j'aimerai avoir l'adresse de sète stp.", "sète"),
    ("coucou grand père, tu ne saurais pas où" +
     " est situé Paris par hasard ?", "paris"),
    ("yo papi, j'veux bien l'adresse du groenland.", "groenland"),
    ("hey, tu n'aurais pas une idée d'où se situe la rue des" +
     " rosiers par hasard ?", "rue rosiers"),
    ("je veux aller en angleterre", "angleterre"),
    ("Salut GrandPy ! Est-ce que tu connais"
     " l'adresse d'OpenClassrooms ?", "openclassrooms")
])
def test_parse_sentence(sentence, excpected):
    """Situationals tests."""
    assert Parser.parse_sentence(sentence) == excpected
