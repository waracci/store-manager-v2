from flask import request
from validate_email import validate_email

from ..models.User import User

def jwt_decode():
    return User().decode_auth_token(request.headers['Authorization'].split(" ")[1])
