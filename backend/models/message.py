from datetime import datetime
from backend.extension import db

class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)
    user_input = db.Column(db.Text)
    agent_response = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)