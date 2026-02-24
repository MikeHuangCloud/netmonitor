from flask import Flask
from flask_login import LoginManager
from config import Config
from models import init_db, User
from controllers import auth_bp, main_bp, api_bp


def create_app():
    """建立 Flask 應用"""
    app = Flask(__name__, 
                template_folder='views/templates',
                static_folder='views/static')
    
    # 載入配置
    app.config.from_object(Config)
    
    # 初始化資料庫
    init_db(app)
    
    # 初始化 Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = '請先登入'
    login_manager.login_message_category = 'warning'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # 註冊藍圖
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp)
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
