from flask import Flask
from flask_restplus import Api, Resource, Namespace
from scraper import Scrapper
from flask_cors import CORS

app = Flask(__name__)

app.url_map.strict_slashes = False

api = Api(app, doc='/docs/', title='Scraper API', description='Scraper Api')

CORS(app, resources=r'/api/*')

scraper = api.namespace('Scraper', path='/scraper')
scraper.add_resource(Scrapper, '/scraper/<mode>/<path:url>')

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 60
app.run(host='0.0.0.0', port=5000, debug=True)
