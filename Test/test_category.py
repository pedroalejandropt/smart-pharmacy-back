import os
import json
import requests
import unittest

class CategoryTest(unittest.TestCase):

    token = ''

    def setUp(self):
        # Initial Values
        global token
        user = { 'email': 'pedro@gmail.com', 'password': '123456' }
        res = requests.post('http://localhost:5000/api/v1/login', json = user)
        token = json.loads(res.text)['token']

    def test_get_categories(self):
        # Given
        global token

        # When
        res = requests.get('http://localhost:5000/api/v1/categories', headers={ 'x-access-token': token })
        categories = json.loads(res.text)

        # Then
        self.assertEqual(type(categories), type([]))

    def test_post_category(self):
        # Given
        global token
        category = { 'name': 'Miselaneos' }

        # When
        res = requests.post('http://localhost:5000/api/v1/categories', json = category , headers = { 'x-access-token': token })
        new_category = json.loads(res.text)

        # Then
        self.assertEqual(new_category['name'], category['name'])

    def test_put_category(self):
        # Given
        global token
        id = 1
        category = { 'name': 'Medicina' }

        # When
        res = requests.put('http://localhost:5000/api/v1/categories/' + str(id), json = category , headers = { 'x-access-token': token })
        updated_category = json.loads(res.text)

        # Then
        self.assertEqual(updated_category['name'], category['name'])

    def test_delete_category(self):
        # Given
        global token
        id = 1

        # When
        res = requests.delete('http://localhost:5000/api/v1/categories/' + str(id), headers = { 'x-access-token': token })
        deleted_category = json.loads(res.text)

        # Then
        self.assertTrue(deleted_category['delete'])

    def tearDown(self):
        # Delete Initial Values
        pass