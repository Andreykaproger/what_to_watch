from enum import Enum
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db

class OpinionStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"

class User(db.Model, UserMixin):
    """Модель пользователя"""

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    is_active = db.Column(db.Boolean, default=True)
    block_reason = db.Column(db.Text, nullable=True)
    blocked_at = db.Column(db.DateTime)

    role = db.Column(db.Enum(UserRole), default=UserRole.USER)

    opinion = db.relationship('Opinion', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == UserRole.ADMIN


class Opinion(db.Model):
    """Модель БД мнений о фильмах"""

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(256))

    timestamp = db.Column(
        db.DateTime,
        index = True,
        default=datetime.utcnow
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id'),
        nullable=False
    )

    status = db.Column(
        db.Enum(OpinionStatus),
        default=OpinionStatus.PENDING
    )

    rejection_reason = db.Column(db.Text, nullable=True)
    moderated_at = db.Column(db.DateTime)

    @staticmethod
    def visible():
        return (
        Opinion.query.join(User)
        .filter(
            Opinion.status == OpinionStatus.APPROVED,
            User.is_active == True
        )
        )

    def is_visible_to(self, viewer):

        if self.status == OpinionStatus.APPROVED:
            return True

        if viewer.is_authenticated:

            if viewer.is_admin():
                return True

            if viewer.id == self.user_id:
                return True

        return False

class AdminLog(db.Model):
    """Модель действий администратора"""

    id = db.Column(db.Integer, primary_key=True)

    action = db.Column(db.String(255))

    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        index=True
    )

    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class TokenBlockList(db.Model):
    """Модель заблокированных токенов авторизации JWT"""

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

