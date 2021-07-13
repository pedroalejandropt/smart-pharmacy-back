import os
import json
import requests
import unittest

class ExchangeTest(unittest.TestCase):

    token = ''
    user_id = 0

    def setUp(self):
        # Initial Values
        global token
        exchange = { 'email': 'pedro@gmail.com', 'password': '123456' }
        res = requests.post('http://localhost:5000/api/v1/login', json = exchange)
        user_id = json.loads(res.text)['user']['id']
        token = json.loads(res.text)['token']

    def test_get_exchanges(self):
        # When
        res = requests.get('http://localhost:5000/api/v1/exchanges', headers={ 'x-access-token': token })
        exchanges = json.loads(res.text)

        # Then
        self.assertEqual(type(exchanges), type([]))

    def test_post_exchange(self):
        # Given
        global user_id
        exchange = { 'exchange': { 'date': "2021-06-03", 'amount': 2450000 }, 'user': { 'user_id': user_id } }

        # When
        res = requests.post('http://localhost:5000/api/v1/exchanges', json = exchange , headers = { 'x-access-token': token })
        new_exchange = json.loads(res.text)

        # Then
        self.assertEqual(new_exchange['amount'], exchange['amount'])

    def test_put_exchange(self):
        # Given
        global token
        id = 3
        exchange = { 'date': "2021-06-03", 'amount': 2451999 }

        # When
        res = requests.put('http://localhost:5000/api/v1/exchanges/' + str(id), json = exchange , headers = { 'x-access-token': token })
        updated_exchange = json.loads(res.text)

        # Then
        self.assertEqual(updated_exchange['amount'], exchange['amount'])

    def test_delete_exchange(self):
        # Given
        global token
        id = 3

        # When
        res = requests.delete('http://localhost:5000/api/v1/exchanges/' + str(id), headers = { 'x-access-token': token })
        deleted_exchange = json.loads(res.text)

        # Then
        self.assertTrue(deleted_exchange['delete'])

    def tearDown(self):
        # Delete Initial Values
        pass

    