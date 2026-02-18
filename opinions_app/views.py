from .forms import OpinionForm, RegisterForm, LoginForm
from .models import Opinion, User
from random import randrange
from flask import abort, flash, redirect, render_template, url_for
from flask_login import login_required, current_user, login_user, logout_user

from . import app, db


@app.route('/register', methods=['GET', 'POST'])
def register_view():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username = form.username.data,
            email = form.email.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)

        flash("Регистрация успешна")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_view():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Авторизация завершена!')
            return redirect(url_for('index_view'))
        else:
            flash('Неверный E-Mail или пароль!')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout_view():
    logout_user()
    return redirect(url_for('index_view'))


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
@login_required
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
            user_id = current_user.id
        )
        db.session.add(opinion)
        db.session.commit()
        return redirect(url_for('opinion_view', id = opinion.id))
    return render_template('add_opinion.html', form=form)


