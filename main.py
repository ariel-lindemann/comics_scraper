from unicodedata import name
import requests
from bs4 import BeautifulSoup
from PIL import Image
from fpdf import FPDF

BASE_URL = 'http://readallcomics.com'
COMICS_DIR = ''

images_dir = 'imgs'

def get_data(url):
    r = requests.get(url)
    return r.text


def get_imgs(url, skip = 2):
    print('getting images...')
    htmldata = get_data(url)
    soup = BeautifulSoup(htmldata, 'html.parser')
    images_soup = soup.find_all('img')

    images_pil = []
    x = 0

    for i in images_soup:
        print('.', end='')
        x+=1
        img_url = i['src']
        img = Image.open(requests.get(img_url, stream=True).raw)
        if(x>=skip):
            img = img.convert('RGB')
            images_pil.append(img)
            vertical = (img.size[0] < img.size[1])
            if not vertical:
                x+=1

    return images_pil


def get_issue(issue_url, skip):
    print(f'getting issue: {issue_url}...')
    url = f'{BASE_URL}/{issue_url}'
    
    images = get_imgs(url, skip=skip)

    cover = images[0]
    rest = images[1:]
    pdf_title = issue_url.replace('-', ' ')

    cover.save(f'{COMICS_DIR}{pdf_title}.pdf', 'PDF', save_all=True, append_images=rest)

    # make_pdf(images, 'comic.pdf')

if __name__=='__main__':
    skip = 2
    i = 7


    search_str = f'aquatlantic-full'
    get_issue(search_str, skip)