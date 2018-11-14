import unittest
import json
import psycopg2

from app import create_app
from instance.config import app_configuration
from .data import user_data, user_attendant_data, user_login_data, user_attendant_data2, user_login_data2


class BaseTest(unittest.TestCase):
    """Base class for all tests"""
    baseUrl = '/api/v2/'

    def setUp(self):
        """Initialize a test environment to run tests"""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client

    def user_authentication_register_admin(self):
        """Method to Register a user successfully"""

        return self.client().post('{}auth/signup'.format(self.baseUrl),
                            content_type="application/json",
                            data=json.dumps(user_data))

    def user_authentication_register_attendant(self):
        """Method to Register a user successfully"""

        return self.client().post('{}auth/signup'.format(self.baseUrl),
                            content_type="application/json",
                            data=json.dumps(user_attendant_data))

    def user_authentication_register_attendant2(self):
        """Method to Register a user successfully"""

        return self.client().post('{}auth/signup'.format(self.baseUrl),
                            content_type="application/json",
                            data=json.dumps(user_attendant_data2))

    def user_authentication_login(self):
        """Method to Login an existing user successfully"""

        return self.client().post('{}auth/login'.format(self.baseUrl),
                            content_type="application/json",
                            data=json.dumps(user_login_data))
                            
    def user_authentication_login2(self):
        """Method to Login an existing user successfully"""

        return self.client().post('{}auth/login'.format(self.baseUrl),
                            content_type="application/json",
                            data=json.dumps(user_login_data2))
    def tearDown(self):
        """Remove test variables and clear the test database"""
        database_config=app_configuration['testing'].DATABASE_CONNECTION_URL
        connection=psycopg2.connect(database_config)
        cursor=connection.cursor()
        cursor.execute("DROP TABLE users, products, sales, categories")
        connection.commit()
        connection.close()
