"""User model class"""
import os
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta
import psycopg2
from instance.config import secret_key, app_configuration
from ..utils.database_helper import initialize_database

class user:
    """User class contains user constructor and authentication methods"""
    def __init__(self):
        """Initialize User Object with an email and password"""
         self.connection = initialize_database()
        self.cursor = self.connection.cursor()

    def validate_user_password(self, password):
        """Compare the user entered password and user registered password"""

        return Bcrypt().check_password_hash(self.password, password)

    def save_user(self, email, password, confirm_password, role):
        """Save User Object to Datastructure (dictionary)"""

        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()
        self.role = role
        self.created_at = datetime.now()
        self.id = len(User.registered_users) + 1

        new_user = dict(
            email=self.email,
            password=self.password,
            role=self.role,
            created_at=self.created_at
        )

        self.cursor.execute("SELECT * FROM users WHERE email = (%s);", (self.email,))
        result = self.cursor.fetchone()
        if result:
            self.connection.close()
            return dict(message="Email already exists, try a different one.", error=409)

        save_user_sql = """INSERT INTO users(email, password, role, created_at)
                          VALUES(%(email)s, %(password)s, %(role)s, %(created_at)s);"""

        self.cursor.execute(save_user_sql, new_user)
        self.connection.commit()
        # Confirm user saved
        self.cursor.execute("select * from users where email = (%s);", (self.email,))
        success_register = self.cursor.fetchone()
        self.connection.close()
        if not success_register:
            return dict(message="Failed to register.", error=404)
        return dict(message="Successful registration. Kindly login")

    
    def login(self, email, password):
        """Login user"""
        self.cursor.execute("SELECT email, password FROM users WHERE email = (%s);", (email,))
        existing_user = self.cursor.fetchone()
        self.connection.close()
        if not existing_user:
            return dict(error=401)
        password_decode = Bcrypt().check_password_hash(existing_user[1], password)
        if password_decode:
            return existing_user[0]
        return dict(message="Incorrect credentials", error=401)

    def get_single_user(self, email):
        """Retrieve user details by email"""
        
        self.cursor.execute("SELECT * FROM users WHERE email = (%s);", (email,))
        existing_user = self.cursor.fetchone()
        self.connection.close()
        if not existing_user:
            return dict(error=401)
        return existing_user

    def generate_auth_token(self, email):
        """method to generate access token"""

        try:
            jwt_payload = {
                'exp': datetime.now() + timedelta(days=1, seconds=5, options={'verify_iat': False}),
                'iat': datetime.now(),
                'sub': email
            }
            return jwt.encode(
                jwt_payload,
                secret_key,
                algorithm='HS256')

        except Exception as exception_msg:
            return exception_msg

    def decode_auth_token(self, authentication_token):
        """method to decode the authentication token"""

        try:
            payload = jwt.decode(authentication_token, secret_key)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please sign in again'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please sign in again'

    def __repr__(self):
        return "<User '{}'>".format(self.email)


