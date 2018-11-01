import unittest
import json

from app.tests.base_test import BaseTest

class TestCategory(BaseTest):
    """Test Suite for Category endpoints"""

    def test_post_category(self):
        """Test that admin can add category"""

        self.user_authentication_register(email="mail1234@mail.com", password="password", confirm_password="password", role="admin")
        login_response = self.user_authentication_login(email="mail1234@mail.com", password="password")

        authentication_token = json.loads(login_response.data.decode())['token']
        category_posted = self.client().post('/api/v2/category',
                                    content_type="application/json",
                                    headers=dict(Authorization="Bearer {}".format(authentication_token)),
                                    data=json.dumps({"category_name": "technology",
                                                    "category_description": "tech related gadgets"}))
        result = json.loads(category_posted.data.decode())
        self.assertEqual(result['message'], 'category technology added to inventory')
        self.assertEqual(category_posted.status_code, 201)

    def test_post_category_admin_only(self):
        """Test that only admin can post a category"""

        self.user_authentication_register(email="mail1234@mail.com", password="password", confirm_password="password", role="attendant")
        login_response = self.user_authentication_login(email="mail1234@mail.com", password="password")

        authentication_token = json.loads(login_response.data.decode())['token']
        category_posted = self.client().post('/api/v2/category',
                                    content_type="application/json",
                                    headers=dict(Authorization="Bearer {}".format(authentication_token)),
                                    data=json.dumps({"category_name": "technology",
                                                    "category_description": "tech related gadgets"}))
        result = json.loads(category_posted.data.decode())
        self.assertEqual(result['message'], 'requires admin')
        self.assertEqual(category_posted.status_code, 406)

    def test_fetch_all_categories(self):
        """Test that attendant can not fetch all categories"""

        self.user_authentication_register(email="mail1234@mail.com", password="password", confirm_password="password", role="admin")
        login_response = self.user_authentication_login(email="mail1234@mail.com", password="password")
        authentication_token = json.loads(login_response.data.decode())['token']
        category_posted = self.client().post('/api/v2/category',
                                    content_type="application/json",
                                    headers=dict(Authorization="Bearer {}".format(authentication_token)),
                                    data=json.dumps({"category_name": "technology",
                                                    "category_description": "tech related gadgets"}))
        result = json.loads(category_posted.data.decode())
        self.assertEqual(result['status'], 'ok')
        self.assertEqual(category_posted.status_code, 201)

        fetch_categories = self.client().get('/api/v2/category',
                                        headers=dict(Authorization="Bearer {}".format(authentication_token)))
        fetch_categories_data = json.loads(fetch_categories.data)
        self.assertEqual(fetch_categories.status_code, 200)
        self.assertEqual(fetch_categories_data['status'], 'ok')

    def test_fetch_single_category(self):
        """Test that app returns single category fetched"""

        self.user_authentication_register(email="ulbricht@mail.com", password="password", confirm_password="password", role='admin')
        response = self.user_authentication_login(email="ulbricht@mail.com", password="password")
    
        authentication_token = json.loads(response.data.decode())['token']

        category_posted = self.client().post('/api/v2/category',
                                    content_type="application/json",
                                    headers=dict(Authorization="Bearer {}".format(authentication_token)),
                                    data=json.dumps({"category_name": "technology",
                                                    "category_description": "tech related gadgets"}))
        self.assertEqual(category_posted.status_code, 201)

        fetch_single_category = self.client().get('/api/v2/category/1',
                                                headers=dict(Authorization="Bearer {}".format(authentication_token)))
        self.assertEqual(fetch_single_category.status_code, 200)

    def test_category_details_can_be_edited(self):
        """Test that a category details can be edited and admin"""

        self.user_authentication_register(email="ulbricht@mail.com", password="password", confirm_password="password", role='admin')
        response = self.user_authentication_login(email="ulbricht@mail.com", password="password")

        authentication_token = json.loads(response.data.decode())['token']

        category_posted = self.client().post('/api/v2/category',
                                    content_type="application/json",
                                    headers=dict(Authorization="Bearer {}".format(authentication_token)),
                                    data=json.dumps({"category_name": "technology",
                                                    "category_description": "tech related gadgets"}))
        self.assertEqual(category_posted.status_code, 201)

        fetch_single_category = self.client().get('/api/v2/category/1',
                                                        headers=dict(Authorization="Bearer {}".format(authentication_token)))
        self.assertEqual(fetch_single_category.status_code, 200)

        edit_single_category = self.client().put('/api/v2/category/1',
                                                headers=dict(Authorization="Bearer {}".format(authentication_token)),
                                                content_type='application/json',
                                                data=json.dumps({"category_name": "Eggnog",
                                                    "category_description": "tech related gadgets"}))
        edit_category_result = json.loads(edit_single_category.data)
        self.assertEqual(edit_single_category.status_code, 200)
        self.assertEqual(edit_category_result['message'], 'success')

        fetch_single_category = self.client().get('/api/v2/category/1',
                                                headers=dict(Authorization="Bearer {}".format(authentication_token)))
        self.assertEqual(fetch_single_category.status_code, 200)
        self.assertEqual(json.loads(fetch_single_category.data)['category'][0]['name'], 'Eggnog')

    def test_user_can_delete_category(self):
        """Test that admin can delete a category"""

        self.user_authentication_register(email="ulbricht@mail.com", password="password", confirm_password="password", role='admin')
        response = self.user_authentication_login(email="ulbricht@mail.com", password="password")

        authentication_token = json.loads(response.data.decode())['token']

        category_posted = self.client().post('/api/v2/category',
                                    content_type="application/json",
                                    headers=dict(Authorization="Bearer {}".format(authentication_token)),
                                    data=json.dumps({"category_name": "technology",
                                                    "category_description": "tech related gadgets"}))
        self.assertEqual(category_posted.status_code, 201)


        delete_category = self.client().delete('/api/v2/category/1',
                                                headers=dict(Authorization="Bearer {}".format(authentication_token)))
        edit_category_result = json.loads(delete_category.data)

        self.assertEqual(delete_category.status_code, 200)
        self.assertEqual(edit_category_result['status'], 'ok')

        fetch_single_category = self.client().get('/api/v2/category/1',
                                                headers=dict(Authorization="Bearer {}".format(authentication_token)))
        self.assertEqual(fetch_single_category.status_code, 404)
