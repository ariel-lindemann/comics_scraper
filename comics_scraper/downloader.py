import requests
from bs4 import BeautifulSoup
from PIL import Image


COMICS_DIR = ''
BSPARSER = 'html.parser'


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


def _check_img_belongs(img_url):

    blacklist = [
        'http://readallcomics.com/wp-content/uploads/2020/09/logo-1.png',
        'https://readallcomics.com/wp-content/uploads/2020/09/logo-1.png',
        'http://readallcomics.com/wp-content/uploads/2019/12/prev.png',
        'https://readallcomics.com/wp-content/uploads/2019/12/prev.png',
        'http://readallcomics.com/wp-content/uploads/2019/12/Next.png',
        'https://readallcomics.com/wp-content/uploads/2019/12/Next.png',
        'http://readallcomics.com/wp-content/uploads/2020/03/Donate.png'
        'https://readallcomics.com/wp-content/uploads/2020/03/Donate.png',
        'https://readallcomics.com/wp-content/uploads/2022/05/readallNOVELbanner.jpg'
    ]
    return img_url not in blacklist


def download_issue(url, title):
    print(f'getting issue: {title} ...')

    images = _get_imgs(url)
    title = _sanitiize_title(title)

    if len(images) == 0:
        raise ComicNotFoundException(f'{url} not found')

    cover = images[0]
    rest = images[1:]

    cover.save(f'{COMICS_DIR}{title}.pdf', 'PDF',
               save_all=True, append_images=rest)


def download_multiple_issues(issues: dict[str, str]):
    if not issues:
        print('No issues to download!')
        return
    
    for title, url in issues.items():
        try:
            download_issue(url, title)
        except ComicNotFoundException:
            print(f'{url} not found')


def _sanitiize_title(title):
    # TODO cover additional special symbols
    return title.replace('/', ' ')


class ComicNotFoundException(Exception):
    pass
