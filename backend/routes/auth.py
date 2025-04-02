from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash
from backend.models.user import User
from datetime import datetime
from backend.extension import db

# 创建 auth 蓝图
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    # 检查用户名或邮箱是否已存在
    existing_user = User.query.filter(
        (User.username == data['username']) | (User.email == data['email'])
    ).first()
    if existing_user:
        return jsonify({'error': '用户名或邮箱已被注册'}), 400
    hashed_password = generate_password_hash(data['password'])
    new_user = User(username=data['username'], password=hashed_password, email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': '注册成功'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        user.last_login = datetime.utcnow()
        db.session.commit()
        # 生成 JWT Token
        token = create_access_token(identity=user.id)
        return jsonify({'message': '登录成功', 'token': token})
    return jsonify({'error': '无效的用户名或密码'}), 401
