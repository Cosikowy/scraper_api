import shutil
import os
import time
import urllib.request
import requests
from inscriptis import get_text
from bs4 import BeautifulSoup

def validate_url(url):
    if not url.startswith('http'):           # Validacja adresów, aby można było wpisywać
        url = 'http://'+url                  # pełne adresy oraz pomijając http(s)

    return url

def download_image(image_link, image_name,path):
    response = requests.get(image_link, stream=True)

    # image_name = image_link.split('/')[-1]

    with open(f"./downloaded/{path}/{image_name}.png", 'wb') as file:

        response.raw.decode_content = True
        shutil.copyfileobj(response.raw, file)
        del response

def make_archive_for_download(source, destination):

    # Tworzenie archiwum ze wszystkich plików w folderze

    if not os.path.exists('./temp'):
        os.mkdir('./temp')

    name = source.split('/')[-1]

    shutil.make_archive(name, 'zip', source, destination)
    try:
        shutil.move(f'{name}.zip', f'temp/{destination}')
    except: 
        os.remove(f'./temp/{destination}/{name}.zip')
        shutil.move(f'{name}.zip', f'temp/{destination}')

    return f'{name}.zip'


def scrap_text(url, host, encoding_type='utf-8'):

    # ściąga całą zawartość strony przygotowaną wg formatu Markdown

    html = urllib.request.urlopen(url).read().decode(encoding_type)

    text = get_text(html)

    with open(f'./downloaded/{host}/page_content.txt', 'w', encoding=encoding_type) as _file:
        _file.write(text)


def scrap_images(url, host):

    # Wyszukuje wszystkie elementy <img>, czyli domyślny objekt obrazu w HTML

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    images = soup.find_all("img")
    image_links = []

    for image in images:
        try:
            image_link = image["src"]               # W tym miejscu może powstać błąd w razie dziwnego edge case
            image_link = image_link.split('//')

            if image_link[-1][0] != '/':
                image_link = 'http://'+image_link[-1]
            else:
                image_link = 'http://'+host+image_link[-1]

            image_links.append(image_link) 
        except KeyError:
            continue


    for _, link in enumerate(set(image_links)):
        download_image(link, _,host)



def create_folder_on_url(url):
    if not os.path.exists('./downloaded'):
        os.mkdir('./downloaded/')

    _url = url.split('//')[-1]
    folder_name = _url.split('/')[0]

    if os.path.exists(f'./downloaded/{folder_name}'):
        pass
    else:
        os.mkdir(f'./downloaded/{folder_name}')
    
    return folder_name
