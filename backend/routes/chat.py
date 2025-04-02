from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from backend.extension import db
from backend.models.conversation import Conversation
from backend.models.message import Message

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/conversation', methods=['GET'])
@jwt_required()
def get_conversations():
    user_id = get_jwt_identity()
    conversations = Conversation.query.filter_by(user_id=user_id).all()
    return jsonify([{'id': c.id, 'status': c.status, 'start_time': c.start_time} for c in conversations])

@chat_bp.route('/conversation/<int:conversation_id>', methods=['GET'])
@jwt_required()
def get_conversation(conversation_id):
    user_id = get_jwt_identity()
    conversation = Conversation.query.filter_by(id=conversation_id, user_id=user_id).first()
    if not conversation:
        return jsonify({'error': 'NOT_FOUND', 'message': '对话未找到'}), 404
    return jsonify({
        'id': conversation.id,
        'status': conversation.status,
        'start_time': conversation.start_time,
        'end_time': conversation.end_time
    })

@chat_bp.route('/conversation/<int:conversation_id>/end', methods=['PUT'])
@jwt_required()
def end_conversation(conversation_id):
    user_id = get_jwt_identity()
    conversation = Conversation.query.filter_by(id=conversation_id, user_id=user_id).first()
    if not conversation:
        return jsonify({'error': 'NOT_FOUND', 'message': '对话未找到'}), 404
    conversation.status = 'ended'
    conversation.end_time = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': '对话已结束'})

@chat_bp.route('/conversation/<int:conversation_id>/history', methods=['GET'])
@jwt_required()
def get_conversation_history(conversation_id):
    user_id = get_jwt_identity()
    conversation = Conversation.query.filter_by(id=conversation_id, user_id=user_id).first()
    if not conversation:
        return jsonify({'error': 'NOT_FOUND', 'message': '对话未找到'}), 404
    messages = Message.query.filter_by(conversation_id=conversation_id).all()
    return jsonify([{
        'user_input': m.user_input,
        'agent_response': m.agent_response,
        'timestamp': m.timestamp
    } for m in messages])