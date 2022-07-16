from app import db
from datetime import datetime


class Announcement(db.Model):
    __tablename__ = 'announcement'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    text = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=datetime.now())
    owner = db.Column(db.Integer, db.ForeignKey("users.id"))

    def __repr__(self):
        return f'<Advertisement {self.id} - {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'text': self.description,
            'created_at': self.created_at,
        }


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(200), unique=True)
    announcement = db.relationship(Announcement, backref='user')

    def __repr__(self):
        return f'<User {self.id} - {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email
        }
