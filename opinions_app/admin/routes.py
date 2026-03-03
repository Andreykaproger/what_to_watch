from flask import render_template, redirect, url_for, flash, request
from datetime import datetime

from opinions_app.decorators import admin_required
from opinions_app.models import User, Opinion
from opinions_app import db

from . import admin_bp


@admin_bp.route("/admin_panel/dashboard")
@admin_required
def admin_panel_dashboard_view():
    users_count = User.query.count()
    opinions_count = Opinion.query.filter_by(status='approved').count()
    blocked_users = User.query.filter_by(is_active=False).count()
    pending_opinions = Opinion.query.filter_by(status='pending').count()
    return render_template(
        "admin/admin_panel_dashboard.html",
        users_count=users_count,
        opinions_count=opinions_count,
        blocked_users=blocked_users,
        pending_opinions=pending_opinions
    )

@admin_bp.route("/admin_panel/dashboard/users_list")
@admin_required
def users_list_view():
    users_list = User.query.filter_by(is_active=True).all()
    return render_template("admin/users_list.html", users_list=users_list)

@admin_bp.route("/admin_panel/dashboard/blocked_users_list")
@admin_required
def blocked_users_list_view():
    blocked_users_list = User.query.filter_by(is_active=False).all()
    return render_template(
        "admin/blocked_users_list.html",
        users_count=blocked_users_list)

@admin_bp.route("/admin_panel/dashboard/users_list/<int:id>", methods=['POST'])
@admin_required
def blocked_user(id):
    blocked_user = User.query.get_or_404(id)
    reason = request.form.get("reason")
    if not reason:
        flash("Укажите причину блокировки")
        return redirect(url_for('admin.users_list_view'))

    blocked_user.is_active = False
    blocked_user.block_reason = reason
    blocked_user.blocked_at = datetime.utcnow()
    flash("Пользователь заблокирован")
    db.session.commit()

    return redirect(url_for('admin.users_list_view'))

@admin_bp.route('/admin_panel/dashboard/blocked_users_list/<int:id>', methods=['POST'])
@admin_required
def unblocked_user(id):
    unblocked_user = User.query.get_or_404(id)
    unblocked_user.is_active = True
    db.session.commit()

@admin_bp.route('/admin_panel/dashboard/approved_opinions')
@admin_required
def opinions_list_view():
    opinions_list = Opinion.query.filter_by(status='approved').all()
    return render_template('admin/opinions_list.html', opinions_list=opinions_list)

@admin_bp.route('/admin_panel/dashboard/pending_opinions')
@admin_required
def pending_opinions_view():
    pending_opinions = Opinion.query.filter_by(status='pending').all()
    return render_template('admin/pending_opinions.html', pending_opinions=pending_opinions)

@admin_bp.route('/admin_panel/dashboard/pending_opinions/accept/<int:id>', methods=['GET', 'PATCH'])
@admin_required
def accept_opinion(id):
    opinion = Opinion.query.get_or_404(id)
    opinion.status = 'approved'
    opinion.modified_at = datetime.utcnow()
    db.session.commit()
    flash("Мнение опубликовано")
    return redirect(url_for('admin.pending_opinions_view'))

@admin_bp.route('/admin_panel/dashboard/pending_opinions/reject/<int:id>')
@admin_required
def reject_opinion_view(id):
    opinion = Opinion.query.get_or_404(id)
    return render_template(
        'admin/reject_opinion.html',
        opinion=opinion
    )

@admin_bp.route('/admin_panel/dashboard/pending_opinions/reject/<int:id>/confirm',
           methods=['POST'])
@admin_required
def reject_opinion_confirm(id):
    opinion = Opinion.query.get_or_404(id)

    reason = request.form.get("reason")

    if not reason:
        flash("Укажите причину отказа")
        return redirect(
            url_for('admin.reject_opinion_page', id=id)
        )

    opinion.status = 'rejected'
    opinion.rejection_reason = reason
    opinion.rejected_at = datetime.utcnow()

    db.session.commit()

    flash("Отзыв отклонён")
    return redirect(url_for('admin.pending_opinions_view'))