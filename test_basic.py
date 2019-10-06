import unittest
import json

import app


class AppTest(unittest.TestCase):

    def setUp(self):
        self.app = app.app.test_client()

    def tearDown(self):
        pass

    def test_default(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_add_machine(self):
        response = self.app.get('/addmachine')
        self.assertEqual(response.status_code, 200)

    def test_remove_machine(self):
        response = self.app.get('/removemachine')
        self.assertEqual(response.status_code, 200)

    def test_add_sodas(self):
        response = self.app.get('/addsodas')
        self.assertEqual(response.status_code, 200)
        
    def test_remove_sodas(self):
        response = self.app.get('/removesodas')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
