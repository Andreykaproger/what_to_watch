from datetime import datetime

from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    request,
    abort
)

from opinions_app import db
from opinions_app.models import Opinion, OpinionStatus
from opinions_app.utils.decorators import admin_required

from . import admin_bp


@admin_bp.route('/opinions', methods=["GET"])
@admin_required
def opinions_list_view():
    page = request.args.get('page', 1, type=int)
    per_page = 6

    opinions = Opinion.query.filter_by(
        status=OpinionStatus.APPROVED
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return render_template(
        'admin/opinions_list.html',
        opinions=opinions
    )


@admin_bp.route('/opinions/pending', methods=["GET"])
@admin_required
def pending_opinions_view():

    page = request.args.get("page", 1, type=int)
    per_page = 6

    opinions = Opinion.query.filter_by(
        status=OpinionStatus.PENDING
    ).order_by(
        Opinion.timestamp.desc()
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return render_template(
        'admin/pending_opinions.html',
        pending_opinions=opinions
    )


@admin_bp.route('/opinions/<int:id>/approve', methods=['POST'])
@admin_required
def approve_opinion(id):

    opinion = Opinion.query.get_or_404(id)

    # if opinion.status != OpinionStatus.PENDING:
    #     abort(400)

    opinion.status = OpinionStatus.APPROVED
    opinion.moderated_at = datetime.utcnow()

    db.session.commit()

    flash("Мнение опубликовано")

    return redirect(
        url_for('admin.opinions_list_view')
    )


@admin_bp.route('/opinions/<int:id>/reject', methods=["GET"])
@admin_required
def reject_opinion_view(id):

    opinion = Opinion.query.get_or_404(id)

    if opinion.status != OpinionStatus.PENDING:
        abort(400)

    return render_template(
        'admin/reject_opinion.html',
        opinion=opinion
    )


@admin_bp.route('/opinions/<int:id>/reject/confirm',methods=['POST'])
@admin_required
def reject_opinion_confirm(id):

    opinion = Opinion.query.get_or_404(id)

    reason = request.form.get("reason")

    if not reason:

        flash("Укажите причину отказа")

        return redirect(
            url_for('admin.reject_opinion_view', id=id)
        )

    opinion.status = OpinionStatus.REJECTED
    opinion.rejection_reason = reason
    opinion.moderated_at = datetime.utcnow()

    db.session.commit()

    flash("Отзыв отклонён")

    return redirect(
        url_for('admin.pending_opinions_view')
    )

@admin_bp.route('/opinions/rejected',methods=['GET'])
@admin_required
def rejected_opinions_view():

    page = request.args.get("page", 1, type=int)
    per_page = 6

    opinions = Opinion.query.filter_by(
        status=OpinionStatus.REJECTED
    ).order_by(
        Opinion.timestamp.desc()
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return render_template(
        'admin/rejected_opinions.html',
        opinions=opinions
    )

