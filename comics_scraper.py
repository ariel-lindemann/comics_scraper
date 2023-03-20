from comics_scraper.main import main
from comics_scraper.comics import Series
from comics_scraper.downloader import find_links

def cli_interaction():
    print('Hello, welcome to comics scraper!\nWhich series are you interested in?')
    series_name = input()
    links_dict = find_links(series_name)

    if not links_dict:
        print(f'Sorry, we couldn\'t find any series named \"{series_name}\"')

    else: print('Select one of the following:')
    for i, e in enumerate(links_dict.keys()):
        print(f'    {i}.\t {e}')



if __name__ == '__main__':

    cli_interaction()

    # TODO issue_page
    # TODO CLI


