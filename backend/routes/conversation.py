from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from backend.models.conversation import Conversation
from backend.models.message import Message
from backend.services.ai_service import get_agent_response
from backend.extension import db
from backend.services.chat import save_chat_log
from backend.utils.context import update_context

# 创建 conversation 蓝图
conversation_bp = Blueprint('conversation', __name__)

@conversation_bp.route('/conversation', methods=['POST'])
@jwt_required()
def start_conversation():
    user_id = get_jwt_identity()
    new_conversation = Conversation(user_id=user_id)
    db.session.add(new_conversation)
    db.session.commit()
    return jsonify({'conversation_id': new_conversation.id}), 201


@conversation_bp.route('/conversation/<int:conversation_id>/message', methods=['POST'])
@jwt_required()
def send_message(conversation_id):
    data = request.json
    user_input = data.get('message')
    if not user_input:
        return jsonify({'error': '缺少消息内容'}), 400

    conversation = Conversation.query.get_or_404(conversation_id)
    existing_context = conversation.context or ""

    # 如果有用户画像或长期记忆，可在此传入，目前为空
    user_profile = {}

    # 生成回答，调用大模型接口
    agent_response = get_agent_response(user_input, context=existing_context, user_profile=user_profile)

    # 更新对话上下文
    updated_context = update_context(existing_context, user_input, agent_response, max_total_length=2000)
    conversation.context = updated_context

    # 保存消息记录
    new_message = Message(
        conversation_id=conversation_id,
        user_input=user_input,
        agent_response=agent_response
    )
    db.session.add(new_message)
    db.session.commit()

    save_chat_log(conversation_id, user_input, agent_response)
    return jsonify({'user_message': user_input, 'agent_response': agent_response})