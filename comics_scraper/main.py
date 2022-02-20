import requests
from bs4 import BeautifulSoup
from PIL import Image
from comics_scraper.comics import Issue, Series

BASE_URL = 'http://readallcomics.com'
COMICS_DIR = ''


def _get_data(url):
    r = requests.get(url)
    return r.text


def _get_imgs(url, skip):
    print('getting images...')
    htmldata = _get_data(url)
    soup = BeautifulSoup(htmldata, 'html.parser')
    images_soup = soup.find_all('img')

    images_pil = []
    x = 0

    for i in images_soup:
        print('.', end='')
        x += 1
        img_url = i['src']
        img = Image.open(requests.get(img_url, stream=True).raw)
        if(x >= skip):
            img = img.convert('RGB')
            images_pil.append(img)
            vertical = (img.size[0] < img.size[1])
            if not vertical:
                x += 1

    return images_pil


def get_issue(issue: Issue, skip=2):
    issue_url = issue.get_url()
    print(f'getting issue: {issue_url} ...')
    url = f'{BASE_URL}/{issue_url}'

    images = _get_imgs(url, skip)

    cover = images[0]
    rest = images[1:]
    pdf_title = issue_url.replace('-', ' ')

    cover.save(f'{COMICS_DIR}{pdf_title}.pdf', 'PDF',
               save_all=True, append_images=rest)


def get_multiple_issues(issues:dict, skip):

    for i in issues.values():
        get_issue(i, skip)


def main(series:Series):
    skip = 2

    issues = series.get_all_issues()
    get_multiple_issues(issues, skip)
