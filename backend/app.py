import os
import logging
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from config import Config
from backend.extension import db
from backend.routes.auth import auth_bp
from backend.routes.chat import chat_bp
from backend.routes.feedback import feedback_bp
from backend.routes.admin import admin_bp
from backend.routes.user import user_bp
from backend.routes.conversation import conversation_bp

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# 创建 Flask 应用实例
app = Flask(__name__)
app.config.from_object(Config)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'default-secret-key')  # 从环境变量获取密钥，开发时使用默认值

# 初始化数据库
db.init_app(app)

# 初始化 JWT
jwt = JWTManager(app)

# 注册蓝图，统一使用 /api 前缀
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(chat_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(conversation_bp, url_prefix='/api')
app.register_blueprint(feedback_bp, url_prefix='/api')

# 全局错误处理
@app.errorhandler(404)
def not_found_error(error):
    return jsonify({'error': 'Not Found', 'message': 'The requested resource was not found.'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal Server Error', 'message': 'An unexpected error occurred.'}), 500

# 主程序入口
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # 创建数据库表
    logger.info('Application started')
    app.run(debug=True)