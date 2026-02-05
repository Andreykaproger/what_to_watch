from .forms import OpinionForm
from .models import Opinion
from random import randrange
from flask import abort, flash, redirect, render_template, url_for

from . import app, db

def random_opinion():
    quantity = Opinion.query.count()
    if quantity:
        offset_value = randrange(quantity)
        opinion = Opinion.query.offset(offset_value).first()
        return opinion

@app.route('/')
def index_view():
    opinion = random_opinion()
    if opinion is not None:
        return render_template('opinion.html', opinion=opinion)
    abort(404)

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