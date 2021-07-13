import os
import json
import requests
import unittest

class RoleTest(unittest.TestCase):

    token = ''

    def setUp(self):
        # Initial Values
        global token
        user = { 'email': 'pedro@gmail.com', 'password': '123456' }
        res = requests.post('http://localhost:5000/api/v1/login', json = user)
        token = json.loads(res.text)['token']

    def test_get_roles(self):
        # When
        res = requests.get('http://localhost:5000/api/v1/roles', headers={ 'x-access-token': token })
        roles = json.loads(res.text)

        # Then
        self.assertEqual(type(roles), type([]))

    def test_post_role(self):
        # Given
        role = { 'name': 'Gerente de Area' }

        # When
        res = requests.post('http://localhost:5000/api/v1/roles', json = role , headers = { 'x-access-token': token })
        new_role = json.loads(res.text)

        # Then
        self.assertEqual(new_role['name'], role['name'])

    def test_put_role(self):
        # Given
        global token
        id = 3
        role = { 'name': 'Personal de Limpieza' }

        # When
        res = requests.put('http://localhost:5000/api/v1/roles/' + str(id), json = role , headers = { 'x-access-token': token })
        updated_role = json.loads(res.text)

        # Then
        self.assertEqual(updated_role['name'], role['name'])

    def test_delete_role(self):
        # Given
        global token
        id = 3

        # When
        res = requests.delete('http://localhost:5000/api/v1/roles/' + str(id), headers = { 'x-access-token': token })
        deleted_role = json.loads(res.text)

        # Then
        self.assertTrue(deleted_role['delete'])

    def tearDown(self):
        # Delete Initial Values
        pass