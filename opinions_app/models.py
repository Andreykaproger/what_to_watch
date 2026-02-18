from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    opinion = db.relationship('Opinion', backref='author', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Opinion(db.Model):
    """Модель БД мнений о фильмах"""
    id = db.Column(db.Integer, primary_key=True)
    tittle = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index = True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        return dict(
            id = self.id,
            tittle = self.tittle,
            text = self.text,
            source = self.source,
            timestamp = self.timestamp,
            user_id = self.user_id
        )

    def from_dict(self, data):
        for field in ['tittle','text','source', 'user_id']:
            if field in data:
                setattr(self, field, data[field])
