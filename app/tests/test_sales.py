# import unittest
# import json

# from .base_test import BaseTest

# class TestSales(BaseTest):
#     """Sales Endpoints Test Suite"""

#     def test_user_can_post_sales(self):
#         """Test that user can post sales"""


#         self.user_authentication_register(email="mail1234@mail.com", password="pass", confirm_password="pass", role="admin")
#         login_response = self.user_authentication_login(email="mail1234@mail.com", password="pass")

#         authentication_token = json.loads(login_response.data.decode())['access_token']
#         sales_posted = self.client().post('/api/v2/sales',
#                                     content_type="application/json",
#                                     headers=dict(Authorization="Bearer {}".format(authentication_token)),
#                                     data=json.dumps({{"cart": "1,5",
#                                                       "cart_price": 500
#                                                     }}))
#         result = json.loads(sales_posted.data.decode())
#         self.assertEqual(result['message'], 'success')
#         self.assertEqual(sales_posted.status_code, 201)

#     def test_fetch_all_sales(self):
#         """Test that user can retrieve all sales"""

#         self.user_authentication_register(email="mail1234@mail.com", password="pass", confirm_password="pass", role="admin")
#         login_response = self.user_authentication_login(email="mail1234@mail.com", password="pass")

#         authentication_token = json.loads(login_response.data.decode())['access_token']
#         sales_posted = self.client().post('/api/v2/sales',
#                                     content_type="application/json",
#                                     headers=dict(Authorization="Bearer {}".format(authentication_token)),
#                                     data=json.dumps({{"cart": "1,5",
#                                                       "cart_price": 500
#                                                     }}))
#         result = json.loads(sales_posted.data.decode())
#         self.assertEqual(result['message'], 'success')
#         self.assertEqual(sales_posted.status_code, 201)

#         fetch_sales = self.client().get('/api/v2/sales',
#                                         headers=dict(Authorization="Bearer {}".format(authentication_token)))
#         fetch_sales_data = json.loads(fetch_sales.data)
#         self.assertEqual(fetch_sales.status_code, 200)
#         self.assertEqual(fetch_sales_data['success'], 'ok')

#     def test_fetch_single_sale(self):
#         """Test that user can retrieve single sale"""

#         self.user_authentication_register(email="mail1234@mail.com", password="pass", confirm_password="pass", role="admin")
#         login_response = self.user_authentication_login(email="mail1234@mail.com", password="pass")

#         authentication_token = json.loads(login_response.data.decode())['access_token']
#         sales_posted = self.client().post('/api/v2/sales',
#                                     content_type="application/json",
#                                     headers=dict(Authorization="Bearer {}".format(authentication_token)),
#                                     data=json.dumps({{"cart": "1,5",
#                                                       "cart_price": 500
#                                                     }}))
#         result = json.loads(sales_posted.data.decode())
#         self.assertEqual(result['message'], 'success')
#         self.assertEqual(sales_posted.status_code, 201)

#         fetch_sales_record = self.client().get('/api/v1/sales/{}'.format(result['sales']['id']),
#                                   headers=dict(Authorization="Bearer {}".format(authentication_token)))
#         self.assertEqual(fetch_sales_record.status_code, 200)

