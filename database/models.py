from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    profile_pic = db.Column(db.String(256), default='default.png')
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    histories = db.relationship('History', backref='user', lazy=True)

class Gesture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    emoji = db.Column(db.String(50))
    description = db.Column(db.String(256))
    
    histories = db.relationship('History', backref='gesture', lazy=True)

class Meme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gesture_name = db.Column(db.String(100), nullable=False)  # Map to which gesture it belongs
    filepath = db.Column(db.String(256), nullable=False)

class Gif(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gesture_name = db.Column(db.String(100), nullable=False)
    filepath = db.Column(db.String(256), nullable=False)

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)  # Can be null for guests
    gesture_id = db.Column(db.Integer, db.ForeignKey('gesture.id'), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    emotion = db.Column(db.String(50))
    caption = db.Column(db.String(256))
    screenshot_path = db.Column(db.String(256))
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)
