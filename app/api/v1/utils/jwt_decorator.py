from flask import request
from functools import wraps

from ..models.User import User

def jwt_required(f):
    @wraps(f)

    def decorated(*args, **kwargs):
        authentication_token = None

        if 'Authorization' in request.headers:
            authentication_token = request.headers['Authorization']
        if not authentication_token:
            return dict(message="Authorization required"), 401
        try:
            user = User()
            current_user = user.decode_auth_token(authentication_token)
        except:
            return dict(message="invalid token, please login again"), 403
        return f(*args, **kwargs)
    return decorated
