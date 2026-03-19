from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)

from opinions_app import db
from opinions_app.error_handlers import InvalidAPIUsage
from opinions_app.models import User
from opinions_app.schemas import (
    LoginSchema,
    MessageOutputSchema,
    ProfileSchema,
    RefreshTokenSchema,
    RegisterSchema,
    TokenSchema,
)
from opinions_app.utils.decorators import active_user_required
from opinions_app.models import TokenBlockList
from opinions_app.access_managment.services import auth_service

from . import auth_api_bp


def generate_access_token(user):
    return create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": user.role.value
        }
    )


def revoke_token():
    jti = get_jwt()["jti"]
    db.session.add(TokenBlockList(jti=jti))
    db.session.commit()


@auth_api_bp.route('/register', methods = ["POST"])
@auth_api_bp.input(RegisterSchema)
@auth_api_bp.output(MessageOutputSchema)
def register_user(json_data):
    """Регистрация нового пользователя"""

    user, error = auth_service.register_user(
        json_data['username'],
        json_data['email'],
        json_data['password']
    )

    if error:
        raise InvalidAPIUsage(error, 400)

    return {
        "message": "Пользователь успешно зарегистрирован"
    }


@auth_api_bp.route('/login', methods = ["POST"])
@auth_api_bp.input(LoginSchema)
@auth_api_bp.output(TokenSchema)
def login_user(json_data):
    """Авторизация"""

    user, error = auth_service.authenticate_user(
        json_data['email'],
        json_data['password']
    )

    if error:
        raise InvalidAPIUsage(error, 400)

    access_token = generate_access_token(user)

    refresh_token = create_refresh_token(
        identity=str(user.id)
    )

    return {
        "message": f"Добро пожаловать, {user.username}",
        "access_token": access_token,
        "refresh_token": refresh_token,
    }


@auth_api_bp.route("/logout", methods=["POST"])
@jwt_required()
@auth_api_bp.output(MessageOutputSchema)
def logout_user():
    """Выход из системы"""

    revoke_token()

    return {
        "message": "Вы вышли из системы"
    }


@auth_api_bp.route("/logout-refresh", methods=["POST"])
@jwt_required(refresh=True)
@auth_api_bp.output(MessageOutputSchema)
def logout_refresh():
    """Выход с удалением Refresh токена"""

    revoke_token()

    return {
        "message": "Refresh token отозван"
    }


@auth_api_bp.route("/profile", methods = ["GET"])
@active_user_required()
@auth_api_bp.output(ProfileSchema)
def user_profile():
    """Профиль пользователя"""

    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if not user:
        raise InvalidAPIUsage("Пользователь не найден", 404)

    return user


@auth_api_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
@auth_api_bp.output(RefreshTokenSchema)
def refresh_token():
    """Получение нового Access Token по Refresh Token"""

    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if not user:
        raise InvalidAPIUsage("Пользователь не найден", 404)

    new_access_token = generate_access_token(user)

    return {
        "access_token": new_access_token,
    }