from .forms import OpinionForm, RegisterForm, LoginForm
from .models import Opinion, User
from .decorators import admin_required
from random import randrange
from datetime import datetime
from flask import abort, flash, redirect, render_template, url_for, request
from flask_login import login_required, current_user, login_user, logout_user

from . import app, db

@app.route('/admin')
@admin_required
def admin_view():
    users = User.query.all()
    return render_template('admin.html', users=users)




## Доделать возможности админа, приступить к следующему заданию - подтверждение через email.



## доделать функционал принятия и отказа мнения (с причиной отказа).








