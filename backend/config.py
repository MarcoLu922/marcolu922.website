class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:20030922@localhost:3306/chatbot_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MONGO_URI = 'mongodb://localhost:27017/chatbot_db'
    JWT_TOKEN_LOCATION = ['headers']  # JWT 令c牌存储在请求头中