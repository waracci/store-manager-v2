import unittest
import json
import psycopg2

from app import create_app
from instance.config import app_configuration

class BaseTest(unittest.TestCase):
    """Base class for all tests"""

    def setUp(self):
        """Initialize a test environment to run tests"""
        self.app = create_app(config_name='testing')
        self.client = self.app.test_client

    def user_authentication_register(self, email, password, confirm_password, role):
        """Method to Register a user successfully"""

        return self.client().post('/api/v2/auth/signup',
                            content_type="application/json",
                            data=json.dumps({"email": email,
                                             "password": password,
                                             "confirm_password": confirm_password,
                                              "role": role}))

    def user_authentication_login(self, email, password):
        """Method to Login an existing user successfully"""

        return self.client().post('/api/v2/auth/login',
                            content_type="application/json",
                            data=json.dumps({"email": email,
                                             "password": password}))

    def tearDown(self):
        """Remove test variables and clear the test database"""
        database_config = app_configuration['testing'].DATABASE_CONNECTION_URL
        connection = psycopg2.connect(database_config)
        cursor = connection.cursor()
        cursor.execute("DROP TABLE users, products")
        connection.commit()
        connection.close()
