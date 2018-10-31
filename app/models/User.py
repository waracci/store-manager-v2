"""User model class"""
import os
from flask_bcrypt import Bcrypt
from flask_jwt_extended import get_raw_jwt
from datetime import datetime, timedelta
import psycopg2
from instance.config import secret_key, app_configuration
from ..utils.database_helper import initialize_database

class User:
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
            return dict(message="Email already exists, try a different one.", status="failed"), 400

        save_user_sql = """INSERT INTO users(email, password, role, created_at)
                          VALUES(%(email)s, %(password)s, %(role)s, %(created_at)s);"""

        self.cursor.execute(save_user_sql, new_user)
        self.connection.commit()
        # Confirm user saved
        self.cursor.execute("select * from users where email = (%s);", (self.email,))
        success_register = self.cursor.fetchone()
        self.connection.close()
        if not success_register:
            return dict(message="Failed to register.", status="failed"), 400
        return dict(message="Successful registration. Kindly login", status="ok"), 201

    
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
        return dict(error=401)

    def get_single_user(self, email):
        """Retrieve user details by email"""
        
        self.cursor.execute("SELECT * FROM users WHERE email = (%s);", (email,))
        existing_user = self.cursor.fetchone()
        self.connection.close()
        if not existing_user:
            return dict(error=401)
        return existing_user

    def logout_user(self, token):
        """Logout user by blacklisting token"""
        token = get_raw_jwt()['jti']
        blacklist_token_sql = """INSERT INTO tokens (token) VALUES ('{}')""".format(token)
        self.cursor.execute(blacklist_token_sql)
        self.connection.commit()
        self.connection.close()
        return dict(message="User log out success", status="ok"), 200


    def __repr__(self):
        return "<User '{}'>".format(self.email)
