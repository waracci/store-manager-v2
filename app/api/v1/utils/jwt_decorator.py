# from flask import request
# from functools import wraps

# from ..models.User import User

# def jwt_required(decorated_funct):
#     @wraps(decorated_funct)

#     def decorated(*args, **kwargs):
#         authentication_token = None
#         if 'Authorization' in request.headers:
#             # Use Try catch
#             try:
#                 authentication_token = request.headers['Authorization'].split(" ")[1]
#                 user_identity = User().decode_auth_token(authentication_token)
#                 if "invalid" in user_identity:
#                     return dict(message="Invalid token"), 401
#                 if "expired" in user_identity:
#                     return dict(message="Expired token"), 401
#             except:
#                 return dict(message="Invalid token"), 401                
#         if not authentication_token:
#             return dict(message="Authorization required"), 401
#         return decorated_funct(*args, **kwargs)
#     return decorated
