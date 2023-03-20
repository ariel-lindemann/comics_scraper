from typing import Optional
from comics_scraper import search_series, filter_links, find_links_on_page

def cli_interaction() -> Optional[dict[str,str]]:
    print('Hello, welcome to comics scraper!\nWhich series are you interested in?')
    series_name = input()
    links_dict = search_series(series_name)

    if not links_dict:
        print(f'Sorry, we couldn\'t find any series named \"{series_name}\"')

    else: 
        _list_links(links_dict, 'Select one of the following')
        series_name, series_url = selection_modal(links_dict)
        print(f'You selected \"{series_name}\"')

        # select issue to download
        issues_links = find_links_on_page(series_url)
        issue_name, selected_link = selection_modal(issues_links)

        print(f'You selected the following issue: {issue_name}')

        return {issue_name: selected_link}


def selection_modal(links_dict: dict[str,str]) -> tuple[str,str]:
    # TODO select by number
    while True:
        if len(links_dict) == 1:
            (k, v) = links_dict.popitem()
            return k, v
        print('Narrow the list down by typing more words')
        selection = input()
        if selection == 'END':
            return '', ''#TODO
        links_dict = filter_links(selection, links_dict)
        _list_links(links_dict, 'Select one of the following')


def _list_links(links_dict: dict[str,str], message: str) -> None:
    print(message)
    for i, e in enumerate(links_dict.keys()):
        print(f'    {i}.\t {e}')
