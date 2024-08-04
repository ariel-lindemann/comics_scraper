import string
from typing import Optional
from comics_scraper import search_series, filter_links, find_links_on_page

from prompt_toolkit import PromptSession
from prompt_toolkit.application import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Box, Frame


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
                series_name, series_url = SelectionModal(links_dict).run()
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
            selected_name, selected_link = SelectionModal(issues_links).run()
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
        selection = input('Search: ').strip()
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


class SelectionModal:
    def __init__(self, links_dict: dict[str, str]):
        self.links_dict = links_dict
        self.unfiltered_links = links_dict.copy()
        self.filtered_links = links_dict
        self.query = ""

        self.bindings = KeyBindings()
        self.bindings.add('c-c')(self.exit)
        self.bindings.add('c-q')(self.exit)
        self.bindings.add('enter')(self.select)
        self.bindings.add('backspace')(self.backspace)

        for key in string.printable:
            self.bindings.add(key)(self.add_char(key))

        self.layout = Layout(HSplit([
            Box(Window(FormattedTextControl(self.get_display_text), height=1)),
            Box(Window(FormattedTextControl(self.get_hits_text), height=1)),
            Box(Window(FormattedTextControl(self.get_results_text), height=20, always_hide_cursor=True))
        ]))

        self.application = Application(
            layout=self.layout,
            key_bindings=self.bindings,
            full_screen=True,
            mouse_support=True,
            style=Style.from_dict({
                'window.border': 'cyan',
                'shadow': 'gray',
            }),
        )

    def get_display_text(self):
        return [("class:text", f"Search: {self.query}")]

    def get_hits_text(self):
        return [("class:text", f"Your selection mathes {len(self.filtered_links)} items:")]

    def get_results_text(self):
        if not self.filtered_links:
            return [("class:text", "No entries match your input. Please try again.")]

        return [("class:text", f"{i}: {k}\n") for i, k in enumerate(self.filtered_links.keys())]

    def add_char(self, char):
        def handler(event):
            self.query += char
            self.filtered_links = filter_links(self.query, self.unfiltered_links)
            self.application.layout = Layout(HSplit([
                Box(Window(FormattedTextControl(self.get_display_text), height=1)),
                Box(Window(FormattedTextControl(self.get_hits_text), height=1)),
                Box(Window(FormattedTextControl(self.get_results_text), height=10, always_hide_cursor=True))
            ]))
        return handler

    def backspace(self, event):
        self.query = self.query[:-1]
        self.filtered_links = filter_links(self.query, self.unfiltered_links)
        self.application.layout = Layout(HSplit([
            Box(Window(FormattedTextControl(self.get_display_text), height=1)),
            Box(Window(FormattedTextControl(self.get_hits_text), height=1)),
            Box(Window(FormattedTextControl(self.get_results_text), height=10, always_hide_cursor=True))
        ]))

    def select(self, event):
        if len(self.filtered_links) == 1:
            self.selected_item = list(self.filtered_links.items())[0]
            self.application.exit()
        elif self.query.startswith('#'):
            try:
                index = int(self.query[1:])
                if 0 <= index < len(self.filtered_links):
                    self.selected_item = list(self.filtered_links.items())[index]
                    self.application.exit()
                else:
                    self.query = "Invalid index. Try again."
                    self.filtered_links = self.unfiltered_links
            except ValueError:
                self.query = "Invalid format. Try again."
                self.filtered_links = self.unfiltered_links

    def exit(self, event):
        self.selected_item = None
        self.application.exit()

    def run(self):
        self.application.run()
        return self.selected_item


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
