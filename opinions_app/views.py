from .forms import OpinionForm
from .models import Opinion
from random import randrange
from flask import abort, flash, redirect, render_template, url_for

from . import app, db


@app.route('/')
def index_view():
    quantity = Opinion.query.count()
    if not quantity:
        return abort(404)
    offset_value = randrange(quantity)
    opinion = Opinion.query.offset(offset_value).first()
    return render_template('opinion.html', opinion=opinion)

@app.route('/opinion/<int:id>')
def opinion_view(id):
    opinion = Opinion.query.get_or_404(id)
    return render_template('opinion.html', opinion=opinion)

@app.route('/add', methods=['GET', 'POST'])
def add_opinion_view():
    form = OpinionForm()
    if form.validate_on_submit():
        if Opinion.query.filter_by(text=form.text.data).first():
            flash("Такое мнение уже было составлено ранее!")
            return render_template('add_opinion.html', form=form)
        opinion = Opinion(
            tittle = form.title.data,
            text = form.text.data,
            source = form.source.data,
        )
        db.session.add(opinion)
        db.session.commit()
        return redirect(url_for('opinion_view', id = opinion.id))
    return render_template('add_opinion.html', form=form)