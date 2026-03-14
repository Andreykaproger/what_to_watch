from datetime import datetime
from flask import current_app

from opinions_app.models import TokenBlockList
from opinions_app import db

def cleanup_expired_tokens():

    expire_time = current_app.config["JWT_REFRESH_TOKEN_EXPIRES"]

    cutoff = datetime.utcnow() - expire_time

    tokens = db.session.query(TokenBlockList).filter(
        TokenBlockList.created_at < cutoff
    )

    count = tokens.count()
    tokens.delete(synchronize_session=False)

    db.session.commit()

    return count

