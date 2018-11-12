"""Login endpoint [POST]"""
from flask_restplus import Namespace, Resource, reqparse
from flask import make_response, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from ..utils.helpers import validate_email
from ..models.User import User
from ..utils.admin_required import admin_required_check
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
            return dict(message="enter a valid email", status="failed"), 400

        if password == '' or password == ' ' or role == '' or role == ' ':
            return dict(message="Enter password and role", status="failed"), 400

        if len(password) < 6:
            return dict(message="password length should be more than 6 characters", status="failed"), 400        

        if not confirm_password:
            return dict(message="confirm password is required", status="failed"), 401

        if password != confirm_password:
            return dict(message="passwords do not match", status="failed"), 401

        if not role:
            return dict(message="Role is required", status="failed"), 401
        
        roles = ['admin', 'attendant']
        if role not in roles:
            return dict(message="Incorrect role format", status="failed"), 401

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
            return dict(message="Email or password fields missing.", status="failed"), 401

        if validate_email(email) is None:
            return dict(message="Enter a valid email", status="failed"), 400

        user= User()
        user_login  = user.login(email, password)

        if 'error' in user_login:
            return dict(message="incorrect email or password, try again", status="failed"), 401
            
        token = create_access_token(identity=email)
        return make_response(jsonify({"status": "ok", "message": "success", "token":token}), 200)

@api.route('logout')
class LogoutEndpoint(Resource):
    """User logout endpoint"""
    
    @jwt_required
    def post(self):
        """Logout user"""
        logout_user = User().logout_user(request.headers['Authorization'].split(" ")[1])
        return logout_user

@api.route('attendants')
class AttendantsEndpoint(Resource):
    """Attendants EndPoints"""

    @jwt_required
    @admin_required_check
    def get(self):
        user = User()
        all_attendants = user.retrieve_all_attendants()
        if 'error' in all_attendants:
            return dict(attendants=[], message="no attendants in store"), 404
        return dict(attendants=all_attendants, status="ok"), 200
