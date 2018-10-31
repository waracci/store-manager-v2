"""Login endpoint [POST]"""
from flask_restplus import Namespace, Resource, reqparse
from flask import make_response, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required

from ..utils.helpers import validate_email
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

        if validate_email(email) is None:
            response = jsonify({'message': 'enter a valid email'})
            response.status_code = 400
            return response

        if password == '' or password == ' ' or role == '' or role == ' ':
            response = jsonify({'message': 'Enter password and role'})
            response.status_code = 400
            return response

        if len(password) < 6:
            response = jsonify({'message': 'password length should be more than 6 characters'})
            response.status_code = 400
            return response

        if not confirm_password:
            response = jsonify({'message': 'confirm password is required'})
            response.status_code = 401
            return response

        if password != confirm_password:
            response = jsonify({'message': 'passwords do not match'})
            response.status_code = 401
            return response

        if not role:
            response = jsonify({'message': 'Role is required'})
            response.status_code = 401
            return response
        
        roles = ['admin', 'attendant']
        if role not in roles:
            response = jsonify({'message': 'Incorrect role format'})
            response.status_code = 401
            return response

        register_user = User()
        user_registration = register_user.save_user(email, password, confirm_password, role)
        return user_registration

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
            response = jsonify({'message': 'Email or password fields missing'})
            response.status_code = 401
            return response

        if validate_email(email) is None:
            response = jsonify({'message': 'Enter a valid email'})
            response.status_code = 400
            return response

        user= User()
        user_login  = user.login(email, password)

        if 'error' in user_login:
            response = jsonify({'message': 'incorrect email or password, try again'})
            response.status_code = 401
            return response
            
        token = create_access_token(identity=email)
        response = jsonify({'message': 'success', 'token': token})
        response.status_code = 200
        return response

@api.route('logout')
class LogoutEndpoint(Resource):
    """User logout endpoint"""
    
    @jwt_required
    def post(self):
        """Logout user"""
        print('logout')
        logout_user = User().logout_user(request.headers['Authorization'].split(" ")[1])
        return logout_user
