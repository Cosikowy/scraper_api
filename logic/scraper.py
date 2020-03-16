import shutil
import os
import time
import asyncio
import requests
from inscriptis import get_text
from bs4 import BeautifulSoup
from aiohttp import ClientSession
import aiohttp

def validate_url(url):
    if not url.startswith('http'):           # Validacja adresów, aby można było wpisywać
        url = f'http://{url}'                  # pełne adresy oraz pomijając http(s)
    return url

async def download_image(image_link, image_name,path):
    async with ClientSession() as s, s.get(image_link) as res:
        with open(f"./downloaded/{path}/{image_name}.png", 'wb') as file:
            response = await res.content.read()
            file.write(response)

def make_archive_for_download(source, destination):
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



async def scrap_text(url, host, encoding_type='utf-8'):
    async with ClientSession() as s, s.get(url) as res:
        ret = await res.text('utf-8')
        ret = get_text(ret)
        with open(f'./downloaded/{host}/page_content.txt', 'w', encoding=encoding_type) as _file:
            _file.write(ret)




async def scrap_images(url, host):
    async with ClientSession() as s, s.get(url) as res:
        ret = await res.text('utf-8')

    soup = BeautifulSoup(ret, "html.parser")
    image_count = len(soup.find_all("img"))
    images = (x for x in soup.find_all("img"))
    count = 0
    # test_case = next(images)
    for name, image in enumerate(set(images)):
        try:
            image_link = image["src"]
            image_link = image_link.split('//')
            if image_link[-1][0] != '/':
                image_link = f'http://{image_link[-1]}'
            else:
                image_link = f'http://{host}{image_link[-1]}'
            
            task = asyncio.create_task(download_image(image_link, name, host))
            print(f'{count}/{image_count}')
            await task
            await asyncio.sleep(10)
            count+=1

        except (KeyError, aiohttp.client_exceptions.ClientConnectorError) :
            continue




def create_folder_on_url(url):
    if not os.path.exists('./downloaded'):
        os.mkdir('./downloaded/')

    _url = url.split('//')[-1]
    folder_name = _url.split('/')[0]

    if not os.path.exists(f'./downloaded/{folder_name}'):
        os.mkdir(f'./downloaded/{folder_name}')
    
    return folder_name
