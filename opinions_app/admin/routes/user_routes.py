from datetime import datetime

from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request,
)

from opinions_app import db
from opinions_app.models import User, UserRole
from opinions_app.utils.decorators import admin_required

from . import admin_bp


@admin_bp.route("/users", methods=["GET"])
@admin_required
def users_list_view():

    page  = request.args.get("page", 1, type=int)
    per_page = 6

    users = User.query.filter_by(
        is_active=True,
        role=UserRole.USER
    ).order_by(
        User.id.desc()
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return render_template(
        "admin/users_list.html",
        users_list=users
    )


@admin_bp.route("/users/blocked", methods=["GET"])
@admin_required
def blocked_users_list_view():

    page = request.args.get("page", 1, type=int)
    per_page = 6

    users = User.query.filter_by(
        is_active=False
    ).order_by(
        User.id.desc()
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False,
    )

    return render_template(
        "admin/blocked_users_list.html",
        users_list=users
    )


@admin_bp.route('/users/<int:id>/block', methods=["GET"])
@admin_required
def blocked_user_view(id):

    user = User.query.get_or_404(id)

    return render_template(
        'admin/blocked_user.html',
        user=user
    )


@admin_bp.route("/users/<int:id>/block/confirm", methods=['POST'])
@admin_required
def blocked_user(id):

    user = User.query.get_or_404(id)

    reason = request.form.get("reason")

    if not reason:
        flash("Укажите причину блокировки")

        return redirect(
            url_for('admin.blocked_user_view', id=id)
        )

    user.is_active = False
    user.block_reason = reason
    user.blocked_at = datetime.utcnow()

    flash("Пользователь заблокирован")

    db.session.commit()

    return redirect(
        url_for('admin.users_list_view')
    )


@admin_bp.route('/users/<int:id>/unblock',methods=['POST'])
@admin_required
def unblocked_user(id):

    user = User.query.get_or_404(id)

    user.is_active = True
    user.block_reason = None
    user.blocked_at = None

    db.session.commit()

    flash('Пользователь разблокирован')

    return redirect(url_for('admin.blocked_users_list_view'))