from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    transcripts = db.relationship('Transcript', backref='user', lazy=True)
    chats = db.relationship('Chat', backref='user', lazy=True)
    
    def __init__(self, **kwargs):
        """
        Initialize a User instance.
        
        Parameters:
        - username: Required, username for the user
        - password: Required, hashed password
        """
        super(User, self).__init__(**kwargs)

class Transcript(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_url = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chats = db.relationship('Chat', backref='transcript', lazy=True)
    
    def __init__(self, **kwargs):
        """
        Initialize a Transcript instance.
        
        Parameters:
        - video_url: Required, URL of the YouTube video
        - content: Required, transcript content
        - user_id: Required, ID of the user who created the transcript
        """
        super(Transcript, self).__init__(**kwargs)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    transcript_id = db.Column(db.Integer, db.ForeignKey('transcript.id'), nullable=False)
    messages = db.relationship('Message', backref='chat', lazy=True, cascade='all, delete-orphan')
    
    def __init__(self, **kwargs):
        """
        Initialize a Chat instance.
        
        Parameters:
        - title: Required, title of the chat
        - user_id: Required, ID of the user who created the chat
        - transcript_id: Required, ID of the associated transcript
        """
        super(Chat, self).__init__(**kwargs)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(10), nullable=False)  # 'user' or 'assistant'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    
    def __init__(self, **kwargs):
        """
        Initialize a Message instance.
        
        Parameters:
        - content: Required, message content
        - role: Required, 'user' or 'assistant'
        - chat_id: Required, ID of the chat this message belongs to
        """
        super(Message, self).__init__(**kwargs)