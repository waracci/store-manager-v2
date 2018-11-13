import unittest
import json

from app.tests.base_test import BaseTest
from .data import product1_data, sale1_data, sale2_data, sale3_data

class TestSales(BaseTest):
    """Sales Endpoints Test Suite"""

    def test_user_can_post_sales(self):
        """Test that user can post sales"""


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
        sales_posted = self.client().post('/api/v2/sales',
                                    content_type="application/json",
                                    headers=dict(Authorization="Bearer {}".format(authentication_token)),
                                    data=json.dumps(sale1_data))
        result = json.loads(sales_posted.data.decode())
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(sales_posted.status_code, 201)

    def test_fetch_all_sales(self):
        """Test that user can retrieve all sales"""

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

        sell_posted_product = self.client().post('/api/v2/sales',
                                    content_type="application/json",
                                    headers=dict(Authorization="Bearer {}".format(authentication_token)),
                                    data=json.dumps(sale1_data))
        result = json.loads(sell_posted_product.data.decode())
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(sell_posted_product.status_code, 201)

        fetch_sales = self.client().get('/api/v2/sales',
                                        headers=dict(Authorization="Bearer {}".format(authentication_token)))
        fetch_sales_data = json.loads(fetch_sales.data)
        self.assertEqual(fetch_sales.status_code, 200)
        self.assertEqual(fetch_sales_data['status'], 'ok')

    def test_fetch_single_sale(self):
        """Test that user can retrieve single sale"""

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
        sales_posted = self.client().post('/api/v2/sales',
                                    content_type="application/json",
                                    headers=dict(Authorization="Bearer {}".format(authentication_token)),
                                    data=json.dumps(sale1_data))
        result = json.loads(sales_posted.data.decode())
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(sales_posted.status_code, 201)

        fetch_sales_record = self.client().get('/api/v2/sales/1',
                                  headers=dict(Authorization="Bearer {}".format(authentication_token)))
        self.assertEqual(fetch_sales_record.status_code, 200)

    def test_attendant_cannot_get_all_sales(self):
        """Test that attendant cannot get all sales"""

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
        sales_posted = self.client().post('/api/v2/sales',
                                    content_type="application/json",
                                    headers=dict(Authorization="Bearer {}".format(authentication_token)),
                                    data=json.dumps(sale1_data))
        result = json.loads(sales_posted.data.decode())
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(sales_posted.status_code, 201)

        self.user_authentication_register_attendant2()
        login_response = self.user_authentication_login2()

        authentication_token = json.loads(login_response.data.decode())['token']
        fetch_sales_record = self.client().get('/api/v2/sales/1',
                                  headers=dict(Authorization="Bearer {}".format(authentication_token)))
        self.assertEqual(fetch_sales_record.status_code, 406)

    def test_sale_of_unavailable_quantity_goods(self):
        """Test that attendant cannot sell unavailable quantity of products"""

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
        sales_posted = self.client().post('/api/v2/sales',
                                    content_type="application/json",
                                    headers=dict(Authorization="Bearer {}".format(authentication_token)),
                                    data=json.dumps(sale2_data))
        result = json.loads(sales_posted.data.decode())
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['message'], '5 products remaining only')
        self.assertEqual(sales_posted.status_code, 404)

    def test_sale_of_unavailable_product(self):
        """Test that attendant cannot sell unavailable product"""

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
        sales_posted = self.client().post('/api/v2/sales',
                                    content_type="application/json",
                                    headers=dict(Authorization="Bearer {}".format(authentication_token)),
                                    data=json.dumps(sale3_data))
        result = json.loads(sales_posted.data.decode())
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['message'], 'Product not found for sale')
        self.assertEqual(sales_posted.status_code, 404)
