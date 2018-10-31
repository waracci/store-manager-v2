from functools import wraps
from flask_jwt_extended import get_jwt_identity
from ..models.User import User


def admin_required_check(decorated_func):
    """Decorator to restrict routes that need admin access"""
    @wraps(decorated_func)
    def decorator(*args, **kwargs):
        current_user = User().get_single_user(get_jwt_identity())
        if not current_user:
            return dict(message="user not found", status="failed"), 404
        if current_user[3] == 'attendant':
            return dict(message="requires admin", status="failed"), 406
        return decorated_func(*args, **kwargs)
    return decorator
