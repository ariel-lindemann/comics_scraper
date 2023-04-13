import pytest
import mock
import cli

SERIES_NAME = 'The Adventures of Tintin'


@pytest.fixture(name="generate_links_dict")
def fixture_generate_links_dict():
    return {
        'The Adventures of Tintin': 'https://readallcomics.com/category/the-adventures-of-tintin/',
        'Tintin Film Books': 'https://readallcomics.com/category/tintin-film-books/'
    }


def test_direct_selection_correct_input(generate_links_dict):
    links_dict = generate_links_dict
    selection = '#0'
    key, _ = cli._direct_selection(links_dict, selection)
    assert key == SERIES_NAME


def test_direct_selection_not_a_number(generate_links_dict):
    links_dict = generate_links_dict
    selection = '#a'
    result = cli._direct_selection(links_dict, selection)

    assert result is None


def test_direct_selection_out_of_range(generate_links_dict):
    links_dict = generate_links_dict
    selection = '#5'
    result = cli._direct_selection(links_dict, selection)

    assert result is None
