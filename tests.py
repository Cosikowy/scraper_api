import unittest
from routes.app import app
from logic.scraper_logic import validate_url, create_folder
import os

class StartingTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()


    @classmethod
    def tearDownClass(cls):
        if os.path.exists('./downloaded/test'):
            os.rmdir('./downloaded/test')

        if os.path.exists('./downloaded/www.pl.wikipedia.org'):
            os.rmdir('./downloaded/pl.wikipedia.org')

        if os.path.exists('./downloaded/example'):
            os.rmdir('./downloaded/example')


    def test_create_folder(self):
        self.assertTrue(create_folder('test'), os.path.exists('./downloaded/test'))

    def test_validate_url(self):
        self.assertEqual(validate_url('test.com'), 'http://test.com')
        self.assertEqual(validate_url('www.test.com'), 'http://www.test.com')
        self.assertEqual(validate_url('http://test.com'), 'http://test.com')

    def test_get_list_of_folders(self):

        response = self.app.get('http://localhost:5000/scraper/scraper/downloaded/-')
        self.assertEqual(200, response.status_code)

    # def test_download(self):
    #     response = self.app.get('http://localhost:5000/scraper/scraper/download/test')
    #     self.assertEqual(200, response.status_code)

    def test_scrapping(self):
        '''
        Ten test od razu testuje scraping textu oraz obrazów
        '''
        response = self.app.post(r'http://localhost:5000/scraper/scraper/both/https%3A%2F%2Fpl.wikipedia.org%2Fwiki%2FPython')
        
        self.assertEqual(200, response.status_code)
        self.assertTrue(os.path.exists('./downloaded/pl.wikipedia.org/page_content.txt'))

    def test_wrong_requests(self):
        response_1 = self.app.get('http://localhost:5000/scraper/scraper/downloade/-')
        self.assertEqual(401, response_1.status_code)

        response_2 = self.app.get('http://localhost:5000/scraper/scraper/download/test1')
        self.assertEqual(402, response_2.status_code)

        response_3 = self.app.post('http://localhost:5000/scraper/scraper/both/example')
        self.assertEqual(403, response_3.status_code)




if __name__ == '__main__':
    unittest.main()