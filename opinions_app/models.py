from datetime import datetime

from . import db

class Opinion(db.Model):
    """Модель БД мнений о фильмах"""
    id = db.Column(db.Integer, primary_key=True)
    tittle = db.Column(db.String(128), nullable=False)
    text = db.Column(db.Text, unique=True, nullable=False)
    source = db.Column(db.String(256))
    timestamp = db.Column(db.DateTime, index = True, default=datetime.utcnow)
    added_by = db.Column(db.String(64))

    def to_dict(self):
        return dict(
            id = self.id,
            title = self.tittle,
            text = self.text,
            source = self.source,
            timestamp = self.timestamp,
            added_by = self.added_by
        )

    def from_dict(self, data):
        for field in ['tittle','text','source','added_by']:
            if field in data:
                setattr(self, field, data[field])
