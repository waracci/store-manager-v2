"""Login endpoint [POST]"""
from flask_restplus import Namespace, Resource, reqparse
from flask import make_response, jsonify, request
from validate_email import validate_email

from ..models.User import User
from ..utils.Validator import AuthDataTransferObject

api = AuthDataTransferObject.authentication_namespace

authentication_validator_register = AuthDataTransferObject.authentication_model_register
authentication_validator_login = AuthDataTransferObject.authentication_model_login

parser = reqparse.RequestParser()
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)


@api.route('signup')
class RegistrationEndpoint(Resource):
    """Endpoint for User registration"""

    @api.doc('User registration endpoint')
    @api.expect(authentication_validator_register)
    def post(self):
        """Create new user"""

        parser.add_argument('confirm_password')
        parser.add_argument('role')

        args = parser.parse_args()
        email = args['email']
        password = args['password']
        confirm_password = args['confirm_password']
        role = args['role']

        if not validate_email(email):
            return dict(message="enter a valid email", status="failed"), 400

        if password == '' or password == ' ' or role == '' or role == ' ':
            return dict(message="Enter password and role", status="failed"), 400

        # minimum characters for password
        

        if not confirm_password:
            return dict(message="confirm password is required", status="failed"), 401

        if password != confirm_password:
            return dict(message="passwords do not match", status="failed"), 401

        if not role:
            return dict(message="Role is required", status="failed"), 401

        # add role validation

        register_user = User()
        user_registration = register_user.save_user(email, password, confirm_password, role)

        if 'error' in user_registration:
            return dict(message=user_registration["message"],status="failed"), 400
        return user_registration, 201

@api.route('login')
class LoginEndpoint(Resource):
    """Endpoint for User Login"""

    @api.expect(authentication_validator_login)
    def post(self):
        """login existing user"""

        args = parser.parse_args()
        email = args['email']
        password = args['password']
        if not email or not password:
            return dict(message="Email or password fields missing.", status="failed"), 401

        if not validate_email(email):
            return dict(message="Enter a valid email", status="failed"), 400

        user= User()
        user_login  = user.login(email, password)

        if 'error' in user_login:
            return dict(message="incorrect email or password, try again", status="failed"), 401
            
        token = user.generate_auth_token(user_login)
        return make_response(jsonify({"status": "ok", "message": "success", "token":token.decode()}), 200)
