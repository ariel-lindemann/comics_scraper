import pytest
from comics_scraper.link_finder import search_series, find_links_on_page, filter_links

# TODO add more cases (params)


@pytest.fixture
def generate_str_search_data():
    search_term = 'tintin'

    output = {
        'The Adventures of Tintin': 'https://readallcomics.com/category/the-adventures-of-tintin/',
        'Tintin Film Books': 'https://readallcomics.com/category/tintin-film-books/'
    }

    return search_term, output


@pytest.fixture
def generate_url_search_data():
    search_url = 'https://readallcomics.com/?story=tintin&s=&type=comic'
    output = {
        'The Adventures of Tintin': 'https://readallcomics.com/category/the-adventures-of-tintin/',
        'Tintin Film Books': 'https://readallcomics.com/category/tintin-film-books/'
    }
    return search_url, output


def test_search_series(generate_str_search_data):
    search_term = generate_str_search_data[0]
    expected_result = generate_str_search_data[1]
    results_dict = search_series(search_term)
    assert results_dict == expected_result


def test_find_links_on_page(generate_url_search_data):
    search_term = generate_url_search_data[0]
    expected_result = generate_url_search_data[1]
    results_dict = find_links_on_page(search_term)
    assert results_dict == expected_result


def test_filter_links(generate_str_search_data):
    filter_term = 'adventures'
    expected_result = 'The Adventures of Tintin'
    filtered_links = filter_links(filter_term, generate_str_search_data[1])
    assert expected_result in filtered_links.keys()
