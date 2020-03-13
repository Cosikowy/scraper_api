import os
import time
from io import BytesIO
import zipfile
from flask import send_file
from flask_restplus import Resource
from logic.scraper import create_folder_on_url, scrap_images, scrap_text, make_archive_for_download, validate_url

class Scrapper(Resource):
    def post(self, mode, url):

        url = validate_url(url)
        host = create_folder_on_url(url)

        try:
            if mode == 'images':
                scrap_images(url, host)
                return 'Images fetched', 200

            elif mode == 'content':
                scrap_text(url, host)
                return 'Content fetched', 200

            elif mode == 'both':
                scrap_text(url, host)
                scrap_images(url, host)
                return 'Page content and images fetched', 200

            else:
                return 'Bad request', 400
        
        except Exception as e:
            return f'Bad request, error occured: {e}', 400

    def get(self, mode, url):

        downloaded_list = os.listdir('./downloaded')
        if mode == 'download':
            if url in downloaded_list:
                to_download = make_archive_for_download(f'./downloaded/{url}', './')
                memory_file = BytesIO()
                with zipfile.ZipFile(memory_file, 'w') as zf:
                    data = zipfile.ZipInfo(f'./temp/{to_download}')
                    data.date_time = time.localtime(time.time())[:6]
                    data.compress_type = zipfile.ZIP_DEFLATED
                    zf.writestr(data, f'./temp/{to_download}')
                memory_file.seek(0)
                return send_file(memory_file, attachment_filename=to_download, as_attachment=True)
            
            else:
                return f'Host not in folder, available: {downloaded_list}', 406

        elif mode == 'downloaded':
            response = downloaded_list
            return response, 200

        else:
            return 'Bad request', 400

