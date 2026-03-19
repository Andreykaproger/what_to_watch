from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from opinions_app.forms import LoginForm, RegisterForm

from ..services import auth_service

from . import access_bp


@access_bp.route('/register', methods=['GET', 'POST'])
def register_view():

    form = RegisterForm()

    if form.validate_on_submit():

        user, error = auth_service.register_user(
            form.username.data,
            form.email.data,
            form.password.data
        )

        if error:
            flash(error)
            return render_template(
                'access_managment/register.html',
                form=form
            )

        login_user(user)

        flash("Регистрация успешна")

        return redirect(url_for('opinions.index_view'))

    return render_template('access_managment/register.html', form=form)

@access_bp.route('/login', methods=['POST', 'GET'])
def login_view():

    form = LoginForm()

    if form.validate_on_submit():

        user, error = auth_service.authenticate_user(
            form.email.data,
            form.password.data
        )

        if error:
            flash(error)
            return render_template(
                'access_managment/login.html',
                form=form
            )

        login_user(user)

        flash("Авторизация завершена!")

        return redirect(url_for('opinions.index_view'))

    return render_template('access_managment/login.html', form=form)

@access_bp.route('/logout', methods=["GET"])
@login_required
def logout_view():

    logout_user()

    return redirect(url_for('opinions.index_view'))