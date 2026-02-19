from .forms import OpinionForm, RegisterForm, LoginForm
from .models import Opinion, User
from .decorators import admin_required
from random import randrange
from flask import abort, flash, redirect, render_template, url_for
from flask_login import login_required, current_user, login_user, logout_user

from . import app, db

@app.route('/admin')
@admin_required
def admin_view():
    users = User.query.all()
    return render_template('admin.html', users=users)

@app.route('/register', methods=['GET', 'POST'])
def register_view():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash("Такое имя уже существует!")
            return render_template('register.html', form=form)

        user = User(
            username = form.username.data,
            email = form.email.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Регистрация успешна")
        login_user(user)
        return redirect(url_for('index_view'))

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
def add_opinion_view():
    if not current_user.is_authenticated:
        flash("Хотите добавить мнение? Авторизуйтесь!")
        return redirect(url_for('login_view'))
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

@app.route('/opinion/<int:id>', methods=['DELETE'])
def delete_opinion_view(id):
    opinion = Opinion.query.get_or_404(id)
    if opinion.user_id != current_user.id and not current_user.is_admin():
        abort(401)
    db.session.delete(opinion)
    db.session.commit()

    return redirect(url_for('opinion_view', id = id))

@app.route('/redact_opinion/<int:id>', methods=['GET','POST'])
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
            return render_template('add_opinion.html', form=form)
        opinion.title = form.title.data
        opinion.text = form.text.data
        opinion.source = form.source.data
        flash('Мнение успешно отредактировано')
        db.session.commit()
        return redirect(url_for('opinion_view', id = opinion.id))

    return render_template('add_opinion.html', form=form)

@app.route("/user/<string:username>")
def user_profile_view(username):
    user = User.query.filter_by(username=username).first()
    opinions = Opinion.query.filter_by(user_id=user.id).all()
    return render_template('user_profile.html', user=user, opinions=opinions)





