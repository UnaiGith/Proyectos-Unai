import unittest

from python_uax.external_packages import app

import unittest
class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_hello_world(self):
        response = self.app.get('/')
        self.assertEqual(200, response.status_code)
        self.assertEqual('Hello world!', response.data.decode())

    def test_about(self):
        response = self.app.get('/about')
        self.assertEqual(200, response.status_code)
        self.assertEqual('About', response.data.decode())

    def test_get_user(self):
        response = self.app.get('/user/123')
        self.assertEqual(200, response.status_code)
        self.assertEqual('User id: 123', response.data.decode())

        response = self.app.get('/user/456')
        self.assertEqual(200, response.status_code)
        self.assertEqual('User id: 456', response.data.decode())


if __name__ == 'flask':
    unittest.main()
