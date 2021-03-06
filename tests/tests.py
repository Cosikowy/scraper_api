import unittest
from routes.app import app
from logic.scraper import validate_url, create_folder_on_url
import os
import shutil

class StartingTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()


    @classmethod
    def tearDownClass(cls):
        if os.path.exists('./downloaded/test'):
            shutil.rmtree('./downloaded/test')

        if os.path.exists('./downloaded/pl.wikipedia.org'):
            shutil.rmtree('./downloaded/pl.wikipedia.org')

        if os.path.exists('./downloaded/example'):
            shutil.rmtree('./downloaded/example')


    def test_create_folder(self):

        # Testy tworzenia folderów

        self.assertTrue(create_folder_on_url('test'), os.path.exists('./downloaded/test'))

    def test_validate_url(self):

        # Testy validacyjne

        self.assertEqual(validate_url('test.com'), 'http://test.com')
        self.assertEqual(validate_url('www.test.com'), 'http://www.test.com')
        self.assertEqual(validate_url('http://test.com'), 'http://test.com')

    def test_get(self):
        
        # Testy metod GET
        
        response = self.app.get('http://localhost:5000/scraper/scraper/downloaded/-')
        self.assertEqual(200, response.status_code)

        response_download = self.app.get('http://localhost:5000/scraper/scraper/download/test')
        self.assertEqual(200, response_download.status_code)

    def test_scrapping(self):
        
        # Testy metod POST
        
        response = self.app.post(r'http://localhost:5000/scraper/scraper/both/https%3A%2F%2Fpl.wikipedia.org%2Fwiki%2FPython')
        
        self.assertEqual(200, response.status_code)
        self.assertTrue(os.path.exists('./downloaded/pl.wikipedia.org/page_content.txt'))

    def test_wrong_requests(self):
        bad_list_request = self.app.get('http://localhost:5000/scraper/scraper/downloade/-')
        self.assertEqual(400, bad_list_request.status_code)

        wrong_folder_request = self.app.get('http://localhost:5000/scraper/scraper/download/test1')
        self.assertEqual(406, wrong_folder_request.status_code)

        bad_web_page = self.app.post('http://localhost:5000/scraper/scraper/both/example')
        self.assertEqual(400, bad_web_page.status_code)




if __name__ == '__main__':
    unittest.main()