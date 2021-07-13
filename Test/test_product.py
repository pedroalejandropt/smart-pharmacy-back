import os
import json
import requests
import unittest

class ProductTest(unittest.TestCase):

    token = ''
    user_id = 0
    product_id = 0

    def setUp(self):
        # Initial Values
        global token
        product = { 'email': 'pedro@gmail.com', 'password': '123456' }
        res = requests.post('http://localhost:5000/api/v1/login', json = product)
        user_id = json.loads(res.text)['user']['id']
        token = json.loads(res.text)['token']

    def test_get_products(self):
        # When
        res = requests.get('http://localhost:5000/api/v1/products', headers={ 'x-access-token': token })
        products = json.loads(res.text)

        # Then
        self.assertEqual(type(products), type([]))

    def test_post_product(self):
        # Given
        global user_id
        global product_id
        product = { 'product': { 'code': 123456789, 'codebar': 123456789, 'name': 'Producto', 'price': 5.3, 'freeze': 0, 'tax': 0, 'recipe': 0, 'regulated': 1, 'rating': 4, 'replacementClassification': 3, 'labProviderName': 'Proveedor', 'subcategory_id': 1 }, 'user': { 'user_id': 1 } }

        # When
        res = requests.post('http://localhost:5000/api/v1/products', json = product , headers = { 'x-access-token': token })
        new_product = json.loads(res.text)
        product_id = new_product[id]

        # Then
        self.assertEqual(new_product['amount'], product['amount'])

    def test_put_product(self):
        # Given
        global token
        global product_id
        product = { 'code': 123456789, 'codebar': 123456789, 'name': 'Producto', 'price': 5.3, 'freeze': 0, 'tax': 0, 'recipe': 0, 'regulated': 1, 'rating': 4, 'replacementClassification': 3, 'labProviderName': 'Proveedor', 'subcategory_id': 1 }

        # When
        res = requests.put('http://localhost:5000/api/v1/products/' + str(product_id), json = product , headers = { 'x-access-token': token })
        updated_product = json.loads(res.text)

        # Then
        self.assertEqual(updated_product['amount'], product['amount'])

    def test_delete_product(self):
        # Given
        global token
        global product_id

        # When
        res = requests.delete('http://localhost:5000/api/v1/products/' + str(id), headers = { 'x-access-token': token })
        deleted_product = json.loads(res.text)

        # Then
        self.assertTrue(deleted_product['delete'])

    def tearDown(self):
        # Delete Initial Values
        pass