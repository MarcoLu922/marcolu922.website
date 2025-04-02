from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from backend.extension import db
from backend.models.conversation import Conversation
from backend.models.feedback import Feedback

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/feedback', methods=['POST'])
@jwt_required()
def submit_feedback():
    data = request.json
    user_id = get_jwt_identity()
    conversation = Conversation.query.get(data['conversation_id'])
    if not conversation or conversation.user_id != user_id:
        return jsonify({'error': 'INVALID_CONVERSATION', 'message': '对话不存在或无权限'}), 403
    feedback = Feedback(
        conversation_id=data['conversation_id'],
        user_id=user_id,
        rating=data['rating'],
        comment=data.get('comment'),
        created_at=datetime.utcnow()
    )
    db.session.add(feedback)
    db.session.commit()
    return jsonify({'message': '反馈提交成功'}), 201

@feedback_bp.route('/feedback/<int:conversation_id>', methods=['GET'])
@jwt_required()
def get_feedback(conversation_id):
    user_id = get_jwt_identity()
    feedback = Feedback.query.filter_by(conversation_id=conversation_id, user_id=user_id).first()
    if not feedback:
        return jsonify({'error': 'NOT_FOUND', 'message': '反馈未找到'}), 404
    return jsonify({
        'rating': feedback.rating,
        'comment': feedback.comment,
        'created_at': feedback.created_at
    })