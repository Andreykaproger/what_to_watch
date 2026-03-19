from datetime import datetime
from typing import Literal

from opinions_app import db
from opinions_app.models import Opinion, OpinionStatus

def approve_reject_opinion(mode: Literal["approve", "reject"], id, json_data = None):

    opinion = Opinion.query.get(id)

    if not opinion:
        return None, "Мнение не найдено", 404

    if mode == "approve":

        if opinion.status == OpinionStatus.APPROVED:
            return None, "Мнение уже принято", 400

        opinion.status = OpinionStatus.APPROVED
        opinion.rejection_reason = None
        opinion.moderated_at = datetime.utcnow()


    elif mode == "reject":

        if opinion.status == OpinionStatus.REJECTED:
            return None ,"Мнение уже отклонено", 400

        opinion.status = OpinionStatus.REJECTED
        opinion.rejection_reason = json_data["reason"]
        opinion.moderated_at = datetime.utcnow()

    db.session.commit()

    return opinion, None, 200