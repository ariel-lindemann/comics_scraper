from typing import Optional
from comics_scraper import search_series, filter_links, find_links_on_page

RETURN_COMMAND = 'END'


def cli_interaction() -> Optional[dict[str, str]]:
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
            try:
                series_name, series_url = _selection_modal(links_dict)
            except TypeError:
                break
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
        try:
            selected_name, selected_link = _selection_modal(issues_links)
        except TypeError:
            break
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


def _selection_modal(links_dict: dict[str, str]) -> Optional[tuple[str, str]]:
    unfiltered_links = links_dict
    while True:
        if len(links_dict) == 1:
            (k, v) = links_dict.popitem()
            return k, v
        print('Narrow the list down by typing more words or type \'#\' before a number to select an entry directly.')
        selection = input()
        if not selection:
            continue
        if selection == RETURN_COMMAND:
            return None
        if selection[0] == '#':
            try:
                k, v = _direct_selection(links_dict, selection)
                return k, v
            except TypeError:
                continue
        links_dict = filter_links(selection, links_dict)
        if not links_dict:
            print('No entries match your input. Please try again')
            links_dict = unfiltered_links

        _list_links(links_dict, 'Select one of the following')


def _direct_selection(links_dict: dict[str, str], selection: str) -> Optional[tuple[str, str]]:
    '''Select an entry by its index
    '''
    try:
        index = int(selection[1:])
    except ValueError:
        print(f'{selection[1:]} is not a number! Please try again.')
        return None
    try:
        key = list(links_dict)[index]
        value = list(links_dict.values())[index]
    except IndexError:
        print('Number out of range. Please try again.')
        return None
    return key, value


def _list_links(links_dict: dict[str, str], message: str) -> None:
    print(message)
    for i, e in enumerate(links_dict.keys()):
        print(f'    {i}.\t {e}')
