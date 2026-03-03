from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required

from opinions_app.forms import LoginForm, RegisterForm
from opinions_app.models import User
from opinions_app import db

from . import access_bp


@access_bp.route('/register', methods=['GET', 'POST'])
def register_view():
    form = RegisterForm()
    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash("Такое имя уже существует!")
            return render_template('access_managment/register.html', form=form)

        user = User(
            username = form.username.data,
            email = form.email.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Регистрация успешна")
        login_user(user)
        return redirect(url_for('opinions.index_view'))

    return render_template('access_managment/register.html', form=form)

@access_bp.route('/login', methods=['GET', 'POST'])
def login_view():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if not user.is_active:
            flash("Ваш аккаунт заблокирован")
            return redirect(url_for('opinions.login_view'))
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Авторизация завершена!')
            return redirect(url_for('opinions.index_view'))
        else:
            flash('Неверный E-Mail или пароль!')
    return render_template('access_managment/login.html', form=form)

@access_bp.route('/logout')
@login_required
def logout_view():
    logout_user()
    return redirect(url_for('opinions.index_view'))