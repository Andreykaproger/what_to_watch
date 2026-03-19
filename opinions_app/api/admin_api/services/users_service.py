from datetime import datetime
from typing import Literal

from opinions_app import db
from opinions_app.models import User

def block_unblock_user(mode: Literal["block", "unblock"], id, json_data = None):

    user = User.query.get(id)

    if not user:
        return None, "Пользователь не найден", 404

    if mode == "block":

        if user.is_active == False:
            return None, "Пользователь уже заблокирован", 400

        user.is_active = False
        user.block_reason = json_data["reason"]
        user.blocked_at = datetime.utcnow()

    elif mode == "unblock":

        if user.is_active == True:
            return None , "Пользователь уже разблокирован", 400

        user.is_active = True
        user.block_reason = None
        user.blocked_at = None

    db.session.commit()

    return user, None, 200