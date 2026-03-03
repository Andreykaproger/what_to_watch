from flask import render_template, url_for, flash, abort, redirect
from flask_login import current_user
from random import randrange

from opinions_app.models import Opinion
from opinions_app.forms import OpinionForm
from opinions_app import db

from . import opinions_bp


def random_opinion():
    quantity = Opinion.query.filter_by(status='approved').count()
    if quantity:
        offset_value = randrange(quantity)
        opinion = Opinion.query.filter_by(status='approved').offset(offset_value).first()
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
    if opinion.status != 'approved':
        abort(404)
    return render_template('opinions/opinion.html', opinion=opinion)

@opinions_bp.route('/add', methods=['GET', 'POST'])
def add_opinion_view():
    if not current_user.is_authenticated:
        flash("Хотите добавить мнение? Авторизуйтесь!")
        return redirect(url_for('access_managment.login_view'))
    form = OpinionForm()
    if form.validate_on_submit():
        if Opinion.query.filter_by(text=form.text.data).first():
            flash("Такое мнение уже было составлено ранее!")
            return render_template('opinions/add_opinion.html', form=form)
        opinion = Opinion(
            tittle = form.title.data,
            text = form.text.data,
            source = form.source.data,
            user_id = current_user.id
        )
        db.session.add(opinion)
        db.session.commit()
        return redirect(url_for('opinions.opinion_view', id = opinion.id))
    return render_template('opinions/add_opinion.html', form=form)

@opinions_bp.route('/opinion/<int:id>', methods=['DELETE'])
def delete_opinion_view(id):
    opinion = Opinion.query.get_or_404(id)
    if opinion.user_id != current_user.id and not current_user.is_admin():
        abort(401)
    db.session.delete(opinion)
    db.session.commit()

    return redirect(url_for('opinions.opinion_view',id=id))

@opinions_bp.route('/redact_opinion/<int:id>', methods=['GET','POST'])
def redact_opinion_view(id):
    opinion = Opinion.query.get_or_404(id)
    if opinion.user_id != current_user.id and not current_user.is_admin():
        abort(401)
    form = OpinionForm(
        title = opinion.tittle,
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