import os
from flask import Flask
from flask_restplus import Api, Resource, Namespace
from resources.scraper import Scrapper
from flask_cors import CORS


app = Flask(__name__)

app.url_map.strict_slashes = False

''' API '''
api = Api(app, doc='/docs/', title='Scraper API', description='Scraper Api')
scraper = api.namespace('Scraper', path='/scraper')

scraper.add_resource(Scrapper, '/scraper/<mode>/<path:url>')

''' Config '''

CORS(app, resources=r'/scraper/*')

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
