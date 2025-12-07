import unittest
import json
import tempfile
import os
from app import app
from db import init_db


class UserAPITestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.original_db = app.config.get('DATABASE', 'test.db')

        app.config['DATABASE'] = self.db_path
        app.config['TESTING'] = True

        self.client = app.test_client()

        with app.app_context():
            init_db(self.db_path)

    def tearDown(self):

        app.config['DATABASE'] = self.original_db
        os.close(self.db_fd)
        try:
            os.unlink(self.db_path)
        except:
            pass

    def test_hello_endpoint(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), 'Hello URFU')


    def test_create_user(self):
        user_data = {
            'name': 'Test User',
            'email': 'test@urfu.ru'
        }

        response = self.client.post(
            '/user',
            data=json.dumps(user_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data.decode())
        self.assertIn('id', data)
        self.assertEqual(data['message'], 'Пользователь успешно создан')


    def test_get_users_empty(self):
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        self.assertEqual(data, [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
