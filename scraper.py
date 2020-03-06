import urllib.request
from inscriptis import get_text
from bs4 import BeautifulSoup
import requests
import shutil
import os


def download_image(image_link, image_name, path):
    response = requests.get(image_link, stream=True)

    file = open(f"./downloaded/{path}/{image_name}.jpg", 'wb')
    
    response.raw.decode_content = True
    shutil.copyfileobj(response.raw, file)
    del response


def scrap_text(url, path, decoder='utf-8'):
    url = "https://www.python.org/"
    html = urllib.request.urlopen(url).read().decode(decoder)

    text = get_text(html)

    with open(f'./downloaded/{path}/page_content.txt', 'w', encoding=decoder) as _file:
        _file.write(text)


def scrap_images(url, host):

    # Wyszukuje wszystkie elementy <img>, czyli domyślny objekt obrazu w HTML

    response = requests.get(url)
    
    soup = BeautifulSoup(response.text, "html.parser")
    images = soup.find_all("img")
    
    image_links = []

    for image in images:
        image_link = image["src"]
        image_link = image_link.split('//')

        if image_link[-1][0] != '/':
            image_link = 'http://'+image_link[-1]
        else:
            image_link = 'http://'+host+image_link[-1]

        image_links.append(image_link)
    
    for num ,link in enumerate(set(image_links)):
        download_image(link, num, host)



def create_folder(url):
    if not os.path.exists(f'./downloaded'):
        os.mkdir(f'./downloaded/')

    if 'http://' or 'https://' in url:
        _url = url.split('//')[-1]
        host = _url.split('/')[0]
    else:
        host = _url.split('/')[0]
    
    if os.path.exists(f'./downloaded/{host}'):
        pass
    else:
        os.mkdir(f'./downloaded/{host}')

    # scrap_text(url, host)
    # scrap_images(url, host)

create_folder('http://google.com')

# scrap_images_and_text("https://pl.wikipedia.org/wiki/Python", 'pl.wikipedia.org')