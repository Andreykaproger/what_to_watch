from flask import render_template
from flask_login import login_required

from opinions_app.models import User, Opinion

from . import users_bp

@users_bp.route("/users/<string:username>")
@login_required
def user_profile_view(username):
    user = User.query.filter_by(username=username).first()
    opinions = Opinion.query.filter_by(user_id=user.id).all()
    return render_template('users/user_profile.html', user=user, opinions=opinions)