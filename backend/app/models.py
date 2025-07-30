from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from app import db

# db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default='agent')  # roles: admin, agent, viewer
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username}>"
    
    
class Platform(db.Model):
    __tablename__ = 'platforms'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    icon_url = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Platform {self.name}>"

from datetime import datetime

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    direction = db.Column(db.String(10), nullable=False)  # 'incoming' or 'outgoing'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    platform_id = db.Column(db.Integer, db.ForeignKey('platforms.id'), nullable=False)

    user = db.relationship('User', backref='messages', lazy=True)
    platform = db.relationship('Platform', backref='messages', lazy=True)

    def __repr__(self):
        return f"<Message {self.id} | {self.direction} | {self.timestamp}>"
class FAQ(db.Model):
    __tablename__ = 'faqs'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(100), nullable=True)
    times_asked = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<FAQ {self.id} | {self.question}>"

class Analytics(db.Model):
    __tablename__ = 'analytics'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    total_messages = db.Column(db.Integer, default=0)
    unique_users = db.Column(db.Integer, default=0)
    avg_response_time = db.Column(db.Float, default=0.0)
    most_active_platform = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"<Analytics {self.date}>"
class Settings(db.Model):
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    default_view = db.Column(db.String(50), default='inbox')
    theme = db.Column(db.String(20), default='light')
    notifications = db.Column(db.Boolean, default=True)
    language = db.Column(db.String(10), default='en')

    user = db.relationship('User', backref='settings', lazy=True)

    def __repr__(self):
        return f"<Settings for User {self.user_id}>"


