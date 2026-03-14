from datetime import datetime

from opinions_app import db
from opinions_app.models import User, Opinion
from opinions_app.error_handlers import InvalidAPIUsage
from opinions_app.utils.decorators import api_admin_required
from opinions_app.schemas import (
    BlockUserSchema,
    BlockOpinionSchema,
    UsersListSchema,
    MessageOutputSchema,
    OpinionsListSchema
)

from . import admin_api_bp

@admin_api_bp.route("/users", methods=["GET"])
@api_admin_required()
@admin_api_bp.output(UsersListSchema)
def api_users_stats():
    """Список всех активных пользователей WTW"""

    users = User.query.filter_by(
        is_active=True, role='user'
    ).all()
    users_list = [user.to_dict() for user in users]

    return {
        "Number of users": len(users_list),
        "Users": users_list,
    }

@admin_api_bp.route("/users/blocked", methods=["GET"])
@api_admin_required()
@admin_api_bp.output(UsersListSchema)
def api_blocked_users():
    """Список заблокированных пользователей"""

    blocked_users = User.query.filter_by(
        is_active=False
    ).all()

    blocked_users_list = [
        blocked_user.to_dict() for blocked_user in blocked_users
    ]
    return {
        "Number of blocked users": len(blocked_users_list),
        "Blocked users": blocked_users_list
    }

@admin_api_bp.route("/users/<int:id>/block", methods=["POST"])
@api_admin_required()
@admin_api_bp.input(BlockUserSchema)
@admin_api_bp.output(MessageOutputSchema)
def api_blocked_user(json_data, id):
    """Эндпоинт блокировки пользователя по Id"""

    user = User.query.get_or_404(id)

    if user.is_active == False:
        raise InvalidAPIUsage("Пользователь уже заблокирован", 208)

    user.is_active = False
    user.block_reason = json_data["reason"]
    user.blocked_at = datetime.utcnow()
    db.session.commit()

    return {
        "message": "Пользователь заблокирован"
    }

@admin_api_bp.route("/users/<int:id>/unblock", methods=["GET"])
@api_admin_required()
@admin_api_bp.output(MessageOutputSchema)
def api_unblocked_user(id):
    """Эндпоить разблокировки пользователя по Id"""

    user = User.query.get_or_404(id)

    if user.is_active == True:
        raise InvalidAPIUsage("Пользователь уже разблокирован", 208)

    user.is_active = True
    user.block_reason = None
    user.blocked_at = None
    db.session.commit()

    return {
        "message": "Пользователь разблокирован"
    }

@admin_api_bp.route("/opinions/pending", methods=["GET"])
@api_admin_required()
@admin_api_bp.output(OpinionsListSchema)
def api_pending_opinions():
    """Список мнений, ожидающих модерации"""

    pending_opinions = Opinion.query.filter_by(
        status='pending'
    ).all()

    pending_opinions_list = [
        pending_opinion.to_dict() for pending_opinion in pending_opinions
    ]
    return {
        "Number of pending opinions": len(pending_opinions_list),
        "Pending opinions": pending_opinions_list
    }

@admin_api_bp.route("/opinions/rejected", methods=["GET"])
@api_admin_required()
@admin_api_bp.output(OpinionsListSchema)
def api_rejected_opinions():
    """Список отклоненных мнений"""

    opinions = Opinion.query.filter_by(status='rejected').all()

    opinions_list = [opinion.to_dict() for opinion in opinions]

    return {
        "Number of rejected opinions": len(opinions_list),
        "Rejected opinions": opinions_list,
    }

@admin_api_bp.route("/opinions/<int:id>/approve", methods=["GET"])
@api_admin_required()
@admin_api_bp.output(MessageOutputSchema)
def api_accept_opinion(id):
    """Эндпоинт подтверждения мнения"""

    approved_opinion = Opinion.query.get(id)

    if approved_opinion.status == "approved":
        raise InvalidAPIUsage("Мнение уже принято", 208)

    if approved_opinion.status == "rejected":
        raise InvalidAPIUsage("Нельзя принять отклоненное мнение", 400)

    approved_opinion.status = "approved"
    approved_opinion.rejection_reason = None
    approved_opinion.moderated_at = datetime.utcnow()
    db.session.commit()

    return {
        "message": "Мнение опубликовано"
    }

@admin_api_bp.route("/opinions/<int:id>/reject", methods=["POST"])
@api_admin_required()
@admin_api_bp.input(BlockOpinionSchema)
@admin_api_bp.output(MessageOutputSchema)
def api_reject_opinion(json_data, id):
    """Эндпоинт отказа от мнения"""

    rejected_opinion = Opinion.query.get(id)

    if rejected_opinion.status == "rejected":
        raise InvalidAPIUsage("Мнение уже отклонено", 208)

    if rejected_opinion.status == "approved":
        raise InvalidAPIUsage("Нельзя отклонить принятое мнение", 400)

    rejected_opinion.status = "rejected"
    rejected_opinion.rejection_reason = json_data["reason"]
    rejected_opinion.moderated_at = datetime.utcnow()

    db.session.commit()

    return {
        "message": "Мнение отклонено"
    }