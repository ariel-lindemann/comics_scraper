import requests
from bs4 import BeautifulSoup
from PIL import Image
from comics_scraper.comics import Issue, Series

BASE_URL = 'http://readallcomics.com'
COMICS_DIR = ''


def _get_data(url):
    r = requests.get(url)
    return r.text


def _get_imgs(url):
    print('getting images...')
    htmldata = _get_data(url)
    soup = BeautifulSoup(htmldata, 'html.parser')
    images_soup = soup.find_all('img')

    images_pil = []

    for i in images_soup:
        print('.', end='')
        img_url = i['src']
        img = Image.open(requests.get(img_url, stream=True).raw)
        if _check_img_belongs(img_url):
            img = img.convert('RGB')
            images_pil.append(img)

    return images_pil


def _check_img_belongs(img_url):

    blacklist = [
        'http://readallcomics.com/wp-content/uploads/2020/09/logo-1.png',
        'http://readallcomics.com/wp-content/uploads/2019/12/prev.png',
        'http://readallcomics.com/wp-content/uploads/2019/12/Next.png',
        'http://readallcomics.com/wp-content/uploads/2020/03/Donate.png'
    ]
    return img_url not in blacklist


def get_issue(issue: Issue):
    issue_url = issue.get_url()
    print(f'getting issue: {issue_url} ...')
    url = f'{BASE_URL}/{issue_url}'

    images = _get_imgs(url)

    cover = images[0]
    rest = images[1:]
    pdf_title = issue_url.replace('-', ' ')

    cover.save(f'{COMICS_DIR}{pdf_title}.pdf', 'PDF',
               save_all=True, append_images=rest)


def get_multiple_issues(issues: dict):

    for i in issues.values():
        get_issue(i)


def main(series: Series):

    issues = series.get_all_issues()
    get_multiple_issues(issues)
