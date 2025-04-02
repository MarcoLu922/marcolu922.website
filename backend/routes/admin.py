from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from werkzeug.security import generate_password_hash
from backend.extension import db
from backend.models.conversation import Conversation
from backend.models.user import User

admin_bp = Blueprint('admin', __name__)

# 自定义装饰器，确保只有管理员能访问
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if user.role != 'admin':
            return jsonify({'error': 'FORBIDDEN', 'message': '管理员权限要求'}), 403
        return fn(*args, **kwargs)
    return wrapper

@admin_bp.route('/user', methods=['GET'])
@jwt_required()
@admin_required
def get_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'username': u.username, 'role': u.role} for u in users])

@admin_bp.route('/conversation', methods=['GET'])
@jwt_required()
@admin_required
def get_conversations():
    conversations = Conversation.query.all()
    return jsonify([{'id': c.id, 'user_id': c.user_id, 'status': c.status} for c in conversations])

@admin_bp.route('/conversation/<int:conversation_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_conversation(conversation_id):
    conversation = Conversation.query.get(conversation_id)
    if not conversation:
        return jsonify({'error': 'NOT_FOUND', 'message': '对话未找到'}), 404
    db.session.delete(conversation)
    db.session.commit()
    return jsonify({'message': '对话删除成功'})


# 添加用户
@admin_bp.route('/user', methods=['POST'])
@jwt_required()
@admin_required
def add_user():
    data = request.json
    # 检查用户名或邮箱是否已存在
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'INVALID_INPUT', 'message': '用户名已存在'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'INVALID_INPUT', 'message': '邮箱已存在'}), 400

    # 创建新用户，密码加密存储
    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        username=data['username'],
        password=hashed_password,
        email=data['email'],
        role=data.get('role', 'user')  # 默认角色为 "user"
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': '用户创建成功', 'user_id': new_user.id}), 201


# 更新用户
@admin_bp.route('/user/<int:user_id>', methods=['PUT'])
@jwt_required()
@admin_required
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'USER_NOT_FOUND', 'message': '用户ID不存在'}), 404

    data = request.json
    # 更新用户字段（仅更新提供的字段）
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'role' in data:
        user.role = data['role']
    if 'status' in data:
        user.status = data['status']

    db.session.commit()
    return jsonify({
        'message': '用户信息更新成功',
        'user': {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'status': user.status
        }
    })


# 删除用户
@admin_bp.route('/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'USER_NOT_FOUND', 'message': '用户ID不存在'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': '用户删除成功'})