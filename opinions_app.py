from datetime import datetime

from random import randrange

from flask import Flask, render_template, url_for, redirect, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, URLField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'my secret key'

db = SQLAlchemy(app)

# Модель БД
class Opinion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tittle = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index = True, default=datetime.utcnow)

# Форма добавления мнения
class OpinionForm(FlaskForm):
    title = StringField(
        'Введите название фильма',
        validators=[DataRequired(message="Обязательное поле"),
                    Length(1,128)]
    )
    text = TextAreaField(
        'Напишите мнение',
        validators=[DataRequired(message="Обязательное поле")],
    )
    source = URLField(
        'Добавьте ссылку на подробный обзор фильма',
        validators=[Length(1,256), Optional()]
    )
    submit = SubmitField('Добавить')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    db.session.rollback()
    return render_template('500.html'), 500

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

if __name__ == '__main__':
    app.run()