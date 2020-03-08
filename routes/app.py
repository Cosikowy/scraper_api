from flask import Flask
from flask_restplus import Api, Resource, Namespace
from resources.scraper import Scrapper
from flask_cors import CORS
from werkzeug.contrib.fixers import ProxyFix
import os


app = Flask(__name__)

# app.wsgi_app = ProxyFix(app.wsgi_app)

api = Api(app, doc='/docs/', title='Scraper API', description='Scraper Api')
scraper = api.namespace('Scraper', path='/scraper')

scraper.add_resource(Scrapper, '/scraper/<mode>/<path:url>')

app.url_map.strict_slashes = False

CORS(app, resources=r'/api/*')

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
