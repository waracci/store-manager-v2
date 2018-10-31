import unittest
import json

from app.tests.base_test import BaseTest

class TestSales(BaseTest):
    """Sales Endpoints Test Suite"""

    def test_user_can_post_sales(self):
        """Test that user can post sales"""


        self.user_authentication_register(email="mail1234@mail.com", password="password", confirm_password="password", role="admin")
        login_response = self.user_authentication_login(email="mail1234@mail.com", password="password")

        authentication_token = json.loads(login_response.data.decode())['token']
        product_posted = self.client().post('/api/v2/products',
                                    content_type="application/json",
                                    headers=dict(Authorization="Bearer {}".format(authentication_token)),
                                    data=json.dumps({"product_name": "cake",
                                                    "product_description": "sweet and lovely",
                                                    "product_quantity": 5,
                                                    "product_price": 100,
                                                    "product_category": "bakery",
                                                    "product_moq": 100}))
        result = json.loads(product_posted.data.decode())
        self.assertEqual(result['message'], 'Product cake added to inventory')
        self.assertEqual(product_posted.status_code, 201)
        sales_posted = self.client().post('/api/v2/products/1',
                                    content_type="application/json",
                                    headers=dict(Authorization="Bearer {}".format(authentication_token)),
                                    data=json.dumps({
                                                    "product_quantity": 1
                                                    }))
        result = json.loads(sales_posted.data.decode())
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(sales_posted.status_code, 201)

    def test_fetch_all_sales(self):
        """Test that user can retrieve all sales"""

        self.user_authentication_register(email="mail1234@mail.com", password="password", confirm_password="password", role="admin")
        login_response = self.user_authentication_login(email="mail1234@mail.com", password="password")
        authentication_token = json.loads(login_response.data.decode())['token']
        product_posted = self.client().post('/api/v2/products',
                                    content_type="application/json",
                                    headers=dict(Authorization="Bearer {}".format(authentication_token)),
                                    data=json.dumps({"product_name": "cake",
                                                    "product_description": "sweet and lovely",
                                                    "product_quantity": 5,
                                                    "product_price": 100,
                                                    "product_category": "bakery",
                                                    "product_moq": 100}))
        result = json.loads(product_posted.data.decode())
        self.assertEqual(result['message'], 'Product cake added to inventory')
        self.assertEqual(product_posted.status_code, 201)

        sell_posted_product = self.client().post('/api/v2/products/1',
                                    content_type="application/json",
                                    headers=dict(Authorization="Bearer {}".format(authentication_token)),
                                    data=json.dumps({
                                                    "product_quantity": 1
                                                    }))
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

        self.user_authentication_register(email="mail1234@mail.com", password="password", confirm_password="password", role="admin")
        login_response = self.user_authentication_login(email="mail1234@mail.com", password="password")

        authentication_token = json.loads(login_response.data.decode())['token']
        product_posted = self.client().post('/api/v2/products',
                                    content_type="application/json",
                                    headers=dict(Authorization="Bearer {}".format(authentication_token)),
                                    data=json.dumps({"product_name": "cake",
                                                    "product_description": "sweet and lovely",
                                                    "product_quantity": 5,
                                                    "product_price": 100,
                                                    "product_category": "bakery",
                                                    "product_moq": 100}))
        result = json.loads(product_posted.data.decode())
        self.assertEqual(result['message'], 'Product cake added to inventory')
        self.assertEqual(product_posted.status_code, 201)
        sales_posted = self.client().post('/api/v2/products/1',
                                    content_type="application/json",
                                    headers=dict(Authorization="Bearer {}".format(authentication_token)),
                                    data=json.dumps({
                                                    "product_quantity": 1
                                                    }))
        result = json.loads(sales_posted.data.decode())
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(sales_posted.status_code, 201)

        fetch_sales_record = self.client().get('/api/v2/sales/1',
                                  headers=dict(Authorization="Bearer {}".format(authentication_token)))
        self.assertEqual(fetch_sales_record.status_code, 200)

    def test_attendant_cannot_get_all_sales(self):
        """Test that attendant cannot get all sales"""

        self.user_authentication_register(email="mail1234@mail.com", password="password", confirm_password="password", role="admin")
        login_response = self.user_authentication_login(email="mail1234@mail.com", password="password")

        authentication_token = json.loads(login_response.data.decode())['token']
        product_posted = self.client().post('/api/v2/products',
                                    content_type="application/json",
                                    headers=dict(Authorization="Bearer {}".format(authentication_token)),
                                    data=json.dumps({"product_name": "cake",
                                                    "product_description": "sweet and lovely",
                                                    "product_quantity": 5,
                                                    "product_price": 100,
                                                    "product_category": "bakery",
                                                    "product_moq": 100}))
        result = json.loads(product_posted.data.decode())
        self.assertEqual(result['message'], 'Product cake added to inventory')
        self.assertEqual(product_posted.status_code, 201)
        sales_posted = self.client().post('/api/v2/products/1',
                                    content_type="application/json",
                                    headers=dict(Authorization="Bearer {}".format(authentication_token)),
                                    data=json.dumps({
                                                    "product_quantity": 1
                                                    }))
        result = json.loads(sales_posted.data.decode())
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(sales_posted.status_code, 201)

        self.user_authentication_register(email="attendant@mail.com", password="password", confirm_password="password", role="attendant")
        login_response = self.user_authentication_login(email="attendant@mail.com", password="password")

        authentication_token = json.loads(login_response.data.decode())['token']
        fetch_sales_record = self.client().get('/api/v2/sales/1',
                                  headers=dict(Authorization="Bearer {}".format(authentication_token)))
        self.assertEqual(fetch_sales_record.status_code, 406)
