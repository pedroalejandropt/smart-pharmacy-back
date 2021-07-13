import os
import json
import requests
import unittest

class UserTest(unittest.TestCase):

    token = ''

    def setUp(self):
        # Initial Values
        global token
        user = { 'email': 'pedro@gmail.com', 'password': '123456' }
        res = requests.post('http://localhost:5000/api/v1/login', json = user)
        token = json.loads(res.text)['token']

    def test_login(self):
        global token
        user = { 'email': 'pedro@gmail.com', 'password': '123456' }
        res = requests.post('http://localhost:5000/api/v1/login', json = user)
        token = json.loads(res.text)['token']

    def test_login_missing_data(self):
        global token
        user = { 'email': 'pedro@gmail.com' }
        res = requests.post('http://localhost:5000/api/v1/login', json = user)
        print = json.loads(res.text)

    def test_get_users(self):
        # When
        res = requests.get('http://localhost:5000/api/v1/users', headers={ 'x-access-token': token })
        users = json.loads(res.text)

        # Then
        self.assertEqual(type(users), type([]))

    def test_post_user(self):
        # Given
        user = { 'identificationNumber': 12345678919, 'firstName': 'Juan', 'lastName': 'Lopez', 'email': 'jlopez@gmail.com', 'password': '654321', 'role_id': 1 }

        # When
        res = requests.post('http://localhost:5000/api/v1/users', json = user , headers = { 'x-access-token': token })
        new_user = json.loads(res.text)

        # Then
        self.assertEqual(new_user['firstName'], user['firstName'])

    def test_put_user(self):
        # Given
        global token
        id = 3
        user = { 'identificationNumber': 12345678919, 'firstName': 'Juan', 'middleName': 'Carlos', 'lastName': 'Lopez', 'email': 'jlopez@gmail.com', 'password': '654321', 'role_id': 1 }

        # When
        res = requests.put('http://localhost:5000/api/v1/users/' + str(id), json = user , headers = { 'x-access-token': token })
        updated_user = json.loads(res.text)

        # Then
        self.assertEqual(updated_user['firstName'], user['firstName'])

    def test_delete_user(self):
        # Given
        global token
        id = 3

        # When
        res = requests.delete('http://localhost:5000/api/v1/users/' + str(id), headers = { 'x-access-token': token })
        deleted_user = json.loads(res.text)

        # Then
        self.assertTrue(deleted_user['delete'])

    def tearDown(self):
        # Delete Initial Values
        pass