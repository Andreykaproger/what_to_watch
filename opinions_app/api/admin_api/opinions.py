from opinions_app.error_handlers import InvalidAPIUsage
from opinions_app.models import Opinion, OpinionStatus
from opinions_app.schemas import (
    BlockOpinionSchema,
    MessageOutputSchema,
)
from opinions_app.schemas.admin import  OpinionsListSchema
from opinions_app.utils.decorators import api_admin_required

from . import admin_api_bp
from .services.opinions_service import approve_reject_opinion


@admin_api_bp.route("/opinions/pending", methods=["GET"])
@api_admin_required()
@admin_api_bp.output(OpinionsListSchema)
def api_pending_opinions():
    """Список мнений, ожидающих модерации"""

    opinions = (
        Opinion.query.filter_by(
        status=OpinionStatus.PENDING
    ).order_by(
        Opinion.timestamp.desc()
    ).all()
    )

    return {
        "count": len(opinions),
        "opinions": opinions
    }


@admin_api_bp.route("/opinions/rejected", methods=["GET"])
@api_admin_required()
@admin_api_bp.output(OpinionsListSchema)
def api_rejected_opinions():
    """Список отклоненных мнений"""

    opinions = (
        Opinion.query.filter_by(
        status=OpinionStatus.REJECTED
    ).order_by(
        Opinion.timestamp.desc()
    ).all()
    )

    return {
        "count": len(opinions),
        "opinions": opinions,
    }


@admin_api_bp.route("/opinions/<int:id>/approve", methods=["POST"])
@api_admin_required()
@admin_api_bp.output(MessageOutputSchema)
def api_accept_opinion(id):
    """Эндпоинт подтверждения мнения"""

    opinion, error, status_code = approve_reject_opinion(
        "approve", id
    )

    if error:
        raise InvalidAPIUsage(error, status_code)


    return {
        "message": "Мнение опубликовано"
    }


@admin_api_bp.route("/opinions/<int:id>/reject", methods=["POST"])
@api_admin_required()
@admin_api_bp.input(BlockOpinionSchema)
@admin_api_bp.output(MessageOutputSchema)
def api_reject_opinion(json_data, id):
    """Эндпоинт отказа от мнения"""

    opinion, error, status_code = approve_reject_opinion(
        "reject", id, json_data
    )

    if error:
        raise InvalidAPIUsage(error, status_code)

    return {
        "message": "Мнение отклонено"
    }