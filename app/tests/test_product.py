import unittest
import json

from app.tests.base_test import BaseTest
from .data import product1_data, product2_data

class TestProduct(BaseTest):
    """Test Suite for Product endpoints"""

    def test_post_product(self):
        """Test that admin can add Product"""

        self.user_authentication_register_admin()
        login_response = self.user_authentication_login()

        authentication_token = json.loads(login_response.data.decode())['token']
        product_posted = self.client().post('/api/v2/products',
                                    content_type="application/json",
                                    headers=dict(Authorization="Bearer {}".format(authentication_token)),
                                    data=json.dumps(product1_data))
        result = json.loads(product_posted.data.decode())
        self.assertEqual(result['message'], 'Product cake added to inventory')
        self.assertEqual(product_posted.status_code, 201)

    def test_post_product_admin_only(self):
        """Test that only admin can post a Product"""

        self.user_authentication_register_attendant()
        login_response = self.user_authentication_login()

        authentication_token = json.loads(login_response.data.decode())['token']
        product_posted = self.client().post('/api/v2/products',
                                    content_type="application/json",
                                    headers=dict(Authorization="Bearer {}".format(authentication_token)),
                                    data=json.dumps(product1_data))
        result = json.loads(product_posted.data.decode())
        self.assertEqual(result['message'], 'requires admin')
        self.assertEqual(product_posted.status_code, 406)

    def test_fetch_all_products(self):
        """Test that user can fetch all products"""

        self.user_authentication_register_admin()
        login_response = self.user_authentication_login()
        authentication_token = json.loads(login_response.data.decode())['token']
        product_posted = self.client().post('/api/v2/products',
                                    content_type="application/json",
                                    headers=dict(Authorization="Bearer {}".format(authentication_token)),
                                    data=json.dumps(product1_data))
        result = json.loads(product_posted.data.decode())
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(product_posted.status_code, 201)

        fetch_products = self.client().get('/api/v2/products',
                                        headers=dict(Authorization="Bearer {}".format(authentication_token)))
        fetch_products_data = json.loads(fetch_products.data)
        self.assertEqual(fetch_products.status_code, 200)
        self.assertEqual(fetch_products_data['status'], 'ok')

    def test_fetch_single_product(self):
        """Test that app returns single product fetched"""

        self.user_authentication_register_admin()
        response = self.user_authentication_login()
    
        authentication_token = json.loads(response.data.decode())['token']

        product_posted = self.client().post('/api/v2/products',
                                    content_type="application/json",
                                    headers=dict(Authorization="Bearer {}".format(authentication_token)),
                                    data=json.dumps(product1_data))
        self.assertEqual(product_posted.status_code, 201)

        fetch_single_product = self.client().get('/api/v2/products/1',
                                                headers=dict(Authorization="Bearer {}".format(authentication_token)))
        self.assertEqual(fetch_single_product.status_code, 200)

    def test_product_details_can_be_edited(self):
        """Test that a product details can be edited by admin"""

        self.user_authentication_register_admin()
        response = self.user_authentication_login()

        authentication_token = json.loads(response.data.decode())['token']

        product_posted = self.client().post('/api/v2/products',
                                    content_type="application/json",
                                    headers=dict(Authorization="Bearer {}".format(authentication_token)),
                                    data=json.dumps(product1_data))
        self.assertEqual(product_posted.status_code, 201)

        fetch_single_product = self.client().get('/api/v2/products/1',
                                                        headers=dict(Authorization="Bearer {}".format(authentication_token)))
        self.assertEqual(fetch_single_product.status_code, 200)

        edit_single_product = self.client().put('/api/v2/products/1',
                                                headers=dict(Authorization="Bearer {}".format(authentication_token)),
                                                content_type='application/json',
                                                data=json.dumps(product2_data))
        edit_product_result = json.loads(edit_single_product.data)
        self.assertEqual(edit_single_product.status_code, 200)
        self.assertEqual(edit_product_result['message'], 'success')

        fetch_single_product = self.client().get('/api/v2/products/1',
                                                headers=dict(Authorization="Bearer {}".format(authentication_token)))
        self.assertEqual(fetch_single_product.status_code, 200)
        self.assertEqual(json.loads(fetch_single_product.data)['product'][0]['name'], 'Eggnog')

    def test_user_can_delete_product(self):
        """Test that admin can delete a product"""

        self.user_authentication_register_admin()
        response = self.user_authentication_login()

        authentication_token = json.loads(response.data.decode())['token']

        product_posted = self.client().post('/api/v2/products',
                                    content_type="application/json",
                                    headers=dict(Authorization="Bearer {}".format(authentication_token)),
                                    data=json.dumps(product1_data))
        self.assertEqual(product_posted.status_code, 201)


        delete_product = self.client().delete('/api/v2/products/1',
                                                headers=dict(Authorization="Bearer {}".format(authentication_token)))
        edit_product_result = json.loads(delete_product.data)

        self.assertEqual(delete_product.status_code, 200)
        self.assertEqual(edit_product_result['status'], 'ok')

        fetch_single_product = self.client().get('/api/v2/products/1',
                                                headers=dict(Authorization="Bearer {}".format(authentication_token)))
        self.assertEqual(fetch_single_product.status_code, 404)

    def test_user_cannot_post_two_products_with_same_name(self):
        """Test that admin can add Product"""

        self.user_authentication_register_admin()
        login_response = self.user_authentication_login()

        authentication_token = json.loads(login_response.data.decode())['token']
        product_posted = self.client().post('/api/v2/products',
                                    content_type="application/json",
                                    headers=dict(Authorization="Bearer {}".format(authentication_token)),
                                    data=json.dumps(product1_data))
        result = json.loads(product_posted.data.decode())
        self.assertEqual(result['message'], 'Product cake added to inventory')
        self.assertEqual(product_posted.status_code, 201)

        product_posted = self.client().post('/api/v2/products',
                                    content_type="application/json",
                                    headers=dict(Authorization="Bearer {}".format(authentication_token)),
                                    data=json.dumps(product1_data))
        result = json.loads(product_posted.data.decode())
        self.assertEqual(result['message'], 'product cake exists')
        self.assertEqual(product_posted.status_code, 400)
