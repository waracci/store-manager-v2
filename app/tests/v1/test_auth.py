import json
from app.tests.v1.base_test import BaseTest

class TestAuth(BaseTest):
    """Test Suite for User Authentication, (login and registration)"""
    
    def test_user_registration(self):
        """Test that a user can register successfully"""

        user_registration = self.client().post('/api/v2/auth/signup',
                            content_type="application/json",
                            data=json.dumps({
                                            "email": "u3ser@user.com",
                                            "password": "password",
                                            "confirm_password": "password",
                                            "role": "admin"
                                           }))

        user_reg_result = json.loads(user_registration.data)
        self.assertEqual(user_registration.status_code, 201)
        self.assertEqual(user_reg_result['status'], 'ok')

    def test_confirm_password(self):
        """Test that password and confirm password fields match"""

        user_registration = self.client().post('/api/v2/auth/signup',
                            content_type="application/json",
                            data=json.dumps({"email": "user@user.com",
                                             "password": "password",
                                             "confirm_password": "bad_password",
                                              "role": "admin"}))
        user_reg_result = json.loads(user_registration.data)
        self.assertEqual(user_registration.status_code, 401)
        self.assertEqual(user_reg_result['message'], 'passwords do not match')

    def test_no_password_provided(self):
        """Test that user provided password"""

        user_registration = self.client().post('/api/v2/auth/signup',
                            content_type="application/json",
                            data=json.dumps({"email": "user@user.com",
                                             "password": "",
                                             "confirm_password": "password",
                                              "role": "admin"}))
        user_reg_result = json.loads(user_registration.data)
        self.assertEqual(user_registration.status_code, 400)
        self.assertEqual(user_reg_result['message'], 'Enter password and role')

    def test_existing_user(self):
        """Test that same email can not register twice"""

        user_registration = self.client().post('/api/v2/auth/signup',
                            content_type="application/json",
                            data=json.dumps({"email": "user@user.com",
                                             "password": "password",
                                             "confirm_password": "password",
                                              "role": "admin"}))
        user_reg_result = json.loads(user_registration.data)
        self.assertEqual(user_registration.status_code, 201)
        self.assertEqual(user_reg_result['status'], 'ok')

        user_registration = self.client().post('/api/v2/auth/signup',
                            content_type="application/json",
                            data=json.dumps({"email": "user@user.com",
                                             "password": "password",
                                             "confirm_password": "password",
                                              "role": "admin"}))
        user_reg_result = json.loads(user_registration.data)
        self.assertEqual(user_registration.status_code, 400)
        self.assertEqual(user_reg_result['message'], 'Email already exists, try a different one.')

    def test_login_user(self):
        """Test that a user can login successfully"""

        user_registration = self.client().post('/api/v2/auth/signup',
                            content_type="application/json",
                            data=json.dumps({"email": "user@user.com",
                                             "password": "password",
                                             "confirm_password": "password",
                                              "role": "admin"}))
        user_reg_result = json.loads(user_registration.data)
        self.assertEqual(user_registration.status_code, 201)
        self.assertEqual(user_reg_result['status'], 'ok')

        user_login = self.client().post('/api/v2/auth/login',
                     content_type="application/json",
                     data=json.dumps({"email": "user@user.com",
                                      "password": "password"}))
        user_login_result = json.loads(user_login.data)
        self.assertEqual(user_login.status_code, 200)
        self.assertEqual(user_login_result['status'], 'ok')

    def test_user_login_incorrect_password(self):
        """Test that user can not login with incorrect password"""

        user_registration = self.client().post('/api/v2/auth/signup',
                            content_type="application/json",
                            data=json.dumps({"email": "user@user.com",
                                             "password": "password",
                                             "confirm_password": "password",
                                              "role": "admin"}))
        user_reg_result = json.loads(user_registration.data)
        self.assertEqual(user_registration.status_code, 201)
        self.assertEqual(user_reg_result['status'], 'ok')

        user_login = self.client().post('/api/v2/auth/login',
                     content_type="application/json",
                     data=json.dumps({"email": "user@user.com",
                                      "password": "bad_password"}))
        user_login_result = json.loads(user_login.data)
        self.assertEqual(user_login.status_code, 401)
        self.assertEqual(user_login_result['message'], 'incorrect email or password, try again')

    def test_login_no_provided_password(self):
        """Test that password must be provided during login"""

        user_registration = self.client().post('/api/v2/auth/signup',
                            content_type="application/json",
                            data=json.dumps({"email": "user@user.com",
                                             "password": "password",
                                             "confirm_password": "password",
                                              "role": "admin"}))
        user_reg_result = json.loads(user_registration.data)
        self.assertEqual(user_registration.status_code, 201)
        self.assertEqual(user_reg_result['status'], 'ok')

        user_login = self.client().post('/api/v2/auth/login',
                     content_type="application/json",
                     data=json.dumps({"email": "user@user.com",
                                      "password": ""}))
        user_login_result = json.loads(user_login.data)
        self.assertEqual(user_login.status_code, 401)
        self.assertEqual(user_login_result['message'], 'Email or password fields missing.')

    def test_login_unregistered_account(self):
        """Test that login is successful for registered accounts only"""

        user_login = self.client().post('/api/v2/auth/login',
                     content_type="application/json",
                     data=json.dumps({"email": "user@user.com",
                                      "password": "password"}))
        user_login_result = json.loads(user_login.data)
        self.assertEqual(user_login.status_code, 401)
        self.assertEqual(user_login_result['message'], 'incorrect email or password, try again')

    def test_invalid_email_format_register(self):
        """Test that only accurate and correct formats allowed"""

        user_registration = self.client().post('/api/v2/auth/signup',
                            content_type="application/json",
                            data=json.dumps({"email": "user.user*com",
                                             "password": "password",
                                             "confirm_password": "password",
                                             "role": "admin"}))
        user_reg_result = json.loads(user_registration.data)
        self.assertEqual(user_registration.status_code, 400)
        self.assertEqual(user_reg_result['message'], 'enter a valid email')

    def test_invalid_email_format_login(self):
        """Test that only accurate and correct formats allowed"""

        user_registration = self.client().post('/api/v2/auth/signup',
                            content_type="application/json",
                            data=json.dumps({"email": "user@user.com",
                                             "password": "password",
                                             "confirm_password": "password",
                                              "role": "admin"}))
        user_reg_result = json.loads(user_registration.data)
        self.assertEqual(user_registration.status_code, 201)
        self.assertEqual(user_reg_result['status'], 'ok')

        user_login = self.client().post('/api/v2/auth/login',
                     content_type="application/json",
                     data=json.dumps({"email": "user.user*com",
                                      "password": "bad_password"}))
        user_login_result = json.loads(user_login.data)
        self.assertEqual(user_login.status_code, 400)
        self.assertEqual(user_login_result['message'], 'Enter a valid email')
