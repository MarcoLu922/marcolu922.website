from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from backend.extension import db
from backend.models.user import User

# 创建 auth 蓝图
user_bp = Blueprint('user', __name__)


@user_bp.route('/user/me', methods=['GET'])
@jwt_required()
def get_user_info():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({'username': user.username, 'email': user.email})

@user_bp.route('/user/me', methods=['PUT'])
@jwt_required()
def update_user():
    user_id = get_jwt_identity()
    user = User.query.get_or_404(user_id)
    data = request.json

    # 更新字段示例，视情况可扩展
    if "username" in data:
        user.username = data["username"]
    if "email" in data:
        user.email = data["email"]
    if "password" in data:
        user.password = generate_password_hash(data["password"])

    db.session.commit()
    return jsonify({'message': '用户资料更新成功'}), 200

@user_bp.route('/user/logout', methods=['POST'])
@jwt_required()
def logout_user():
    return jsonify({'message': '注销成功'}), 200

