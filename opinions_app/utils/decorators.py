from functools import wraps
from flask_login import current_user
from flask_jwt_extended import get_jwt, verify_jwt_in_request, get_jwt_identity
from flask import abort

from opinions_app.error_handlers import InvalidAPIUsage
from opinions_app.models import User

ROLE_HIERARCHY = {
    "user": 1,
    "moderator": 2,
    "admin": 3
}

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403)

        return f(*args, **kwargs)

    return decorated_function

def api_admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if verify_jwt_in_request(optional=True) is None:
                raise InvalidAPIUsage("Вы не авторизованы", 401)

            claims = get_jwt()
            if claims.get("role") != "admin":
                raise InvalidAPIUsage("Отказано в доступе", 403)

            return fn(*args, **kwargs)

        return decorator

    return wrapper


def active_user_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if verify_jwt_in_request(optional=True) is None:
                raise InvalidAPIUsage("Вы не авторизованы", 401)

            user_id = int(get_jwt_identity())
            user = User.query.get(user_id)
            if not user or not user.is_active:
                raise InvalidAPIUsage("Пользователь заблокирован или не найден", 403)

            return fn(*args, **kwargs)

        return decorator

    return wrapper

def role_required(required_role):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()

            claims = get_jwt()

            user_role = claims.get("role", "user")

            if ROLE_HIERARCHY.get(user_role, 0) < ROLE_HIERARCHY.get(required_role, 0):
                abort(403, message="Недостаточно прав")

            return fn(*args, **kwargs)

        return decorator

    return wrapper