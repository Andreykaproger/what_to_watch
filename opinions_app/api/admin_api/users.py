from datetime import datetime

from opinions_app import db
from opinions_app.error_handlers import InvalidAPIUsage
from opinions_app.models import User, UserRole
from opinions_app.schemas import (
    BlockUserSchema,
    MessageOutputSchema,
    UsersListSchema,
)
from opinions_app.utils.decorators import api_admin_required

from . import admin_api_bp
from .services.users_service import block_unblock_user


@admin_api_bp.route("/users", methods=["GET"])
@api_admin_required()
@admin_api_bp.output(UsersListSchema)
def list_users():
    """Список всех активных пользователей WTW"""

    users = (
        User.query.filter_by(
        is_active=True,
        role=UserRole.USER
    ).order_by(
        User.id.desc()
    ).all()
    )

    return {
        "count": len(users),
        "users": users
    }


@admin_api_bp.route("/users/blocked", methods=["GET"])
@api_admin_required()
@admin_api_bp.output(UsersListSchema)
def list_blocked_users():
    """Список заблокированных пользователей"""

    users = (
        User.query.filter_by(
        is_active=False
    ).order_by(
        User.id.desc()
    ).all()
    )

    return {
        "count": len(users),
        "users": users
    }


@admin_api_bp.route("/users/<int:id>/block", methods=["POST"])
@api_admin_required()
@admin_api_bp.input(BlockUserSchema)
@admin_api_bp.output(MessageOutputSchema)
def block_user(json_data, id):
    """Эндпоинт блокировки пользователя по Id"""

    user, error, status_code = block_unblock_user(
        "block", id, json_data
    )

    if error:
        raise InvalidAPIUsage(error, status_code)

    return {
        "message": "Пользователь заблокирован"
    }


@admin_api_bp.route("/users/<int:id>/unblock", methods=["POST"])
@api_admin_required()
@admin_api_bp.output(MessageOutputSchema)
def unblock_user(id):
    """Эндпоинт разблокировки пользователя по Id"""

    user, error, status_code = block_unblock_user(
        "unblock", id
    )

    if error:
        raise InvalidAPIUsage(error, status_code)

    return {
        "message": "Пользователь разблокирован"
    }