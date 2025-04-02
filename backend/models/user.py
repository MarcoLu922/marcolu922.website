from datetime import datetime
from backend.extension import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 注册时间
    last_login = db.Column(db.DateTime, nullable=True)  # 上次登录时间
    role = db.Column(db.Enum('user', 'admin'), default='user')
    status = db.Column(db.Enum('active', 'disabled'), default='active')