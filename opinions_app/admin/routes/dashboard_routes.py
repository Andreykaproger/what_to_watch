from flask import render_template

from opinions_app.models import User, Opinion, OpinionStatus

from opinions_app.utils.decorators import admin_required

from . import admin_bp


@admin_bp.route("/", methods=["GET"])
@admin_required
def admin_panel_dashboard_view():

    users_count = User.query.count()

    opinions_count = Opinion.query.filter_by(
        status=OpinionStatus.APPROVED
    ).count()

    blocked_users = User.query.filter_by(
        is_active=False
    ).count()

    pending_opinions = Opinion.query.filter_by(
        status=OpinionStatus.PENDING
    ).count()

    rejected_opinions = Opinion.query.filter_by(
        status=OpinionStatus.REJECTED
    ).count()

    return render_template(
        "admin/admin_panel_dashboard.html",
        users_count=users_count,
        opinions_count=opinions_count,
        blocked_users=blocked_users,
        pending_opinions=pending_opinions,
        rejected_opinions=rejected_opinions
    )