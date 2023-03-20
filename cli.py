from typing import Optional
from comics_scraper import search_series, filter_links, find_links_on_page


def cli_interaction() -> Optional[dict[str, str]]:
    # TODO ask for download
    print('Hello, welcome to comics scraper!')
    selected_issues = dict()

    while True:
        print('Which series are you interested in?')
        series_name = input()
        links_dict = search_series(series_name)

        if not links_dict:
            print(
                f'Sorry, we couldn\'t find any series named \"{series_name}\"')
            tryagain = _yes_or_no_modal('Would you like to try again?]')
            if not tryagain:
                break

        else:
            _list_links(links_dict, 'Select one of the following')
            series_name, series_url = _selection_modal(links_dict)
            print(f'You selected \"{series_name}\"')

            # select issues to download
            selected_issues = issue_selection(series_url, selected_issues)

            different_series = _yes_or_no_modal(
                'Would you like to select another series?')
            if not different_series:
                break

    _list_links(selected_issues, 'You have selected the following issues:')
    download_confirmed = _yes_or_no_modal('Do you wish do download them?')

    return selected_issues if download_confirmed else None


def issue_selection(series_url: str, selected: dict[str, str]) -> dict[str, str]:
    '''Allows for the selection of multiple issues of a given series and appends them to the provided dictionary
    '''
    # TODO check if issue already in dict
    issues_links = find_links_on_page(series_url)
    while True:
        _list_links(issues_links, 'Select the issue you are interested in')
        selected_name, selected_link = _selection_modal(issues_links)
        print(f'You selected the following issue: {selected_name}')

        selected[selected_name] = selected_link
        select_more = _yes_or_no_modal('Do you want to select more?')
        if not select_more:
            break

    return selected


def _yes_or_no_modal(message: str) -> bool:
    while True:
        answer = input(f'{message} [Y/n]\n')
        if not answer:
            return True
        if answer.lower() == 'yes' or answer.lower() == 'y':
            return True
        elif answer.lower() == 'no' or answer.lower() == 'n':
            return False
        message = 'Please answer yes or no:'


def _selection_modal(links_dict: dict[str, str]) -> tuple[str, str]:
    # TODO select by number
    # TODO handle wrong input (keep unfiltered dict)
    while True:
        if len(links_dict) == 1:
            (k, v) = links_dict.popitem()
            return k, v
        print('Narrow the list down by typing more words')
        selection = input()
        if selection == 'END':
            return '', ''  # TODO
        links_dict = filter_links(selection, links_dict)
        _list_links(links_dict, 'Select one of the following')


def _list_links(links_dict: dict[str, str], message: str) -> None:
    print(message)
    for i, e in enumerate(links_dict.keys()):
        print(f'    {i}.\t {e}')
