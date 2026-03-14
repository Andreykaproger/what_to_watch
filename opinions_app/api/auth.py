from flask import jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)

from opinions_app import db, TokenBlockList
from opinions_app.models import User
from opinions_app.schemas import (
    RegisterSchema,
    LoginSchema,
    TokenSchema,
    ProfileSchema,
    MessageOutputSchema,
    RefreshTokenSchema
)
from opinions_app.error_handlers import InvalidAPIUsage
from opinions_app.utils.decorators import active_user_required

from . import auth_api_bp


@auth_api_bp.route('/register', methods = ["POST"])
@auth_api_bp.input(RegisterSchema)
@auth_api_bp.output(MessageOutputSchema)
def api_register(json_data):
    """Регистрация нового пользователя"""

    if User.query.filter_by(email=json_data['email']).first():
        raise InvalidAPIUsage(
            'Такой E-mail уже используется',
            400
        )
    if User.query.filter_by(username=json_data['username']).first():
        raise InvalidAPIUsage(
            'Пользователь с таким именем уже зарегистрирован',
            400
        )

    user = User(
        username=json_data['username'],
        email=json_data['email']
    )
    user.set_password(json_data['password'])

    db.session.add(user)
    db.session.commit()

    return {
        "message": "Пользователь успешно зарегистрирован"
    }

@auth_api_bp.route('/login', methods = ["POST"])
@auth_api_bp.input(LoginSchema)
@auth_api_bp.output(TokenSchema)
def api_login(json_data):
    """Авторизация"""

    user = User.query.filter_by(email=json_data['email']).first()

    if not(user and user.check_password(json_data['password'])):
        raise InvalidAPIUsage("Неверный E-mail или пароль", 400)

    if not user.is_active:
        raise InvalidAPIUsage(
            f"Ваш аккаунт заблокирован по причине: {user.block_reason}",
            400
        )

    access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": "admin" if user.is_admin() else "user"
        }
    )
    refresh_token = create_refresh_token(
        identity=str(user.id)
    )

    return jsonify({
        "message": f"Добро пожаловать, {user.username}",
        "access_token": access_token,
        "refresh_token": refresh_token,
    })

@auth_api_bp.route("/logout", methods=["GET"])
@jwt_required()
@auth_api_bp.output(MessageOutputSchema)
def api_logout():
    """Выход из системы"""

    jti = get_jwt()['jti']
    blocked_token = TokenBlockList(
        jti=jti
    )
    db.session.add(blocked_token)
    db.session.commit()

    return {
        "message": "Вы вышли из системы"
    }

@auth_api_bp.route("/logout_refresh", methods=["GET"])
@jwt_required(refresh=True)
@auth_api_bp.output(MessageOutputSchema)
def api_logout_refresh():
    """Выход с удалением Refresh токена"""

    jti = get_jwt()['jti']
    blocked_token = TokenBlockList(
        jti=jti
    )
    db.session.add(blocked_token)
    db.session.commit()

    return {
        "message": "Refresh token отозван"
    }

@auth_api_bp.route("/profile", methods = ["GET"])
@active_user_required()
@auth_api_bp.output(ProfileSchema)
def api_profile():
    """Профиль пользователя"""

    user_id = int(get_jwt_identity())

    user = User.query.get(user_id)

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
    })

@auth_api_bp.route("/refresh", methods=["GET"])
@jwt_required(refresh=True)
@auth_api_bp.output(RefreshTokenSchema)
def api_refresh():
    """Получение нового Access Token по Refresh Token"""

    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    new_access_token = create_access_token(
        identity=str(user.id),
        additional_claims={
            "role": "admin" if user.is_admin() else "user"
        }
    )

    return jsonify({
        "access_token": new_access_token,
    })



