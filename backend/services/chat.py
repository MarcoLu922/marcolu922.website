from pymongo import MongoClient
from datetime import datetime
from backend.config import Config

client = MongoClient(Config.MONGO_URI)
db = client.get_default_database()

def save_chat_log(conversation_id, user_input, agent_response):
    chat_logs = db.chat_logs
    chat_logs.insert_one({
        'conversation_id': conversation_id,
        'user_input': user_input,
        'agent_response': agent_response,
        'timestamp': datetime.utcnow()
    })