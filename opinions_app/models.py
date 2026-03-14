from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    block_reason = db.Column(db.Text, nullable=True)
    blocked_at = db.Column(db.DateTime)

    role = db.Column(db.String(20), default='user')

    opinion = db.relationship('Opinion', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == 'admin'

    def to_dict(self):
        return dict(
            id = self.id,
            username = self.username,
            email = self.email,
            is_active = self.is_active,
            role = self.role,
        )


class Opinion(db.Model):
    """Модель БД мнений о фильмах"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index = True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')
    rejection_reason = db.Column(db.Text, nullable=True)
    moderated_at = db.Column(db.DateTime)

    def to_dict(self):
        return dict(
            id = self.id,
            title = self.title,
            text = self.text,
            source = self.source,
            timestamp = self.timestamp,
            user_id = self.user_id,
            status = self.status,
        )

    def from_dict(self, data):
        for field in ['title','text','source', 'user_id']:
            if field in data:
                setattr(self, field, data[field])

    @staticmethod
    def visible():
        return (Opinion.query
        .join(User)
        .filter(
            Opinion.status == 'approved',
            User.is_active == True
        )
    )

    def is_visible_to(self, viewer):
        if (
                viewer.is_authenticated and
                (viewer.is_admin() or
                self.user_id != viewer.id)
        ):
            return True
        if not self.status == "rejected":
            return True
        return False

class AdminLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class TokenBlockList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow())

