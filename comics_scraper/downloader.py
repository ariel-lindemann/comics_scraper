import requests
from bs4 import BeautifulSoup, SoupStrainer
from PIL import Image
from comics_scraper.comics import Series, Issue


BASE_URL = 'http://readallcomics.com'
COMICS_DIR = ''
BSPARSER = 'html.parser'


def find_links(series_name: str) -> dict[str:str]:
    '''Returns a mapping of matching titles to  links of their respective series pages
    '''
    url = BASE_URL + f'?story={series_name}&s=&type=comic'
    htmldata = _get_data(url)
    a_tags = SoupStrainer('a')
    soup = BeautifulSoup(htmldata, BSPARSER, parse_only=a_tags)

    soup = soup.find_all(title=True)

    links = [s['href'] for s in soup]
    titles = [s['title'] for s in soup]
    links_dict = dict(zip(titles, links))

    return links_dict


def _get_data(url):
    r = requests.get(url)
    return r.text


def _get_imgs(url):
    print('getting images...')
    htmldata = _get_data(url)
    soup = BeautifulSoup(htmldata, BSPARSER)
    images_soup = soup.find_all('img')

    images_pil = []

    for i in images_soup:
        img_url = i['src']
        img = Image.open(requests.get(img_url, stream=True).raw)
        if _check_img_belongs(img_url):
            img = img.convert('RGB')
            images_pil.append(img)

    return images_pil

def _check_link_belongs(url):
    blacklist = [
        "https://readallcomics.com/",
        'http://readallcomics.com/wp-content/uploads/2019/12/prev.png',
        'http://readallcomics.com/wp-content/uploads/2019/12/Next.png',
        'http://readallcomics.com/wp-content/uploads/2020/03/Donate.png'
    ]
    return url not in blacklist

def _check_img_belongs(img_url):

    blacklist = [
        'http://readallcomics.com/wp-content/uploads/2020/09/logo-1.png',
        'http://readallcomics.com/wp-content/uploads/2019/12/prev.png',
        'http://readallcomics.com/wp-content/uploads/2019/12/Next.png',
        'http://readallcomics.com/wp-content/uploads/2020/03/Donate.png'
    ]
    return img_url not in blacklist


def download_issue(issue: Issue):
    issue_url = issue.get_url()
    full_url = f'{BASE_URL}/{issue_url}'
    title = issue_url.replace('-', ' ')

    _download_url(full_url, title )


def _download_url(url, pdf_title):
    print(f'getting issue: {url} ...')

    images = _get_imgs(url)

    if len(images) == 0:
        raise ComicNotFoundException(f'{url} not found')

    cover = images[0]
    rest = images[1:]

    cover.save(f'{COMICS_DIR}{pdf_title}.pdf', 'PDF',
               save_all=True, append_images=rest)


def download_multiple_issues(issues: list[Issue]):

    for i in issues:
        try:
            download_issue(i)
        except ComicNotFoundException:
            i.increment_url()
            try:
                download_issue(i)
            except ComicNotFoundException:
                print(f'{i.url} not found')


class ComicNotFoundException(Exception):
    pass
