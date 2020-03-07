from inscriptis import get_text
from bs4 import BeautifulSoup
import urllib.request
import requests
import shutil
import os
import time

def validate_url(url):
    if 'http' not in url:
        print('validated')
        url = 'http://'+url
    return url

def download_image(image_link, image_name, path):
    response = requests.get(image_link, stream=True)

    file = open(f"./downloaded/{path}/{image_name}.png", 'wb')
    
    response.raw.decode_content = True
    shutil.copyfileobj(response.raw, file)
    del response

def make_archive_for_download(source, destination):
    
    # Function to create a tar archive with all page data
    
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


def scrap_text(url, host, decoder='utf-8'):
    
    # ściąga całą zawartość strony przygotowaną wg formatu Markdown
    print(url)
    html = urllib.request.urlopen(url).read().decode(decoder)

    text = get_text(html)

    with open(f'./downloaded/{host}/page_content.txt', 'w', encoding=decoder) as _file:
        _file.write(text)


def scrap_images(url, host):

    # Wyszukuje wszystkie elementy <img>, czyli domyślny objekt obrazu w HTML
    print(url)
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    images = soup.find_all("img")

    image_links = []

    for image in images:
        image_link = image["src"]               # W tym miejscu może powstać błąd w razie dziwnego edge case
        image_link = image_link.split('//')     # 

        if image_link[-1][0] != '/':
            image_link = 'http://'+image_link[-1]
        else:
            image_link = 'http://'+host+image_link[-1]

        image_links.append(image_link) 
    
    for num, link in enumerate(set(image_links)):
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
    return host
