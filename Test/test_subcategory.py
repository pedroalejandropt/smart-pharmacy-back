import os
import json
import requests
import unittest

class SubCategoryTest(unittest.TestCase):

    token = ''

    def setUp(self):
        # Initial Values
        global token
        user = { 'email': 'pedro@gmail.com', 'password': '123456' }
        res = requests.post('http://localhost:5000/api/v1/login', json = user)
        token = json.loads(res.text)['token']

    def test_get_subcategories(self):
        # Given
        global token

        # When
        res = requests.get('http://localhost:5000/api/v1/subcategories', headers={ 'x-access-token': token })
        subcategories = json.loads(res.text)

        # Then
        self.assertEqual(type(subcategories), type([]))

    def test_post_subcategory(self):
        # Given
        global token
        subcategory = { 'name': 'Dolores Musculares', 'category_id': 1 }

        # When
        res = requests.post('http://localhost:5000/api/v1/subcategories', json = subcategory , headers = { 'x-access-token': token })
        new_subcategory = json.loads(res.text)

        # Then
        self.assertEqual(new_subcategory['name'], subcategory['name'])

    def test_put_subcategory(self):
        # Given
        global token
        id = 2
        subcategory = { 'name': 'Dolor Muscular', 'category_id': 1 }

        # When
        res = requests.put('http://localhost:5000/api/v1/subcategories/' + str(id), json = subcategory , headers = { 'x-access-token': token })
        updated_subcategory = json.loads(res.text)

        # Then
        self.assertEqual(updated_subcategory['name'], subcategory['name'])

    def test_delete_subcategory(self):
        # Given
        global token
        id = 2

        # When
        res = requests.delete('http://localhost:5000/api/v1/subcategories/' + str(id), headers = { 'x-access-token': token })
        deleted_subcategory = json.loads(res.text)

        # Then
        self.assertTrue(deleted_subcategory['delete'])

    def tearDown(self):
        # Delete Initial Values
        pass