from flask import render_template, url_for, flash, abort, redirect
from flask_login import current_user, login_required
from sqlalchemy.sql.expression import func

from opinions_app.models import Opinion
from opinions_app.forms import OpinionForm
from opinions_app import db

from . import opinions_bp


def random_opinion():
    opinion = Opinion.visible().order_by(func.random()).first()

    return opinion

@opinions_bp.route('/')
def index_view():
    opinion = random_opinion()

    if opinion is not None:
        return render_template('opinions/opinion.html', opinion=opinion)

    abort(404)

@opinions_bp.route('/opinion/<int:id>')
def opinion_view(id):
    opinion = Opinion.query.get_or_404(id)

    if not opinion.is_visible_to(current_user):
        abort(404)

    return render_template('opinions/opinion.html', opinion=opinion)

@opinions_bp.route('/opinion/add', methods=['GET', 'POST'])
@login_required
def add_opinion_view():
    form = OpinionForm()
    if form.validate_on_submit():
        if Opinion.query.filter_by(text=form.text.data).first():
            flash("Такое мнение уже было составлено ранее!")

        opinion = Opinion(
            title = form.title.data,
            text = form.text.data,
            source = form.source.data,
            user_id = current_user.id
        )

        db.session.add(opinion)
        db.session.commit()
        flash("Мнение отправлено на модерацию")

        return redirect(url_for('opinions.opinion_view', id = opinion.id))

    return render_template('opinions/add_opinion.html', form=form)

@opinions_bp.route('/opinion/<int:id>/delete', methods=['POST'])
@login_required
def delete_opinion(id):
    opinion = Opinion.query.get_or_404(id)

    if opinion.user_id != current_user.id and not current_user.is_admin():
        abort(403)

    db.session.delete(opinion)
    db.session.commit()
    flash("Мнение удалено")

    return redirect(url_for('users.user_profile_view',username=current_user.username))

@opinions_bp.route('/opinion/<int:id>/redact', methods=['GET','POST'])
@login_required
def redact_opinion_view(id):
    opinion = Opinion.query.get_or_404(id)

    if opinion.user_id != current_user.id and not current_user.is_admin():
        abort(403)

    form = OpinionForm(
        title = opinion.title,
        text = opinion.text,
        source = opinion.source,
    )

    if form.validate_on_submit():

        if Opinion.query.filter_by(text=form.text.data).first() is not None:
            flash("Такое мнение уже было составлено ранее!")
            return render_template('opinions/add_opinion.html', form=form)

        opinion.title = form.title.data
        opinion.text = form.text.data
        opinion.source = form.source.data
        flash('Мнение успешно отредактировано')

        db.session.commit()
        return redirect(url_for('opinions.opinion_view', id = opinion.id))

    return render_template('opinions/add_opinion.html', form=form)