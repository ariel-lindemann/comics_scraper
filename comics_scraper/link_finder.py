
from bs4 import BeautifulSoup, SoupStrainer
import requests
from comics_scraper.downloader import BASE_URL, BSPARSER


def search_series(series_name: str) -> dict[str:str]:
    '''Returns a mapping of matching titles to  links of their respective series pages
    '''
    url = BASE_URL + f'?story={series_name}&s=&type=comic'
    return find_links_on_page(url)
    

def find_links_on_page(url: str) -> dict[str:str]:
    '''Returns dictionary of links on the provided page
    '''
    htmldata = requests.get(url).text
    a_tags = SoupStrainer('a')
    soup = BeautifulSoup(htmldata, BSPARSER, parse_only=a_tags)

    soup = soup.find_all(title=True)

    links = [s['href'] for s in soup]
    titles = [s['title'] for s in soup]
    links_dict = dict(zip(titles, links))

    return links_dict


def filter_links(search_term: str, links: dict[str:str]) -> dict[str:str]:
    filtered = dict((k, v) for k, v in links.items() if search_term in k.lower())
    return filtered
