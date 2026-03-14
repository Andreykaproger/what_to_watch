from flask import render_template, abort, request
from flask_login import login_required, current_user

from opinions_app.models import User, Opinion

from . import users_bp

@users_bp.route("/users/<string:username>")
@login_required
def user_profile_view(username):
    user = User.query.filter_by(username=username).first()
    if not user.is_active and not current_user.is_admin():
        abort(404)

    page = request.args.get('page', 1, type=int)
    per_page = 3

    opinions = Opinion.query.filter_by(user_id=user.id).order_by(
        Opinion.timestamp.desc()
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    return render_template('users/user_profile.html', user=user, opinions=opinions)