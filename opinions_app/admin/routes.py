from flask import render_template, redirect, url_for, flash, request, abort
from datetime import datetime

from opinions_app.utils.decorators import admin_required
from opinions_app.models import User, Opinion
from opinions_app import db

from . import admin_bp

@admin_bp.route(
    "/"
)
@admin_required
def admin_panel_dashboard_view():
    users_count = User.query.count()
    opinions_count = Opinion.query.filter_by(
        status='approved'
    ).count()
    blocked_users = User.query.filter_by(
        is_active=False
    ).count()
    pending_opinions = Opinion.query.filter_by(
        status='pending'
    ).count()
    return render_template(
        "admin/admin_panel_dashboard.html",
        users_count=users_count,
        opinions_count=opinions_count,
        blocked_users=blocked_users,
        pending_opinions=pending_opinions
    )

@admin_bp.route(
    "/users-list"
)
@admin_required
def users_list_view():
    page = request.args.get("page",1, type=int)
    per_page = 6

    users_list = User.query.filter_by(
        is_active=True, role='user'
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return render_template(
        "admin/users_list.html",
        users_list=users_list
    )

@admin_bp.route(
    "/blocked-users"
)
@admin_required
def blocked_users_list_view():
    page = request.args.get("page", 1, type=int)
    per_page= 6

    blocked_users_list = User.query.filter_by(
        is_active=False
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False,
    )

    return render_template(
        "admin/blocked_users_list.html",
        users_list=blocked_users_list)

@admin_bp.route(
    '/users-list/<int:id>/block'
)
@admin_required
def blocked_user_view(id):
    user = User.query.get_or_404(id)
    return render_template(
        'admin/blocked_user.html',
        user=user
    )

@admin_bp.route(
    "/users-list/<int:id>/block/confirm",
    methods=['POST']
)
@admin_required
def blocked_user(id):
    blocked_user = User.query.get_or_404(id)
    reason = request.form.get("reason")
    if not reason:
        flash("Укажите причину блокировки")
        return redirect(
            url_for('admin.blocked_user_view', id=id)
        )

    blocked_user.is_active = False
    blocked_user.block_reason = reason
    blocked_user.blocked_at = datetime.utcnow()
    Opinion.query.filter_by(user_id = id).update({"status": "rejected"})
    flash("Пользователь заблокирован")

    db.session.commit()

    return redirect(
        url_for('admin.users_list_view')
    )

@admin_bp.route(
    '/blocked-users-list/<int:id>/unblock',
    methods=['POST']
)
@admin_required
def unblocked_user(id):
    unblocked_user = User.query.get_or_404(id)
    unblocked_user.is_active = True
    Opinion.query.filter_by(user_id = id).update({"status": "pending"})
    db.session.commit()
    flash('Пользователь разблокирован')

    return redirect(url_for('admin.blocked_users_list_view'))

@admin_bp.route(
    '/approved-opinions'
)
@admin_required
def opinions_list_view():
    page = request.args.get('page', 1, type=int)
    per_page = 6

    opinions_list = Opinion.query.filter_by(status='approved').order_by(
        Opinion.timestamp.desc()
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return render_template(
        'admin/opinions_list.html',
        opinions_list=opinions_list
    )

@admin_bp.route(
    '/pending-opinions'
)
@admin_required
def pending_opinions_view():
    page = request.args.get("page", 1, type=int)
    per_page = 6
    pending_opinions = Opinion.query.filter_by(
        status='pending'
    ).order_by(
        Opinion.timestamp.desc()
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return render_template(
        'admin/pending_opinions.html',
        pending_opinions=pending_opinions
    )

@admin_bp.route(
    '/pending-opinions/<int:id>/approve',
    methods=['POST']
)
@admin_required
def approve_opinion(id):
    opinion = Opinion.query.get_or_404(id)
    opinion.status = 'approved'
    opinion.moderated_at = datetime.utcnow()
    db.session.commit()
    flash("Мнение опубликовано")
    return redirect(
        url_for('admin.pending_opinions_view')
    )

@admin_bp.route(
    '/pending-opinions/<int:id>/reject'
)
@admin_required
def reject_opinion_view(id):
    opinion = Opinion.query.get_or_404(id)

    if opinion.status != "pending":
        abort(400)

    return render_template(
        'admin/reject_opinion.html',
        opinion=opinion
    )

@admin_bp.route(
    '/pending-opinions/<int:id>/reject/confirm',
    methods=['POST']
)
@admin_required
def reject_opinion_confirm(id):
    opinion = Opinion.query.get_or_404(id)

    reason = request.form.get("reason")

    if not reason:
        flash("Укажите причину отказа")
        return redirect(
            url_for('admin.reject_opinion_view', id=id)
        )

    opinion.status = 'rejected'
    opinion.rejection_reason = reason
    opinion.rejected_at = datetime.utcnow()

    db.session.commit()

    flash("Отзыв отклонён")
    return redirect(
        url_for('admin.pending_opinions_view')
    )