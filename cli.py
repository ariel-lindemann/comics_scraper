from comics_scraper import find_links, filter_links

def cli_interaction():
    print('Hello, welcome to comics scraper!\nWhich series are you interested in?')
    series_name = input()
    links_dict = find_links(series_name)

    if not links_dict:
        print(f'Sorry, we couldn\'t find any series named \"{series_name}\"')

    else: 
        _list_links(links_dict, 'Select one of the following')
        series_name, series_url = select_series(links_dict)
        # TODO issue selection modal
        print(f'You selected \"{series_name}\"')


def select_series(links_dict: dict[str:str]) -> tuple[str:str]:
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


def _list_links(links_dict: dict[str:str], message: str) -> None:
    print(message)
    for i, e in enumerate(links_dict.keys()):
        print(f'    {i}.\t {e}')
